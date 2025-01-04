import streamlit as st
import plotly.express as px
from modules.comercial.services.data_service import get_pipeline_data

def render():
    """Renderiza o dashboard de pipeline."""
    st.title("Análise de Pipeline")
    
    # Carrega dados
    df = get_pipeline_data()
    
    # Métricas principais
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total em Pipeline", f"R$ {df['value'].sum():,.2f}")
    with col2:
        st.metric("Número de Oportunidades", f"{df['count'].sum():,}")
    
    # Gráfico de funil
    fig = px.funnel(
        df,
        x='value',
        y='stage',
        title='Funil de Vendas'
    )
    st.plotly_chart(fig, use_container_width=True) 