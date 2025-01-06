import streamlit as st
import pandas as pd
from core.auth.login import setup_login
from core.auth.permissions import UserRole, Permissions
from config.settings import APP_NAME, MODULES
from shared.components.cards import create_module_card
from shared.utils.cursor_rules import CursorRules
from shared.components.charts import ChartComponents
from shared.utils.alerts import AlertManager
from modules.comercial import render_comercial_module  # Nova importação

# Configuração da página DEVE ser a primeira chamada Streamlit
st.set_page_config(
    page_title="Empresamix BI",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Carrega os estilos personalizados globais
with open('.streamlit/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inicialização do estado da aplicação
if 'current_module' not in st.session_state:
    st.session_state.current_module = 'home'

def render_kpi(col, label, value, delta, help, kpi_name, user_role):
    """Renderiza um KPI se o usuário tiver permissão"""
    if Permissions.can_view_kpi(user_role, kpi_name):
        with col:
            st.metric(
                label=label,
                value=value,
                delta=delta,
                help=help
            )
    else:
        with col:
            st.info("🔒 Acesso Restrito")

def main():
    # Verificar autenticação
    authenticated, username = setup_login()
    
    if authenticated:
        # Por enquanto, vamos assumir um papel de admin para teste
        user_role = UserRole.ADMIN
        
        # Verifica o módulo atual e redireciona se necessário
        current_module = st.session_state.get('current_module', 'home')
        
        if current_module != 'home':
            # Aqui você pode adicionar a lógica para carregar diferentes módulos
            st.title(f"Módulo {current_module.title()}")
            
            # Botão para voltar à home
            if st.button("← Voltar para Home"):
                st.session_state.current_module = 'home'
                st.rerun()
            
            # Carrega o módulo específico
            if current_module == "comercial":
                render_comercial_module()  # Chama a função do módulo comercial
            elif current_module == "financeiro":
                st.write("Conteúdo do módulo Financeiro")
            # ... adicione outros módulos conforme necessário ...
                
            return  # Importante: não continua renderizando a home
        
        # Cabeçalho
        st.title(APP_NAME)
        
        # Dashboard Principal com KPIs
        st.markdown("### 📈 Visão Geral")
        
        # Primeira linha de KPIs
        col1, col2, col3, col4 = st.columns(4)
        render_kpi(
            col1, 
            "Faturamento Mensal", 
            "R$ 1.5M", 
            "+12%", 
            "Faturamento total do mês atual",
            "faturamento",
            user_role
        )
        render_kpi(
            col2,
            "Margem EBITDA",
            "25%",
            "+5%",
            "Margem EBITDA do período atual",
            "margem_ebitda",
            user_role
        )
        render_kpi(
            col3,
            "Eficiência Operacional",
            "92%",
            "+3%",
            "Taxa de eficiência da produção",
            "eficiencia",
            user_role
        )
        render_kpi(
            col4,
            "Satisfação Clientes",
            "4.8/5.0",
            "+0.3",
            "Média de satisfação dos clientes",
            "satisfacao",
            user_role
        )

        # Segunda linha de KPIs
        col1, col2, col3, col4 = st.columns(4)
        render_kpi(
            col1,
            "Leads Qualificados",
            "250",
            "+8%",
            "Número de leads qualificados no mês",
            "leads",
            user_role
        )
        render_kpi(
            col2,
            "Taxa de Conversão",
            "15%",
            "+2%",
            "Taxa de conversão de leads",
            "conversao",
            user_role
        )
        render_kpi(
            col3,
            "Turnover",
            "3%",
            "-1%",
            "Taxa de turnover mensal",
            "turnover",
            user_role
        )
        render_kpi(
            col4,
            "Ordens em Produção",
            "15",
            "+2",
            "Número de ordens em produção",
            "ordens_producao",
            user_role
        )

        # Gráficos principais
        st.markdown("### 📊 Indicadores Chave")
        col1, col2 = st.columns(2)
        
        with col1:
            # Dados de exemplo - Faturamento últimos 6 meses
            df_faturamento = pd.DataFrame({
                'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                'Faturamento': [1.2, 1.3, 1.35, 1.4, 1.45, 1.5],
                'Meta': [1.25, 1.3, 1.35, 1.4, 1.45, 1.5]
            })
            
            fig_fat = ChartComponents.create_line_chart(
                df_faturamento,
                x='Mês',
                y=['Faturamento', 'Meta'],
                title='Evolução do Faturamento (em milhões R$)'
            )
            st.plotly_chart(fig_fat, use_container_width=True)
        
        with col2:
            # Dados de exemplo - Distribuição de vendas por região
            df_vendas = pd.DataFrame({
                'Região': ['Sul', 'Sudeste', 'Norte', 'Nordeste', 'Centro-Oeste'],
                'Vendas': [280, 520, 150, 320, 180]
            })
            
            fig_vendas = ChartComponents.create_pie_chart(
                df_vendas,
                values='Vendas',
                names='Região',
                title='Distribuição de Vendas por Região (em mil R$)'
            )
            st.plotly_chart(fig_vendas, use_container_width=True)

        st.markdown("---")

        # Alertas importantes
        with st.expander("⚠️ Alertas Importantes"):
            for module in MODULES:
                if Permissions.can_access_module(user_role, module["id"]):
                    alerts = AlertManager.get_module_alerts(module["id"], user_role)
                    for alert_type, message in alerts:
                        if alert_type == "warning":
                            st.warning(message)
                        elif alert_type == "info":
                            st.info(message)
                        elif alert_type == "success":
                            st.success(message)

        st.markdown("---")

        # Módulos disponíveis
        st.markdown("### 📊 Módulos Disponíveis")
        col1, col2 = st.columns(2)
        
        # Distribuir os módulos em duas colunas
        for idx, module in enumerate(MODULES):
            if Permissions.can_access_module(user_role, module["id"]):
                with col1 if idx % 2 == 0 else col2:
                    create_module_card(
                        title=module["title"],
                        description=module["description"],
                        icon=module["icon"]
                    )

if __name__ == "__main__":
    main()