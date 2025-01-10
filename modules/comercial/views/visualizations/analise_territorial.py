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

logger = logging.getLogger(__name__)

def render_analise_territorial():
    """Renderiza o dashboard de análise territorial"""
    st.title("Análise Territorial")
    
    # CSS personalizado para os cards e container
    st.markdown("""
        <style>
            .metrics-container {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            div[data-testid="metric-container"] {
                background-color: rgba(28, 131, 225, 0.1);
                border: 1px solid rgba(28, 131, 225, 0.1);
                padding: 5% 5% 5% 10%;
                border-radius: 5px;
                color: rgb(30, 103, 119);
                overflow-wrap: break-word;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            div[data-testid="metric-container"]:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            }
            div[data-testid="metric-container"] > label {
                color: rgb(30, 103, 119);
                font-size: 1rem;
                font-weight: 500;
            }
            div[data-testid="metric-container"] > div {
                font-size: 1.5rem;
                font-weight: 600;
            }
            .stMetric {
                background-color: rgba(28, 131, 225, 0.1);
                border-radius: 5px;
                padding: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)
    
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
        
        # Container com efeito 3D
        st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
        
        # Cards informativos dentro do container
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_clientes = df['codcli'].nunique()
            st.metric(
                label="Total de Clientes",
                value=f"{total_clientes:,}".replace(",", "."),
                help="Número total de clientes únicos atendidos no período"
            )
        
        with col2:
            total_estados = df[df['uf'] != 'EX']['uf'].nunique()
            st.metric(
                label="Estados Atendidos",
                value=total_estados,
                help="Número de estados brasileiros com clientes ativos"
            )
        
        with col3:
            total_paises = df[df['uf'] == 'EX']['pais'].nunique()
            st.metric(
                label="Países Atendidos",
                value=total_paises,
                help="Número de países estrangeiros com clientes ativos"
            )
        
        with col4:
            clientes_externos = df[df['uf'] == 'EX']['codcli'].nunique()
            perc_externos = round((clientes_externos / total_clientes * 100), 1)
            st.metric(
                label="Clientes Externos",
                value=f"{clientes_externos:,}".replace(",", "."),
                delta=f"{perc_externos}%",
                help="Número e percentual de clientes em outros países"
            )
        
        # Fecha o container
        st.markdown('</div>', unsafe_allow_html=True)
        
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
                
    except Exception as e:
        st.error('Erro ao renderizar dashboard')
        logger.error(f'Erro na renderização: {str(e)}') 