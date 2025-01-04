import streamlit as st
import plotly.express as px
import pandas as pd
from modules.comercial.services.data_service import get_sales_data
from shared.utils.formatters import format_currency, format_percentage

def render():
    st.title("Performance de Vendas")
    
    # Carregando dados
    try:
        df = get_sales_data()
        
        # Layout em colunas para KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Receita Total",
                format_currency(df['receita'].sum()),
                format_percentage(df['crescimento_mom'])
            )
            
        with col2:
            st.metric(
                "Ticket Médio",
                format_currency(df['ticket_medio'].mean()),
                format_percentage(df['variacao_ticket'])
            )
            
        # Gráficos
        st.subheader("Distribuição Regional de Faturamento")
        fig_map = px.scatter_mapbox(
            df,
            lat='latitude',
            lon='longitude',
            size='receita',
            color='regiao',
            hover_name='cidade',
            zoom=4
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Mais gráficos...
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}") 