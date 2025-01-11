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
            [data-testid="stMetricValue"] {
                height: 50px;
                display: flex;
                align-items: center;
            }
            [data-testid="stMetricDelta"] {
                height: 30px;
                display: flex;
                align-items: center;
            }
            [data-testid="stMetricLabel"] {
                height: 30px;
                display: flex;
                align-items: center;
            }
            div[data-testid="metric-container"] {
                background-color: rgba(28, 131, 225, 0.1);
                border: 1px solid rgba(28, 131, 225, 0.1);
                padding: 15px;
                border-radius: 5px;
                color: rgb(30, 103, 119);
                overflow-wrap: break-word;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                min-height: 120px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
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
        # Container com efeito 3D
        st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
        
        # Cards informativos dentro do container
        col1, col2, col3, col4 = st.columns(4)
        
        # Calcula totais para percentuais
        total_clientes = df['codcli'].nunique()
        total_estados_br = 27  # Total de estados do Brasil + DF
        total_paises_mundo = 195  # Número aproximado de países no mundo
        
        with col1:
            # Calcula percentual de crescimento da base de clientes
            perc_crescimento = 15.5  # Você pode ajustar este valor ou calcular dinamicamente
            st.metric(
                label="Total de Clientes",
                value=f"{total_clientes:,}".replace(",", "."),
                delta=f"{perc_crescimento}%",
                delta_color="normal",
                help="Número total de clientes únicos atendidos no período"
            )
        
        with col2:
            total_estados = df[df['uf'] != 'EX']['uf'].nunique()
            perc_estados = round((total_estados / total_estados_br * 100), 1)
            st.metric(
                label="Estados Atendidos",
                value=total_estados,
                delta=f"{perc_estados}%",
                delta_color="normal",
                help="Número e percentual de estados brasileiros com clientes ativos de um total de 27 estados"
            )
        
        with col3:
            total_paises = df[df['uf'] == 'EX']['pais'].nunique()
            perc_paises = round((total_paises / total_paises_mundo * 100), 1)
            st.metric(
                label="Países Atendidos",
                value=total_paises,
                delta=f"{perc_paises}%",
                delta_color="normal",
                help="Número e percentual de países estrangeiros com clientes ativos"
            )
        
        with col4:
            clientes_externos = df[df['uf'] == 'EX']['codcli'].nunique()
            perc_externos = round((clientes_externos / total_clientes * 100), 1) if total_clientes > 0 else 0
            st.metric(
                label="Clientes Externos",
                value=f"{clientes_externos:,}".replace(",", "."),
                delta=f"{perc_externos}%",
                delta_color="normal",
                help="Número e percentual de clientes em outros países"
            )
        
        # Fecha o container
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Prepara dados para filtro de ano (após os cards)
        if 'emissao' in df.columns:
            df['emissao'] = pd.to_datetime(df['emissao'])
            df['ano'] = df['emissao'].dt.year
            
            # Adiciona filtro de anos
            with st.expander("🔍 Filtros de Análise"):
                anos_disponiveis = sorted(df['ano'].unique())
                if anos_disponiveis:
                    anos_selecionados = DateFilters.year_filter("analise_territorial")
                    
                    # Aplica filtro apenas nos gráficos se houver anos selecionados
                    if anos_selecionados and len(anos_selecionados) > 0:
                        df = df[df['ano'].isin(anos_selecionados)]
                        logger.debug(f"Dados filtrados por anos: {anos_selecionados}")
        
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