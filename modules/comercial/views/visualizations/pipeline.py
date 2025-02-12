import streamlit as st
import pandas as pd
from ...services.api_service import ComercialAPIService
from ...components.pipeline_analysis import PipelineAnalysis
from shared.utils.visualizations.insights_cards import render_metrics_section

def render_pipeline():
    """Renderiza o dashboard de Pipeline de Vendas"""
    try:
        # Obtém os dados
        api_service = ComercialAPIService()
        df = api_service.get_pipeline_data()
        
        # Título da seção
        st.markdown("## 📊 Pipeline de Vendas")
        
        # Expander explicativo
        with st.expander("ℹ️ Como interpretar o Pipeline?", expanded=False):
            st.markdown("""
                O **Pipeline de Vendas** mostra o fluxo de oportunidades através das diferentes 
                etapas do processo comercial. Ele ajuda a:
                
                - Visualizar o volume de negócios em cada etapa
                - Identificar gargalos no processo de vendas
                - Projetar receita potencial
                - Acompanhar o desempenho da equipe comercial
            """)
        
        # Configuração das métricas para os cards
        metrics = {
            'total_oportunidades': {
                'title': '📈 Total de Oportunidades',
                'value': len(df),
                'formatter': 'number',
                'help_text': 'Número total de oportunidades em todas as etapas do pipeline'
            },
            'valor_total': {
                'title': '💰 Valor Total Pipeline',
                'value': df['valor'].sum(),
                'formatter': 'currency',
                'help_text': 'Soma do valor de todas as oportunidades no pipeline',
                'positive_is_good': True
            },
            'ticket_medio': {
                'title': '🎯 Ticket Médio',
                'value': df['valor'].sum() / len(df) if len(df) > 0 else 0,
                'formatter': 'currency',
                'help_text': 'Valor médio das oportunidades no pipeline',
                'positive_is_good': True
            }
        }
        
        # Renderiza os cards de métricas
        render_metrics_section('', metrics, columns=3)
        
        # Separador
        st.markdown("---")
        
        # Gráficos do Pipeline
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Funil de Vendas por Status")
            fig_funil = PipelineAnalysis.create_funnel_chart(df)
            st.plotly_chart(fig_funil, use_container_width=True)
            
        with col2:
            st.markdown("### Valor Total por Status")
            fig_valor = PipelineAnalysis.create_value_by_status_chart(df)
            st.plotly_chart(fig_valor, use_container_width=True)
        
        # Segunda linha de gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Tendência de Conversão")
            fig_tendencia = PipelineAnalysis.create_conversion_trend_chart(df)
            st.plotly_chart(fig_tendencia, use_container_width=True)
            
        with col2:
            st.markdown("### Distribuição por Vendedor")
            fig_vendedor = PipelineAnalysis.create_sales_by_rep_chart(df)
            st.plotly_chart(fig_vendedor, use_container_width=True)
        
        # Tempo médio no pipeline
        st.markdown("### Tempo Médio por Etapa")
        fig_tempo = PipelineAnalysis.create_time_in_stage_chart(df)
        st.plotly_chart(fig_tempo, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro ao renderizar Pipeline: {str(e)}") 