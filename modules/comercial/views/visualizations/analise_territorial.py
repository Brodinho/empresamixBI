"""
Dashboard de Análise Territorial
"""
import streamlit as st
import logging
import pandas as pd
from modules.comercial.services import comercial_service
from shared.components.filters import DateFilters
from .territory_map import create_territory_map
from .region_ranking import create_region_ranking

logger = logging.getLogger(__name__)

def render_analise_territorial():
    """Renderiza o dashboard de análise territorial"""
    st.title("Análise Territorial")
    
    # Carrega dados
    df = comercial_service.get_data()
    if df is None:
        st.error('Não foi possível carregar os dados.')
        return
    
    try:
        # Prepara dados para filtro de ano
        if 'emissao' in df.columns:
            df['emissao'] = pd.to_datetime(df['emissao'])
            df['ano'] = df['emissao'].dt.year
        
        # Adiciona filtro de anos
        with st.expander("🔍 Filtros de Análise"):
            anos_disponiveis = sorted(df['ano'].unique()) if 'ano' in df.columns else []
            if anos_disponiveis:
                anos_selecionados = DateFilters.year_filter("analise_territorial")
                
                # Filtra dados por ano
                if anos_selecionados:
                    df = df[df['ano'].isin(anos_selecionados)]
                    logger.debug(f"Dados filtrados por anos: {anos_selecionados}")
        
        # Layout em duas colunas
        col1, col2 = st.columns([2, 1])
        
        with col1:
            try:
                territory_map = create_territory_map(df)
                if territory_map:
                    st.plotly_chart(territory_map, use_container_width=True)
                else:
                    st.error('Erro ao criar mapa territorial')
            except Exception as e:
                st.error('Erro ao criar mapa territorial')
                logger.error(f'Erro no mapa: {str(e)}')
        
        with col2:
            try:
                region_ranking = create_region_ranking(df)
                if region_ranking:
                    st.plotly_chart(region_ranking, use_container_width=True)
                else:
                    st.error('Erro ao criar ranking de regiões')
            except Exception as e:
                st.error('Erro ao criar ranking de regiões')
                logger.error(f'Erro no ranking: {str(e)}')
                
    except Exception as e:
        st.error('Erro ao renderizar dashboard')
        logger.error(f'Erro na renderização: {str(e)}') 