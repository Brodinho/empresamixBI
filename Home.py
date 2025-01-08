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