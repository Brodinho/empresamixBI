import streamlit as st
from modules.financeiro.services.data_service import get_indicators_data

def render():
    st.title("Indicadores Financeiros")
    
    # Carrega dados
    data = get_indicators_data()
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Liquidez Corrente", f"{data['liquidez_corrente']:.2f}")
    with col2:
        st.metric("Margem EBITDA", f"{data['margem_ebitda']:.1%}")
    with col3:
        st.metric("ROI", f"{data['roi']:.1%}") 