import streamlit as st
from .views.visualizations import (
    render_territorio,
    render_leads,
    render_performance,
    render_pipeline
)

def render_nav_button(label: str, icon: str, is_active: bool = False) -> bool:
    """Renderiza um botão de navegação estilizado"""
    button_style = """
        <style>
        div[data-testid="stButton"] button {
            background-color: %s;
            color: white;
            border: 1px solid %s;
            padding: 0.5rem 1rem;
            width: 100%%;
            text-align: left;
            margin: 0.2rem 0;
            border-radius: 4px;
        }
        div[data-testid="stButton"] button:hover {
            border-color: #4CAF50;
            background-color: #2E2E2E;
        }
        </style>
    """ % ("#2E2E2E" if is_active else "#1E1E1E", "#4CAF50" if is_active else "#333")
    
    st.markdown(button_style, unsafe_allow_html=True)
    return st.button(f"{icon} {label}")

def render_comercial_module():
    """Renderiza o módulo comercial com navegação lateral"""
    
    # Inicializa o estado da navegação se não existir
    if 'comercial_page' not in st.session_state:
        st.session_state.comercial_page = None
    
    # Configuração do sidebar
    with st.sidebar:
        st.title("Navegação")
        
        # Botões de navegação estilizados
        if render_nav_button("Análise Territorial", "📍", 
                           st.session_state.comercial_page == "territorial"):
            st.session_state.comercial_page = "territorial"
            st.rerun()
            
        if render_nav_button("Leads", "🎯",
                           st.session_state.comercial_page == "leads"):
            st.session_state.comercial_page = "leads"
            st.rerun()
            
        if render_nav_button("Performance de Vendas", "📈",
                           st.session_state.comercial_page == "performance"):
            st.session_state.comercial_page = "performance"
            st.rerun()
            
        if render_nav_button("Pipeline", "🔄",
                           st.session_state.comercial_page == "pipeline"):
            st.session_state.comercial_page = "pipeline"
            st.rerun()
    
    # Renderiza o dashboard selecionado
    if st.session_state.comercial_page == "territorial":
        render_territorio()
    elif st.session_state.comercial_page == "leads":
        render_leads()
    elif st.session_state.comercial_page == "performance":
        render_performance()
    elif st.session_state.comercial_page == "pipeline":
        render_pipeline()
    else:
        # Página inicial do módulo
        st.header("👋 Bem-vindo ao Módulo Comercial")
        st.write("Selecione um dashboard no menu lateral para começar.")