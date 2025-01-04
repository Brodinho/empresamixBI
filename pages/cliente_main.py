import streamlit as st

# Configuração da página DEVE ser a primeira chamada Streamlit
st.set_page_config(
    page_title="Módulo Cliente",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Remove elementos padrão do Streamlit
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Estilo para o sidebar */
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        
        /* Estilo para botões do sidebar */
        .stButton button {
            width: 100%;
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 0.5rem 1rem;
            margin: 0.5rem 0;
            border-radius: 0.5rem;
            color: white;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.3);
            transform: translateX(5px);
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar personalizado
with st.sidebar:
    # Título do módulo
    st.title("👥 Módulo Cliente")
    st.markdown("---")
    
    # Botões de navegação
    dashboards = {
        "😊 Satisfação do Cliente": "satisfacao",
        "📉 Análise de Churn": "churn",
        "👥 Segmentação de Clientes": "segmentacao",
        "🛣️ Jornada do Cliente": "jornada"
    }
    
    # Variável para controlar o dashboard ativo
    if 'current_dashboard' not in st.session_state:
        st.session_state.current_dashboard = 'satisfacao'
    
    # Criar botões
    for label, dashboard_id in dashboards.items():
        if st.button(
            label,
            key=f"btn_{dashboard_id}",
            use_container_width=True,
            type="primary" if st.session_state.current_dashboard == dashboard_id else "secondary"
        ):
            st.session_state.current_dashboard = dashboard_id

# Área principal
st.title("👥 Dashboard Cliente")

# Renderiza o dashboard selecionado
current = st.session_state.current_dashboard
if current == "satisfacao":
    st.write("Dashboard de Satisfação do Cliente")
elif current == "churn":
    st.write("Dashboard de Análise de Churn")
elif current == "segmentacao":
    st.write("Dashboard de Segmentação de Clientes")
elif current == "jornada":
    st.write("Dashboard de Jornada do Cliente") 