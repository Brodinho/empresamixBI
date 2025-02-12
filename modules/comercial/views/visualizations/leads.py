import streamlit as st
import pandas as pd
import logging
from ...services.api_service import ComercialAPIService
from ...components.leads_analysis import LeadsAnalysis
from shared.utils.visualizations.insights_cards import render_metrics_section

logger = logging.getLogger(__name__)

def render_leads():
    """Renderiza a visualização de análise de leads"""
    try:
        # Obtém os dados
        api_service = ComercialAPIService()
        df = api_service.get_leads_data()
        
        # Calcula as métricas
        total_leads = len(df)
        leads_ativos = len(df[df['ativo'] == 1])
        taxa_conversao = (leads_ativos/total_leads*100) if total_leads > 0 else 0
        
        # Configuração das métricas para os cards
        metrics = {
            'total_leads': {
                'title': 'Total de Leads',
                'value': total_leads,
                'formatter': 'number',
                'help_text': 'Número total de leads cadastrados no sistema, incluindo ativos e inativos'
            },
            'leads_ativos': {
                'title': 'Leads Ativos',
                'value': leads_ativos,
                'formatter': 'number',
                'help_text': 'Quantidade de leads atualmente ativos e em processo de negociação'
            },
            'taxa_conversao': {
                'title': 'Taxa de Conversão',
                'value': taxa_conversao,
                'formatter': 'percentage',
                'decimals': 1,
                'help_text': 'Percentual de leads que foram convertidos em clientes ativos',
                'positive_is_good': True
            }
        }
        
        # Renderiza os cards de métricas
        render_metrics_section('', metrics, columns=3)
        
        # Gráficos
        st.markdown("---")
        
        # Funil de Conversão
        with st.expander("ℹ️ Como interpretar o funil", expanded=False):
            st.markdown("""
                O **Funil de Conversão** mostra a progressão dos leads em cada etapa do processo.
            """)
        
        fig_funnel = LeadsAnalysis.create_conversion_funnel(df)
        if fig_funnel:
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        # Distribuição por Estado
        with st.expander("ℹ️ Como interpretar o gráfico", expanded=False):
            st.markdown("""
                A **Distribuição por Estado** mostra como os leads estão distribuídos geograficamente.
            """)
        
        fig_region = LeadsAnalysis.create_leads_by_region(df)
        if fig_region:
            st.plotly_chart(fig_region, use_container_width=True)
            
    except Exception as e:
        st.error(f"Erro ao renderizar análise de leads: {str(e)}")
        logger.error(f"Erro ao renderizar análise de leads: {str(e)}") 