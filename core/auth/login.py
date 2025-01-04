import streamlit as st
import streamlit_authenticator as stauth
import time

def setup_login():
    # Evita loop infinito de redirecionamento
    if 'authentication_status' in st.session_state and st.session_state['authentication_status']:
        return True, st.session_state.get('username')

    # Container original do formulário
    with st.container():
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
            </style>
        """, unsafe_allow_html=True)

        st.title("Empresamix Sistemas")
        st.markdown('<p class="subtitle">Análise de Dados (BI)</p>', unsafe_allow_html=True)
        
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        
        if st.button("Login"):
            if username == "admin" and password == "admin":
                # Atualiza o estado da sessão
                st.session_state['authentication_status'] = True
                st.session_state['username'] = username
                
                st.success("Login realizado com sucesso! Redirecionando...")
                time.sleep(1)
                
                # Força o rerun da página atual
                st.rerun()
                
                return True, username
            else:
                st.error("Usuário e/ou Senha incorretos")
                return False, None
        
        if "authentication_status" not in st.session_state:
            st.warning("Informe suas credenciais de acesso.")
    
    return False, None