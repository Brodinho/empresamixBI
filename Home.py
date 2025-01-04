import streamlit as st

# Configuração da página DEVE ser a primeira chamada Streamlit
st.set_page_config(
    page_title="Empresamix BI",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Importações após o set_page_config
from core.auth.login import setup_login
from config.settings import APP_NAME, MODULES
from shared.components.cards import create_module_card, create_info_card, create_nav_button, create_module_container
from setup_pages import setup_module_pages

# Área de debug
debug_info = st.empty()

# Carrega os estilos personalizados
with open('assets/styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Debug da configuração dos módulos
debug_info.info("Setup de páginas iniciado...")
setup_module_pages()
debug_info.info("Setup de páginas concluído")

def main():
    # Verificar autenticação
    authenticated, username = setup_login()
    
    if authenticated:
        # Remove elementos padrão do Streamlit
        st.markdown("""
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                .css-1544g2n {display: none !important;}
                .css-14xtw13 e8zbici0 {display: none !important;}
                section[data-testid="stSidebar"] {display: none !important;}
            </style>
        """, unsafe_allow_html=True)

        # Cabeçalho
        st.title(APP_NAME)
        st.markdown("---")

        # Debug dos módulos disponíveis
        debug_info.info(f"Módulos carregados: {list(MODULES.keys())}")

        # Criar grid de cards informativos
        st.markdown("### 📊 Módulos Disponíveis")
        st.markdown("---")

        cols = st.columns(2, gap="large")
        for idx, (module_id, module_info) in enumerate(MODULES.items()):
            with cols[idx % 2]:
                create_module_container(
                    title=module_info["name"],
                    icon=module_info["icon"],
                    color=module_info["color"],
                    dashboards=module_info["dashboards"],
                    module_id=module_id
                )

if __name__ == "__main__":
    main()
