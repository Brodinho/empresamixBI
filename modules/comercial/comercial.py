import streamlit as st

def render_analise_territorial():
    st.header("📍 Análise Territorial")
    st.write("Dashboard de análise territorial em desenvolvimento...")
    # Aqui iremos adicionar o conteúdo do dashboard

def render_leads():
    st.header("🎯 Leads")
    st.write("Dashboard de leads em desenvolvimento...")
    # Aqui iremos adicionar o conteúdo do dashboard

def render_performance_vendas():
    st.header("📈 Performance de Vendas")
    st.write("Dashboard de performance em desenvolvimento...")
    # Aqui iremos adicionar o conteúdo do dashboard

def render_pipeline():
    st.header("🔄 Pipeline")
    st.write("Dashboard de pipeline em desenvolvimento...")
    # Aqui iremos adicionar o conteúdo do dashboard

def render_comercial_module():
    # Configuração do sidebar
    st.sidebar.title("Navegação")
    
    # Botões de navegação no sidebar
    selected_page = st.sidebar.radio(
        "Selecione o Dashboard:",
        [
            "Análise Territorial",
            "Leads",
            "Performance de Vendas",
            "Pipeline"
        ],
        index=0  # Página inicial
    )
    
    # Renderiza o dashboard selecionado
    if selected_page == "Análise Territorial":
        render_analise_territorial()
    elif selected_page == "Leads":
        render_leads()
    elif selected_page == "Performance de Vendas":
        render_performance_vendas()
    elif selected_page == "Pipeline":
        render_pipeline() 