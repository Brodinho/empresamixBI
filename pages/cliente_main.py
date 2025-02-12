import streamlit as st
from shared.components.sidebar import create_sidebar
from modules.cliente.views.visualizations import (
    satisfacao_cliente,
    analise_churn,
    segmentacao_clientes,
    jornada_cliente
)

def load_cliente_module():
    # Configuração DEVE ser a primeira chamada Streamlit
    st.set_page_config(
        page_title="Módulo Cliente", 
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={}
    )
    
    # Carrega os estilos personalizados globais
    with open('.streamlit/custom.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Configuração do sidebar
    menu_items = {
        "Satisfação do Cliente": satisfacao_cliente.render,
        "Análise de Churn": analise_churn.render,
        "Segmentação de Clientes": segmentacao_clientes.render,
        "Jornada do Cliente": jornada_cliente.render
    }
    
    selected_dashboard = create_sidebar(
        "Módulo Cliente",
        menu_items.keys()
    )
    
    # Renderiza o dashboard selecionado
    if selected_dashboard in menu_items:
        menu_items[selected_dashboard]()

if __name__ == "__main__":
    load_cliente_module() 