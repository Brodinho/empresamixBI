import streamlit as st
import streamlit_authenticator as stauth

def setup_login():
    # Estilo com foco no container e centralização
    st.markdown("""
        <style>
        /* Fundo principal */
        .stApp {
            background-color: #0A192F !important;
        }
        
        /* Container principal */
        .block-container {
            max-width: 500px !important;
            padding-top: 2rem !important;
        }
        
        /* Inputs */
        .stTextInput > div > div > input {
            background-color: #1E3A8A !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 12px !important;
            height: 40px !important;
            font-size: 14px !important;
        }
        
        /* Botão */
        .stButton > button {
            background-color: #1E88E5 !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 16px !important;
            width: 100% !important;
            margin-top: 1rem !important;
        }
        
        /* Títulos */
        h1 {
            font-size: 24px !important;
            font-weight: bold !important;
            text-align: center !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        
        /* Subtítulo */
        .subtitle {
            font-size: 14px !important;
            color: #A8B2D1 !important;
            text-align: center !important;
            margin-bottom: 2rem !important;
        }
        
        /* Mensagem de aviso */
        .stAlert {
            background-color: rgba(47, 69, 92, 0.7) !important;
            color: white !important;
        }
        
        /* Remove elementos desnecessários */
        #MainMenu, footer {
            visibility: hidden !important;
        }
        
        /* Ajusta espaçamento dos labels */
        .stTextInput > label {
            font-size: 14px !important;
            margin-bottom: 4px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Empresamix Sistemas")
    st.markdown('<p class="subtitle">Análise de Dados (BI)</p>', unsafe_allow_html=True)
    
    # Formulário
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state["authentication_status"] = True
            st.session_state["username"] = username
            st.switch_page("Home.py")
            return True, username
        else:
            st.error("Usuário e/ou Senha incorretos")
            return False, None
    
    if "authentication_status" not in st.session_state:
        st.warning("Informe suas credenciais de acesso.")
    
    return False, None
