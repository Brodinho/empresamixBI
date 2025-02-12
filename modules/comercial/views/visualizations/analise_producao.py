import streamlit as st
from ...services.api_service import APIService
from ...services.kpi_service import KPIService
from shared.utils.visualizations.insights_cards import render_metrics_section
from .os_status_chart import create_os_status_chart
from .os_tempo_medio_chart import create_os_tempo_medio_chart
from .os_gargalos_chart import create_os_gargalos_chart
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def render_producao():
    """Renderiza o dashboard de Análise de Produção"""
    
    # Título da seção com ícone e texto maiores
    st.markdown("# 🤝 Análise de Produção")
    
    # Expander explicativo
    with st.expander("ℹ️ Como interpretar a Análise de Produção?", expanded=False):
        st.markdown("""
            A **Análise de Produção** permite acompanhar o fluxo produtivo através de:
            
            - Status atual das Ordens de Serviço
            - Tempo médio em cada etapa do processo
            - Identificação de gargalos
            - Análise de capacidade produtiva
            - Tendências de produção
        """)
    
    try:
        # Carrega dados uma única vez e mantém em cache
        @st.cache_data(ttl=3600)
        def load_initial_data():
            api_service = APIService()
            return api_service.get_all_data()
        
        # Carrega dados iniciais
        dataframes = load_initial_data()
        
        # Prepara todos os dataframes necessários
        df_os = dataframes['os'].copy()
        df_orcamento = dataframes['orcamento'].copy()
        df_faturamento = dataframes['faturamento'].copy()
        
        # Converte datas em todos os dataframes
        df_os['data'] = pd.to_datetime(df_os['data'], format='%Y-%m-%d', errors='coerce')
        df_orcamento['data'] = pd.to_datetime(df_orcamento['data'], format='%Y-%m-%d', errors='coerce')
        df_faturamento['data'] = pd.to_datetime(df_faturamento['data'], format='%Y-%m-%d', errors='coerce')
        
        # Remove registros sem data
        df_os = df_os.dropna(subset=['data'])
        df_orcamento = df_orcamento.dropna(subset=['data'])
        df_faturamento = df_faturamento.dropna(subset=['data'])
        
        # Calcula o intervalo dos últimos 5 anos
        ano_atual = datetime.now().year
        data_inicial = datetime(ano_atual - 4, 1, 1)
        
        # Adiciona coluna de ano em todos os dataframes
        df_os['ano'] = df_os['data'].dt.year
        df_orcamento['ano'] = df_orcamento['data'].dt.year
        df_faturamento['ano'] = df_faturamento['data'].dt.year
        
        # Filtra os dados para os últimos 5 anos
        df_os_filtrado = df_os[df_os['data'] >= data_inicial].copy()
        df_orcamento_filtrado = df_orcamento[df_orcamento['data'] >= data_inicial].copy()
        df_faturamento_filtrado = df_faturamento[df_faturamento['data'] >= data_inicial].copy()
        
        # Expander com filtros
        with st.expander("🔍 Filtros de Análise"):
            anos_disponiveis = sorted(df_os_filtrado['ano'].unique())
            if anos_disponiveis:
                opcoes_anos = ['Todos'] + [str(ano) for ano in anos_disponiveis]
                anos_selecionados = st.multiselect(
                    "Selecione os anos:",
                    options=opcoes_anos,
                    default=[],  # Remove o default
                    key="filtro_anos_producao"
                )
        
        # Só mostra dados se algum ano for selecionado (incluindo "Todos")
        if anos_selecionados:
            # Se "Todos" estiver selecionado, usa todos os anos disponíveis
            if 'Todos' in anos_selecionados:
                anos_numericos = [int(ano) for ano in anos_disponiveis]
            else:
                anos_numericos = [int(ano) for ano in anos_selecionados]
            
            df_os_filtrado = df_os_filtrado[df_os_filtrado['ano'].isin(anos_numericos)]
            df_orcamento_filtrado = df_orcamento_filtrado[df_orcamento_filtrado['ano'].isin(anos_numericos)]
            df_faturamento_filtrado = df_faturamento_filtrado[df_faturamento_filtrado['ano'].isin(anos_numericos)]
            
            # Atualiza todos os dataframes filtrados
            dataframes_filtrados = {
                'os': df_os_filtrado,
                'orcamento': df_orcamento_filtrado,
                'faturamento': df_faturamento_filtrado
            }
            
            # Calcula KPIs com os dados filtrados
            kpi_service = KPIService(dataframes_filtrados)
            kpis = kpi_service.calcular_kpis_producao()
            
            # Renderiza cards de métricas
            metrics = {
                'taxa_aprovacao': {
                    'title': 'Taxa de Aprovação',
                    'value': kpis['taxa_conversao'],
                    'formatter': 'percentage',
                    'help_text': 'Percentual de orçamentos convertidos em OS',
                    'positive_is_good': True,
                    'decimals': 1
                },
                'tempo_orc_os': {
                    'title': 'Tempo Médio Orç → OS',
                    'value': kpis['tempo_medio_orc_os'],
                    'suffix': ' dias',
                    'help_text': 'Tempo médio entre orçamento e abertura de OS',
                    'positive_is_good': False,
                    'decimals': 1
                },
                'tempo_os_fat': {
                    'title': 'Tempo Médio OS → Fat',
                    'value': kpis['tempo_medio_os_fat'],
                    'suffix': ' dias',
                    'help_text': 'Tempo médio entre OS e faturamento',
                    'positive_is_good': False,
                    'decimals': 1
                },
                'valor_medio_aprov': {
                    'title': 'Valor Médio Aprovados',
                    'value': kpis['valor_medio_aprovados'],
                    'formatter': 'currency',
                    'help_text': 'Valor médio dos orçamentos aprovados',
                    'positive_is_good': True
                },
                'perc_fat_os': {
                    'title': '% Faturamento via OS',
                    'value': kpis['perc_faturamento_os'],
                    'formatter': 'percentage',
                    'help_text': 'Percentual do faturamento gerado via OS',
                    'positive_is_good': True,
                    'decimals': 1
                }
            }
            
            render_metrics_section("Indicadores de Produção", metrics, columns=5)
            
            # Cria e exibe o gráfico de status
            st.markdown("### Status das Ordens de Serviço")
            fig_status = create_os_status_chart(df_os_filtrado)
            if fig_status:
                st.plotly_chart(fig_status, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de status das OS')
            
            # Cria e exibe o gráfico de tempo médio
            st.markdown("### Tempo Médio em cada Etapa")
            
            # Expander explicativo do gráfico de tempo médio
            with st.expander("ℹ️ Como interpretar o Tempo Médio?"):
                st.markdown("""
                    O gráfico de **Tempo Médio em cada Etapa** apresenta a média de dias desde a abertura da OS até o momento atual, agrupado por status. 
                    
                    **Como é calculado:**
                    - Tempo = Data Atual - Data de Abertura da OS
                    - Os tempos são agrupados por status atual da OS
                    - É calculada a média de tempo para cada status
                    
                    **Como analisar:**
                    1. **Gargalos**: Status com tempo médio elevado podem indicar gargalos no processo
                    2. **Eficiência**: Compare os tempos entre diferentes períodos para avaliar melhorias
                    3. **Metas**: Use como referência para estabelecer tempos-alvo totais
                    4. **Priorização**: Identifique quais status precisam de atenção imediata
                    
                    **Dicas de interpretação:**
                    - O tempo mostrado é o total desde a abertura da OS, não apenas o tempo no status atual
                    - OS's faturadas tendem a mostrar tempos maiores por representarem o ciclo completo
                    - OS's em status iniciais tendem a mostrar tempos menores por serem mais recentes
                    - Considere fatores sazonais que podem impactar os tempos médios
                """)
            
            fig_tempo = create_os_tempo_medio_chart(df_os_filtrado)
            if fig_tempo:
                st.plotly_chart(fig_tempo, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de tempo médio das OS')

            # Cria e exibe o gráfico de gargalos
            st.markdown("### Gargalos de Produção")
            
            # Expander explicativo do gráfico de gargalos
            with st.expander("ℹ️ Como interpretar os Gargalos de Produção?"):
                st.markdown("""
                    O gráfico de **Gargalos de Produção** apresenta o fluxo acumulado de OS's através das diferentes etapas do processo produtivo.
                    
                    **Como é calculado:**
                    - Cada nível mostra a quantidade total de OS's que passaram ou estão em cada status
                    - As porcentagens indicam a taxa de conversão entre etapas sucessivas
                    - A largura das barras representa o volume acumulado em cada etapa
                    
                    **Como analisar:**
                    1. **Volume Total**: A primeira barra (Abertas) mostra o total de OS's no sistema
                    2. **Progressão**: Cada etapa mostra quantas OS's chegaram até ali
                    3. **Conversão**: A diferença entre etapas mostra quantas OS's ainda não avançaram
                    4. **Eficiência**: Quedas acentuadas indicam possíveis gargalos no processo
                    
                    **Dicas de interpretação:**
                    - OS's canceladas não são incluídas para não distorcer a análise do fluxo
                    - Uma queda suave entre etapas indica um processo equilibrado
                    - Quedas bruscas indicam acúmulo de OS's naquela etapa
                    - Compare os volumes entre períodos para identificar tendências
                """)
            
            fig_gargalos = create_os_gargalos_chart(df_os_filtrado)
            if fig_gargalos:
                st.plotly_chart(fig_gargalos, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de gargalos de produção')
        else:
            st.info("👆 Selecione um período para visualizar os dados")
            
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {str(e)}")
        st.error(f"Erro ao carregar dados: {str(e)}")
        st.info("Dashboard em desenvolvimento...") 