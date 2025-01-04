import streamlit as st
import plotly.express as px
from modules.comercial.services.data_service import get_territory_data

def render():
    """Renderiza o dashboard de território."""
    st.title("Análise de Território")
    
    # Carrega dados
    df = get_territory_data()
    
    # Métricas principais
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Vendas", f"R$ {df['sales'].sum():,.2f}")
    with col2:
        st.metric("Market Share Médio", f"{df['market_share'].mean():.1%}")
    
    # Gráfico de barras
    fig = px.bar(
        df,
        x='region',
        y='sales',
        title='Vendas por Região'
    )
    st.plotly_chart(fig, use_container_width=True) 