import streamlit as st
from .views.visualizations.analise_territorial import render_analise_territorial
from .views.visualizations.leads import render_leads
from .views.visualizations.performance_vendas import render_performance
from .views.visualizations.performance_vendedores import render_performance_vendedores
from .views.visualizations.pipeline import render_pipeline
from .views.visualizations.rfv import render_rfv
from .views.visualizations.analise_producao import render_producao

def render_nav_button(label: str, is_active: bool = False, key: str = None) -> bool:
    """Renderiza um botão de navegação estilizado no sidebar"""
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
                transition: all 0.3s ease;
            }
            div[data-testid="stButton"] button:hover {
                border-color: #4CAF50;
                background-color: #2E2E2E;
            }
        </style>
    """ % ("#2E2E2E" if is_active else "#1E1E1E", "#4CAF50" if is_active else "#333")
    
    st.sidebar.markdown(button_style, unsafe_allow_html=True)
    return st.sidebar.button(label, key=key)

def render_comercial_module():
    """Renderiza o módulo comercial"""
    
    # Menu lateral
    st.sidebar.title("Navegação")
    
    # Estado da página atual
    current_page = st.session_state.get('comercial_page', 'welcome')
    
    # Botões de navegação
    if render_nav_button("📍 Análise Territorial", current_page == 'territorial', 'nav_territorial'):
        current_page = 'territorial'
        st.session_state.comercial_page = 'territorial'
        
    if render_nav_button("🎯 Leads", current_page == 'leads', 'nav_leads'):
        current_page = 'leads'
        st.session_state.comercial_page = 'leads'
        
    if render_nav_button("📊 Performance de Vendas", current_page == 'performance', 'nav_performance'):
        current_page = 'performance'
        st.session_state.comercial_page = 'performance'
        
    if render_nav_button("👥 Performance de Vendedores", current_page == 'vendedores', 'nav_vendedores'):
        current_page = 'vendedores'
        st.session_state.comercial_page = 'vendedores'
        
    if render_nav_button("🔄 Pipeline", current_page == 'pipeline', 'nav_pipeline'):
        current_page = 'pipeline'
        st.session_state.comercial_page = 'pipeline'
        
    if render_nav_button("💎 Análise RFV", current_page == 'rfv', 'nav_rfv'):
        current_page = 'rfv'
        st.session_state.comercial_page = 'rfv'
        
    # Novo botão para Análise de Produção
    if render_nav_button("🤝 Análise de Produção", current_page == 'producao', 'nav_producao'):
        current_page = 'producao'
        st.session_state.comercial_page = 'producao'
    
    # Renderiza o conteúdo baseado na página atual
    if current_page == 'territorial':
        render_analise_territorial()
    elif current_page == 'leads':
        render_leads()
    elif current_page == 'performance':
        render_performance()
    elif current_page == 'vendedores':
        render_performance_vendedores()
    elif current_page == 'pipeline':
        render_pipeline()
    elif current_page == 'rfv':
        render_rfv()
    elif current_page == 'producao':
        render_producao()
    else:
        # Mensagem de boas-vindas
        st.markdown("""
        ## Bem-vindo ao Módulo Comercial!
        
        Utilize o menu lateral para acessar os diferentes dashboards disponíveis:
        
        - **Análise Territorial**: Visualize a distribuição geográfica das vendas
        - **Leads**: Acompanhe e gerencie seus leads
        - **Performance de Vendas**: Analise o desempenho comercial
        - **Performance de Vendedores**: Analise o desempenho individual dos vendedores
        - **Pipeline**: Monitore seu funil de vendas
        - **Análise RFV**: Analise Recência, Frequência e Valor dos clientes
        - **Análise de Produção**: Acompanhe o fluxo e desempenho da produção
        """)