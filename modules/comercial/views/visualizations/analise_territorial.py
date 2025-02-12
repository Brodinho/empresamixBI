"""
Dashboard de Análise Territorial
"""
import streamlit as st
import logging
import pandas as pd
from modules.comercial.services import comercial_service, ComercialAPIService
from shared.components.filters import DateFilters
from shared.utils.visualizations.insights_cards import render_metrics_section
from .territory_map import create_territory_map
from .region_ranking import create_region_ranking
from .client_distribution import create_client_distribution
from modules.comercial.components import TerritoryMap, RegionRanking, VendasPorRegiao
from modules.comercial.components.territory_treemap import criar_treemap_territorial

logger = logging.getLogger(__name__)

def render_analise_territorial():
    """Renderiza o dashboard de Análise Territorial"""
    try:
        logger.debug("=== Iniciando render_analise_territorial ===")
        st.title("Análise Territorial")     
        
        # Carrega dados
        logger.debug("Iniciando carregamento de dados...")
        api_service = ComercialAPIService()
        logger.debug("ComercialAPIService instanciado")
        
        df = api_service.get_data("CUBO_FATURAMENTO")
        logger.debug(f"Dados recebidos. DataFrame vazio? {df.empty}")
        
        if df.empty:
            logger.error("DataFrame vazio retornado pela API")
            st.error('Não foi possível carregar os dados.')
            return
            
        logger.debug(f"Colunas disponíveis: {df.columns.tolist()}")
        
        # Verifica se todas as colunas necessárias existem
        required_columns = ['codcli', 'uf', 'pais']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logger.error(f"Colunas ausentes: {missing_columns}")
            st.error('Dados incompletos. Algumas informações necessárias não estão disponíveis.')
            return
        
        # Definição de constantes
        TOTAL_ESTADOS_BR = 27
        TOTAL_PAISES_MUNDO = 195
        
        # Configuração das métricas para os cards
        metrics = {
            'total_clientes': {
                'title': 'Total de Clientes',
                'value': df['codcli'].nunique(),
                'formatter': 'number',
                'delta': 15.5,  # percentual de crescimento
                'help_text': 'Número total de clientes únicos atendidos no período'
            },
            'estados_atendidos': {
                'title': 'Estados Atendidos',
                'value': df[df['uf'] != 'EX']['uf'].nunique(),
                'formatter': 'number',
                'delta': round((df[df['uf'] != 'EX']['uf'].nunique() / TOTAL_ESTADOS_BR * 100), 1),
                'help_text': 'Número e percentual de estados brasileiros com clientes ativos'
            },
            'paises_atendidos': {
                'title': 'Países Atendidos',
                'value': df[df['uf'] == 'EX']['pais'].nunique(),
                'formatter': 'number',
                'delta': round((df[df['uf'] == 'EX']['pais'].nunique() / TOTAL_PAISES_MUNDO * 100), 1),
                'help_text': 'Número e percentual de países estrangeiros com clientes ativos'
            },
            'clientes_externos': {
                'title': 'Clientes Externos',
                'value': df[df['uf'] == 'EX']['codcli'].nunique(),
                'formatter': 'number',
                'delta': round((df[df['uf'] == 'EX']['codcli'].nunique() / df['codcli'].nunique() * 100), 1),
                'help_text': 'Número e percentual de clientes em outros países'
            }
        }
        
        # Renderiza a seção de métricas
        render_metrics_section('', metrics, columns=4)
        
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
                
        # Título e Expander explicativo
        st.markdown("### 📊 Distribuição Territorial")
        with st.expander("ℹ️ Como interpretar este gráfico?"):
            st.markdown("""
            Este gráfico mostra a distribuição geográfica das vendas:
            
            📂 Níveis: Região > Estado > Cidade
            🎨 Cores: Quanto mais escuro, maior o valor
            📊 Tamanho: Proporcional ao valor faturado
            
            % do Total representa:
            • Região: % do faturamento total
            • Estado: % do total da região
            • Cidade: % do total do estado
            
            💡 Dica: Identifique regiões com maior potencial e oportunidades de expansão territorial.
            """)

        # Adiciona os filtros em colunas
        col1, col2 = st.columns(2)
        with col1:
            metrica = st.selectbox(
                "Métrica de Análise",
                options=["Valor Faturado", "Quantidade", "Número de Clientes"],
                key="treemap_metric",
                help="Escolha a métrica para análise no treemap"
            )

        with col2:
            nivel_detalhe = st.selectbox(
                "Nível de Detalhe",
                options=["Região > Estado", "Estado > Cidade", "Região > Estado > Cidade"],
                key="treemap_detail",
                help="Escolha o nível de detalhamento da análise"
            )

        # Cria um container vazio para o gráfico
        chart_container = st.empty()

        # Cria o treemap com os parâmetros selecionados
        try:
            print(f"Criando treemap com métrica: {metrica} e nível: {nivel_detalhe}")
            
            treemap = criar_treemap_territorial(
                df=df,
                metrica=metrica,
                nivel_detalhe=nivel_detalhe
            )
            
            if treemap:
                # Usa o container vazio para mostrar o gráfico
                with chart_container:
                    st.plotly_chart(treemap, use_container_width=True)
            else:
                st.error('Erro ao criar análise territorial')
        except Exception as e:
            st.error('Erro ao criar análise territorial')
            logger.error(f'Erro no treemap: {str(e)}')
                
    except Exception as e:
        logger.error(f"Erro na renderização de Análise Territorial: {str(e)}")
        st.error('Erro ao renderizar dashboard') 