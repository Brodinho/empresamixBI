"""
Dashboard de Análise RFV (Recência, Frequência, Valor)
"""
import streamlit as st
import pandas as pd
import logging
from modules.comercial.services import comercial_service
from shared.components.filters import DateFilters
from modules.comercial.components.grafico_recencia import criar_grafico_recencia
from modules.comercial.components.grafico_frequencia import criar_grafico_frequencia
from modules.comercial.components.grafico_valor import criar_grafico_valor
from datetime import datetime

logger = logging.getLogger(__name__)

def render_rfv():
    """Renderiza o dashboard de análise RFV"""
    try:
        st.title("💎 Análise RFV")
        
        # Filtros de data
        date_filters = DateFilters()
        anos_selecionados = date_filters.year_filter(key_suffix="rfv")
        
        # Carrega os dados usando a instância global
        df = comercial_service.get_dados_rfv(anos_selecionados)
        
        # Expander com explicação do RFV
        with st.expander("ℹ️ O que é análise RFV?"):
            st.markdown("""
                ### Análise RFV - Recência, Frequência e Valor
                
                A análise RFV é uma técnica de segmentação de clientes que considera três aspectos:
                
                - **Recência (R)** 📅: Há quanto tempo o cliente fez a última compra
                - **Frequência (F)** 🔄: Quantas vezes o cliente comprou
                - **Valor (V)** 💰: Quanto o cliente gastou no total
                
                Esta análise ajuda a identificar seus melhores clientes e oportunidades de negócio.
            """)
        
        if df is not None and not df.empty:
            # Layout em colunas para métricas principais
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="📅 Média de Recência",
                    value=f"{df['recencia'].mean():.0f} dias"
                )
                
            with col2:
                st.metric(
                    label="🔄 Média de Frequência",
                    value=f"{df['frequencia'].mean():.1f} compras"
                )
                
            with col3:
                st.metric(
                    label="💰 Ticket Médio",
                    value=f"R$ {df['valor'].mean():,.2f}"
                )
            
            # Gráficos
            st.subheader("Análise de Recência")
            criar_grafico_recencia(df)
            
            # Duas colunas para os outros gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Análise de Frequência")
                criar_grafico_frequencia(df)
                
            with col2:
                st.subheader("Análise de Valor")
                criar_grafico_valor(df)
        else:
            st.warning("Nenhum dado encontrado para o período selecionado.")
            
    except Exception as e:
        st.error('Erro ao renderizar dashboard RFV')
        logger.error(f'Erro na renderização: {str(e)}') 