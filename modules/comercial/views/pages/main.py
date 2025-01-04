import streamlit as st
from shared.components.sidebar import create_sidebar
from modules.comercial.views.visualizations import (
    performance_vendas,
    pipeline,
    leads,
    territorio
)

def load_comercial_module():
    st.set_page_config(page_title="Módulo Comercial", layout="wide")
    
    # Configuração do sidebar
    menu_items = {
        "Performance de Vendas": performance_vendas.render,
        "Análise de Pipeline": pipeline.render,
        "Gestão de Leads": leads.render,
        "Análise de Território": territorio.render
    }
    
    selected_dashboard = create_sidebar(
        "Módulo Comercial",
        menu_items.keys()
    )
    
    # Renderiza o dashboard selecionado
    if selected_dashboard in menu_items:
        menu_items[selected_dashboard]()

if __name__ == "__main__":
    load_comercial_module() 