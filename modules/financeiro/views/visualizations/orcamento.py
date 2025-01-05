import streamlit as st
import plotly.express as px
from modules.financeiro.services.data_service import get_budget_data

def render():
    st.title("Orçamento")
    
    # Carrega dados
    df = get_budget_data()
    
    # Métricas principais
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Orçado", f"R$ {df['orcado'].sum():,.2f}")
    with col2:
        st.metric("Total Realizado", f"R$ {df['realizado'].sum():,.2f}")
    
    # Gráfico de barras
    fig = px.bar(
        df,
        x='departamento',
        y=['orcado', 'realizado'],
        title='Orçado vs Realizado por Departamento',
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True) 