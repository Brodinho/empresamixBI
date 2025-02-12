import streamlit as st
import pandas as pd
import logging
from ..services.api_service import ComercialAPIService
from ..components.leads_analysis import LeadsAnalysis

logger = logging.getLogger(__name__)

def render_leads_dashboard():
    try:
        # Obtém dados combinados
        api_service = ComercialAPIService()
        df = api_service.get_leads_data()
        
        if df.empty:
            st.error("Não foi possível carregar os dados dos leads")
            return
            
        # Layout em colunas para métricas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Total de Leads
            total_leads = len(df)
            st.metric("Total de Leads", f"{total_leads:,}")
        
        with col2:
            # Leads Ativos
            leads_ativos = len(df[df['ativo'] == 1])
            percentual_ativos = (leads_ativos / total_leads * 100) if total_leads > 0 else 0
            st.metric("Leads Ativos", f"{leads_ativos:,}", 
                     f"{percentual_ativos:.1f}% do total")
        
        with col3:
            # Taxa de Conversão
            leads_convertidos = len(df[df['valorfaturado'].notna()])
            taxa_conversao = (leads_convertidos / total_leads * 100) if total_leads > 0 else 0
            st.metric("Taxa de Conversão", f"{taxa_conversao:.1f}%")
        
        # Linha divisória
        st.markdown("---")
        
        # Gráficos em duas colunas
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Funil de conversão
            leads_analysis = LeadsAnalysis()
            funnel_fig = leads_analysis.create_conversion_funnel(df)
            if funnel_fig:
                st.plotly_chart(funnel_fig, use_container_width=True)
            else:
                st.error("Erro ao gerar funil de conversão")
        
        with col_right:
            # Distribuição por região
            region_fig = leads_analysis.create_leads_by_region(df)
            if region_fig:
                st.plotly_chart(region_fig, use_container_width=True)
            else:
                st.error("Erro ao gerar gráfico de distribuição regional")
        
        # Tabela de leads
        st.markdown("### Lista de Leads")
        
        # Seleção de colunas relevantes
        columns_to_show = ['codcli', 'nome', 'cidade', 'uf', 'ativo', 'valorfaturado']
        df_display = df[columns_to_show].copy()
        
        # Formatação da tabela
        df_display['ativo'] = df_display['ativo'].map({1: 'Sim', 0: 'Não'})
        df_display['valorfaturado'] = df_display['valorfaturado'].fillna(0).map('R$ {:,.2f}'.format)
        
        # Exibe a tabela com paginação
        st.dataframe(df_display, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro ao renderizar dashboard de leads: {str(e)}")
        logger.error(f"Erro ao renderizar dashboard de leads: {str(e)}") 