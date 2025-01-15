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

def render_rfv():
    st.header("💎 Análise RFV")
    from modules.comercial.views.visualizations.rfv import render_rfv
    render_rfv()

def render_comercial_module():
    st.sidebar.title("Navegação")
    
    # Botões individuais no sidebar
    if st.sidebar.button("📍 Análise Territorial"):
        st.session_state.page = "analise_territorial"
        
    if st.sidebar.button("🎯 Leads"):
        st.session_state.page = "leads"
        
    if st.sidebar.button("📈 Performance de Vendas"):
        st.session_state.page = "performance_vendas"
        
    if st.sidebar.button("🔄 Pipeline"):
        st.session_state.page = "pipeline"
        
    if st.sidebar.button("💎 Análise RFV"):
        st.session_state.page = "rfv"
    
    # Renderiza o dashboard selecionado
    if "page" not in st.session_state:
        st.session_state.page = "home"
        
    if st.session_state.page == "analise_territorial":
        render_analise_territorial()
    elif st.session_state.page == "leads":
        render_leads()
    elif st.session_state.page == "performance_vendas":
        render_performance_vendas()
    elif st.session_state.page == "pipeline":
        render_pipeline()
    elif st.session_state.page == "rfv":
        render_rfv()
    else:
        st.title("Bem-vindo ao Módulo Comercial!")
        st.write("Utilize o menu lateral para acessar os diferentes dashboards disponíveis:")
        st.write("• **Análise Territorial:** Visualize a distribuição geográfica das vendas")
        st.write("• **Leads:** Acompanhe e gerencie seus leads")
        st.write("• **Performance de Vendas:** Analise o desempenho comercial")
        st.write("• **Pipeline:** Monitore seu funil de vendas")
        st.write("• **Análise RFV:** Analise Recência, Frequência e Valor dos clientes") 