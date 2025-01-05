import streamlit as st
from core.auth.login import setup_login
from config.settings import APP_NAME, MODULES
from shared.components.cards import create_module_card, create_info_card, create_nav_button, create_module_container

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

def main():
    # Verificar autenticação
    authenticated, username = setup_login()
    
    if authenticated:
        # Cabeçalho
        st.title(APP_NAME)
        st.markdown("---")

        # Criar grid de cards informativos
        st.markdown("### 📊 Módulos Disponíveis")
        st.markdown("---")

        cols = st.columns(2, gap="large")
        
        # Módulo Comercial
        with cols[0]:
            create_module_container(
                title="Comercial",
                icon="📈",
                color="#FF6B6B",
                dashboards=[
                    "Performance de Vendas",
                    "Análise de Pipeline",
                    "Gestão de Leads/Oportunidades",
                    "Análise de Território"
                ],
                module_id="comercial"
            )
            
            # Módulo Financeiro
            create_module_container(
                title="Financeiro",
                icon="💰",
                color="#4ECDC4",
                dashboards=[
                    "Fluxo de Caixa",
                    "DRE",
                    "Indicadores Financeiros",
                    "Orçamento"
                ],
                module_id="financeiro"
            )

            create_module_container(
                title="Operacional",
                icon="⚙️",
                color="#FFB347",
                dashboards=[
                    "Produção",
                    "Controle de Qualidade",
                    "Gestão de Estoque",
                    "Manutenção"
                ],
                module_id="operacional"
            )

            create_module_container(
                title="RH",
                icon="👥",
                color="#FF69B4",
                dashboards=[
                    "Recrutamento e Seleção",
                    "Avaliação de Desempenho",
                    "Treinamento e Desenvolvimento",
                    "Folha de Pagamento"
                ],
                module_id="rh"
            )
        
        # Módulo Cliente
        with cols[1]:
            create_module_container(
                title="Cliente",
                icon="👥",
                color="#45B7D1",
                dashboards=[
                    "Satisfação do Cliente",
                    "Análise de Churn",
                    "Segmentação de Clientes",
                    "Jornada do Cliente"
                ],
                module_id="cliente"
            )

            create_module_container(
                title="Marketing",
                icon="🎯",
                color="#96CEB4",
                dashboards=[
                    "Campanhas de Marketing",
                    "Análise de Mídias Sociais",
                    "Funil de Marketing",
                    "ROI de Marketing"
                ],
                module_id="marketing"
            )

            # ... (código anterior mantido)
            
            create_module_container(
                title="PCP",
                icon="🏭",
                color="#4A90E2",
                dashboards=[
                    "Planejamento da Produção",
                    "Programação da Produção",
                    "Análise de Capacidade",
                    "Ordens de Produção"
                ],
                module_id="pcp"
            )

if __name__ == "__main__":
    main()