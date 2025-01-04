import streamlit as st
from core.auth.login import setup_login
from config.settings import APP_NAME, MODULES
from shared.components.cards import create_module_card

def main():
    # Configuração inicial da página
    st.set_page_config(
        page_title=APP_NAME,
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Verificar autenticação
    authenticated, username = setup_login()
    
    if authenticated:
        # Remover menu hamburguer e rodapé
        st.markdown("""
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
            </style>
        """, unsafe_allow_html=True)

        # Cabeçalho
        st.title(APP_NAME)
        st.markdown("---")

        # Criar grid de cards para módulos
        cols = st.columns(3)
        for idx, (module_id, module_info) in enumerate(MODULES.items()):
            col_idx = idx % 3
            with cols[col_idx]:
                create_module_card(
                    title=module_info["name"],
                    icon=module_info["icon"],
                    color=module_info["color"],
                    dashboards=module_info["dashboards"],
                    module_id=module_id
                )

if __name__ == "__main__":
    main()
