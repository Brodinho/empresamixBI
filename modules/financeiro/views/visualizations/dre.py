import streamlit as st
import plotly.express as px
from modules.financeiro.services.data_service import get_dre_data

def render():
    st.title("DRE")
    
    # Carrega dados
    df = get_dre_data()
    
    # Gráfico de barras
    fig = px.bar(
        df,
        x='conta',
        y='valor',
        title='Demonstração do Resultado'
    )
    st.plotly_chart(fig, use_container_width=True) 