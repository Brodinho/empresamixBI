import streamlit as st
import plotly.express as px
from modules.comercial.services.data_service import get_sales_data

def render():
    """Renderiza o dashboard de performance de vendas."""
    st.title("Performance de Vendas")
    
    # Carrega dados
    df = get_sales_data()
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Vendas Totais", f"R$ {df['revenue'].sum():,.2f}")
    with col2:
        st.metric("Média Diária", f"R$ {df['revenue'].mean():,.2f}")
    with col3:
        st.metric("Total de Clientes", f"{df['customers'].sum():,}")
    
    # Gráfico de vendas ao longo do tempo
    fig = px.line(df, x='date', y='revenue', title='Receita ao Longo do Tempo')
    st.plotly_chart(fig, use_container_width=True) 