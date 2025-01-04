import streamlit as st
import plotly.express as px
from modules.comercial.services.data_service import get_leads_data

def render():
    """Renderiza o dashboard de leads."""
    st.title("Gestão de Leads/Oportunidades")
    
    # Carrega dados
    df = get_leads_data()
    
    # Métricas principais
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Leads", f"{len(df):,}")
    with col2:
        st.metric("Valor Total", f"R$ {df['value'].sum():,.2f}")
    
    # Gráfico de status
    fig = px.pie(
        df,
        names='status',
        title='Distribuição por Status'
    )
    st.plotly_chart(fig, use_container_width=True) 