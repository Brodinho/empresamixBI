import streamlit as st
from config.settings import APP_CONFIG
from utils.auth import check_authentication

def main():
    if check_authentication():
        st.success("Autenticado com sucesso!")
    else:
        st.error("Falha na autenticação")

if __name__ == "__main__":
    main()
