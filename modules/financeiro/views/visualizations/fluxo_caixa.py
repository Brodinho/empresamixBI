import streamlit as st
import plotly.express as px
from modules.financeiro.services.data_service import get_cashflow_data

def render():
    st.title("Fluxo de Caixa")
    
    # Carrega dados
    df = get_cashflow_data()
    
    # Métricas principais
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Receitas", f"R$ {df['receitas'].sum():,.2f}")
    with col2:
        st.metric("Total Despesas", f"R$ {df['despesas'].sum():,.2f}")
    
    # Gráfico de linha
    fig = px.line(
        df,
        x='date',
        y=['receitas', 'despesas'],
        title='Fluxo de Caixa Diário'
    )
    st.plotly_chart(fig, use_container_width=True) 