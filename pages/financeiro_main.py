import streamlit as st
from shared.components.sidebar import create_sidebar
from modules.financeiro.views.visualizations import (
    fluxo_caixa,
    dre,
    indicadores,
    orcamento
)

def load_financeiro_module():
    # Configuração DEVE ser a primeira chamada Streamlit
    st.set_page_config(
        page_title="Módulo Financeiro", 
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={}
    )
    
    # Carrega os estilos personalizados globais
    with open('.streamlit/custom.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Configuração do sidebar
    menu_items = {
        "Fluxo de Caixa": fluxo_caixa.render,
        "DRE": dre.render,
        "Indicadores Financeiros": indicadores.render,
        "Orçamento": orcamento.render
    }
    
    selected_dashboard = create_sidebar(
        "Módulo Financeiro",
        menu_items.keys()
    )
    
    # Renderiza o dashboard selecionado
    if selected_dashboard in menu_items:
        menu_items[selected_dashboard]()

if __name__ == "__main__":
    load_financeiro_module() 