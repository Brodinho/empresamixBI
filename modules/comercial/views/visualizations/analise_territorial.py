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
from .client_distribution import create_client_distribution
from modules.comercial.components import TerritoryMap, RegionRanking, VendasPorRegiao

logger = logging.getLogger(__name__)

def render_analise_territorial():
    """Renderiza o dashboard de análise territorial"""
    try:
        st.title("Análise Territorial")
        
        # Carrega dados primeiro
        df = comercial_service.get_data()
        if df is None:
            logger.error("Dados não carregados em Análise Territorial")
            st.error('Não foi possível carregar os dados.')
            return
        
        # Definição de constantes
        TOTAL_ESTADOS_BR = 27
        TOTAL_PAISES_MUNDO = 195
        
        # Container para as métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            perc_crescimento = 15.5
            st.metric(
                label="Total de Clientes",
                value=f"{df['codcli'].nunique():,}".replace(",", "."),
                delta=f"{perc_crescimento}%",
                help="Número total de clientes únicos atendidos no período"
            )
        
        with col2:
            total_estados = df[df['uf'] != 'EX']['uf'].nunique()
            perc_estados = round((total_estados / TOTAL_ESTADOS_BR * 100), 1)
            st.metric(
                label="Estados Atendidos",
                value=total_estados,
                delta=f"{perc_estados}%",
                delta_color="normal",
                help="Número e percentual de estados brasileiros com clientes ativos"
            )
        
        with col3:
            total_paises = df[df['uf'] == 'EX']['pais'].nunique()
            perc_paises = round((total_paises / TOTAL_PAISES_MUNDO * 100), 1)
            st.metric(
                label="Países Atendidos",
                value=total_paises,
                delta=f"{perc_paises}%",
                delta_color="normal",
                help="Número e percentual de países estrangeiros com clientes ativos"
            )
        
        with col4:
            total_clientes = df['codcli'].nunique()
            clientes_externos = df[df['uf'] == 'EX']['codcli'].nunique()
            perc_externos = round((clientes_externos / total_clientes * 100), 1) if total_clientes > 0 else 0
            st.metric(
                label="Clientes Externos",
                value=f"{clientes_externos:,}".replace(",", "."),
                delta=f"{perc_externos}%",
                delta_color="normal",
                help="Número e percentual de clientes em outros países"
            )
        
        # Filtros após as métricas
        with st.expander("🔍 Filtros de Análise"):
            if 'emissao' in df.columns:
                df['emissao'] = pd.to_datetime(df['emissao'])
                df['ano'] = df['emissao'].dt.year
                
                anos_disponiveis = sorted(df['ano'].unique())
                if anos_disponiveis:
                    anos_selecionados = DateFilters.year_filter("analise_territorial")
                    
                    if anos_selecionados and len(anos_selecionados) > 0:
                        df = df[df['ano'].isin(anos_selecionados)]
        
        # Separador visual
        st.markdown("---")
        
        # Layout dos gráficos
        col_map, col_rank = st.columns([2, 1])
        
        with col_map:
            try:
                territory_map = create_territory_map(df)
                if territory_map:
                    st.plotly_chart(territory_map, use_container_width=True)
                else:
                    st.error('Erro ao criar mapa territorial')
            except Exception as e:
                st.error('Erro ao criar mapa territorial')
                logger.error(f'Erro no mapa: {str(e)}')
        
        with col_rank:
            try:
                region_ranking = create_region_ranking(df)
                if region_ranking:
                    st.plotly_chart(region_ranking, use_container_width=True)
                else:
                    st.error('Erro ao criar ranking de regiões')
            except Exception as e:
                st.error('Erro ao criar ranking de regiões')
                logger.error(f'Erro no ranking: {str(e)}')
        
        # Adiciona o novo gráfico de distribuição de clientes
        st.markdown("---")  # Separador visual
        try:
            client_dist = create_client_distribution(df)
            if client_dist:
                st.plotly_chart(client_dist, use_container_width=True)
            else:
                st.error('Erro ao criar distribuição de clientes')
        except Exception as e:
            st.error('Erro ao criar distribuição de clientes')
            logger.error(f'Erro na distribuição: {str(e)}')
                
        # Após o último gráfico existente, adicionamos apenas:
        st.markdown("---")  # Separador visual
        try:
            vendas_regiao = VendasPorRegiao.create_sales_region_chart(df)
            if vendas_regiao:
                st.plotly_chart(vendas_regiao, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de vendas por região')
        except Exception as e:
            st.error('Erro ao criar gráfico de vendas por região')
            logger.error(f'Erro nas vendas por região: {str(e)}')
                
    except Exception as e:
        logger.error(f"Erro na renderização de Análise Territorial: {str(e)}")
        st.error('Erro ao renderizar dashboard') 