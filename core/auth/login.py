import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def setup_login():
    # Estilo personalizado
    st.markdown("""
        <style>
        .stApp {
            background-color: #f0f2f6;
        }
        .login-container {
            max-width: 400px;
            margin: auto;
            padding: 2rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # Container de login
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Logo (opcional)
        # st.image("assets/images/logo.png", width=200)
        
        st.title("Empresamix Sistemas")
        st.subheader("Análise de Dados (BI)")

        # Credenciais temporárias
        credentials = {
            'usernames': {
                'admin': {
                    'name': 'Admin',
                    'password': stauth.Hasher(['admin']).generate()[0]
                }
            }
        }

        authenticator = stauth.Authenticate(
            credentials,
            'empresamix_cookie',
            'auth_key',
            cookie_expiry_days=30
        )

        name, authentication_status, username = authenticator.login('Login', 'main')

        if authentication_status == False:
            st.error('Usuário e/ou Senha incorretos')
        elif authentication_status == None:
            st.warning('Informe suas credenciais de acesso.')
        elif authentication_status:
            return True, username

        st.markdown('</div>', unsafe_allow_html=True)
        
    return False, None
