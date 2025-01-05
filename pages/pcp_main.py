import os
import sys
from pathlib import Path

# Força desabilitar sistema de páginas
sys.path.insert(0, str(Path(__file__).parent.parent))
from setup_pages import disable_pages
disable_pages()

import streamlit as st
import logging
from shared.components.sidebar import create_sidebar
from modules.pcp.views.visualizations import (
    planejamento,
    programacao,
    capacidade,
    ordens
)

logger = logging.getLogger('streamlit_app')

def remove_streamlit_elements():
    """Remove elementos padrão do Streamlit"""
    st.markdown("""
        <style>
            /* Remove navegação lateral */
            [data-testid="stSidebarNav"],
            div[data-testid="stSidebarNav"],
            section[data-testid="stSidebarNav"] {
                display: none !important;
                width: 0 !important;
                height: 0 !important;
                position: absolute !important;
                overflow: hidden !important;
                z-index: -1 !important;
            }
            
            /* Remove menu e outros elementos */
            #MainMenu, footer, header,
            .stDeployButton, [data-testid="stToolbar"],
            .main-nav, [data-testid="collapsedControl"] {
                display: none !important;
            }
            
            /* Remove botão de expandir sidebar */
            button[kind="header"],
            .css-1d391kg,
            .css-14xtw13 {
                display: none !important;
            }
            
            /* Ajusta sidebar */
            section[data-testid="stSidebar"] > div {
                padding-top: 0 !important;
            }
            
            /* Remove elementos de navegação específicos */
            .stApp > header,
            .stApp [data-testid="stDecoration"],
            div.element-container:has([data-testid="stSidebarNav"]) {
                display: none !important;
            }
        </style>
        
        <script>
            // Remove elementos de navegação assim que possível
            function removeNavElements() {
                const elements = document.querySelectorAll('[data-testid="stSidebarNav"], .main-nav');
                elements.forEach(el => el.remove());
            }
            
            // Executa imediatamente e observa mudanças
            removeNavElements();
            new MutationObserver(removeNavElements).observe(
                document.body,
                {childList: true, subtree: true}
            );
        </script>
    """, unsafe_allow_html=True)

def load_pcp_module():
    logger.debug("=== INICIANDO MÓDULO PCP ===")
    
    # Configuração DEVE ser a primeira chamada Streamlit
    st.set_page_config(
        page_title="Módulo PCP",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={}
    )
    
    # Carrega os estilos personalizados globais
    with open('.streamlit/custom.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Remove navegação imediatamente
    remove_streamlit_elements()
    
    # Configuração do sidebar
    menu_items = {
        "Planejamento da Produção": planejamento.render,
        "Programação da Produção": programacao.render,
        "Análise de Capacidade": capacidade.render,
        "Ordens de Produção": ordens.render
    }
    
    selected_dashboard = create_sidebar(
        "Módulo PCP",
        menu_items.keys()
    )
    
    # Remove navegação novamente após criar sidebar
    remove_streamlit_elements()
    
    # Renderiza o dashboard selecionado
    if selected_dashboard in menu_items:
        menu_items[selected_dashboard]()
        # Remove navegação uma última vez
        remove_streamlit_elements()

if __name__ == "__main__":
    try:
        load_pcp_module()
    except Exception as e:
        logger.error(f"Erro ao carregar módulo PCP: {str(e)}") 