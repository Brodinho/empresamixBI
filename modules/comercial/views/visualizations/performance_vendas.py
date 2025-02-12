"""
Dashboard de Performance de Vendas
"""
import streamlit as st
import pandas as pd
import logging
from datetime import datetime
from shared.utils.cursor_rules import CursorRules
from shared.components.layouts import DashboardLayout
from shared.components.filters import DateFilters
from modules.comercial.services.api_service import ComercialAPIService
from .sales_vs_target import create_sales_vs_target_chart
from .monthly_growth import create_monthly_growth_chart
import locale
import calendar
from modules.comercial.components import TendenciaVendas
from modules.comercial.services import comercial_service
import plotly.graph_objects as go
from shared.utils.formatters import format_currency, format_number

logger = logging.getLogger(__name__)

# Configura locale para português brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

logging.basicConfig(level=logging.DEBUG)

def calcular_meta_anual(df: pd.DataFrame, percentual_aumento: float) -> float:
    """Calcula meta anual baseada no faturamento total do ano anterior + percentual"""
    ano_atual = datetime.now().year
    
    # Extrai ano da data de emissão
    df = df.copy()
    df['ano'] = pd.to_datetime(df['emissao']).dt.year
    
    # Filtra ano anterior
    df_ano_anterior = df[df['ano'] == ano_atual - 1]
    
    if df_ano_anterior.empty:
        return 0
        
    faturamento_total = df_ano_anterior['valorfaturado'].sum()
    meta_anual = faturamento_total * (1 + percentual_aumento/100)
    return meta_anual / 12  # Divide por 12 para distribuir igualmente entre os meses

def formatar_valor_br(valor: float) -> str:
    """Formata valor monetário no padrão brasileiro"""
    return locale.currency(valor, grouping=True, symbol='R$')

def prepare_data_for_chart(df: pd.DataFrame, meta_percentual: float) -> pd.DataFrame:
    """
    Prepara dados para o gráfico de vendas vs meta
    """
    try:
        df = df.copy()
        ano_atual = datetime.now().year
        
        if 'emissao' not in df.columns:
            return pd.DataFrame()
            
        df['emissao'] = pd.to_datetime(df['emissao'])
        df['ano'] = df['emissao'].dt.year
        df['mes'] = df['emissao'].dt.month
        
        # Cria DataFrame base com todos os meses de 2025
        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        
        df_mensal = pd.DataFrame({'mes': range(1, 13)})
        df_mensal['Mês'] = df_mensal['mes'].map(meses)
        
        # Pega vendas de 2025 (se houver)
        vendas_2025 = df[df['ano'] == ano_atual].groupby('mes')['valorfaturado'].sum().reset_index()
        
        # Merge com vendas (preenchendo zeros onde não há vendas)
        df_mensal = df_mensal.merge(vendas_2025, on='mes', how='left')
        df_mensal['Vendas'] = df_mensal['valorfaturado'].fillna(0)
        
        # Calcula meta baseada em 2024
        ano_anterior = ano_atual - 1
        faturamento_ano_anterior = df[df['ano'] == ano_anterior]['valorfaturado'].sum()
        
        if faturamento_ano_anterior > 0:
            meta_mensal = (faturamento_ano_anterior * (1 + meta_percentual/100)) / 12
        else:
            meta_mensal = 0
            
        df_mensal['Meta'] = meta_mensal
        
        return df_mensal[['Mês', 'Vendas', 'Meta']]
            
    except Exception as e:
        return pd.DataFrame()

def render_performance():
    """Renderiza o dashboard de Performance de Vendas"""
    try:
        # Título com ano dinâmico
        st.header(f"📈 Performance de Vendas")
        st.subheader(f"Meta para {datetime.now().year}")
        
        # Carrega dados especificando a view correta
        api_service = ComercialAPIService()
        df_vendas = api_service.get_data("CUBO_FATURAMENTO")  # Especifica a view
        
        if df_vendas is None or df_vendas.empty:
            st.error("""
                Não foi possível carregar os dados. 
                Possíveis causas:
                - Problema de conexão com o servidor
                - Tabela não encontrada no banco de dados
                - Erro na consulta SQL
                
                Por favor, verifique se todas as tabelas necessárias existem no banco de dados.
            """)
            logger.error("Falha ao carregar dados da API")
            return
            
        
        
        # Slider para definir meta
        meta_percentual = st.slider(
            "Percentual de aumento para Meta",
            min_value=0,
            max_value=100,
            value=10,
            step=10,
            help="Define o percentual de aumento sobre o faturamento do ano anterior"
        )
        
        # Prepara dados para o gráfico
        df_graficos = prepare_data_for_chart(df_vendas, meta_percentual)
        
        if df_graficos.empty:
            st.error('Erro ao preparar dados para visualização.')
            return
            
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            fig_vendas = create_sales_vs_target_chart(df_graficos)
            if fig_vendas:
                st.plotly_chart(fig_vendas, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de vendas vs meta')
                
        # Adicionar o gráfico
        st.markdown("---")

        # Prepara dados para filtro de ano
        if 'emissao' in df_vendas.columns:
            df_vendas['emissao'] = pd.to_datetime(df_vendas['emissao'])
            df_vendas['ano'] = df_vendas['emissao'].dt.year
            
            # Adiciona filtro de anos logo após o carregamento dos dados
            with st.expander("🔍 Filtros de Análise"):
                anos_disponiveis = sorted(df_vendas['ano'].unique())
                if anos_disponiveis:
                    anos_selecionados = DateFilters.year_filter("performance_vendas")
                    logger.debug(f"Anos disponíveis: {anos_disponiveis}")
                    logger.debug(f"Anos selecionados: {anos_selecionados}")
                    
                    # Aplica filtro apenas se houver anos selecionados
                    if anos_selecionados and len(anos_selecionados) > 0:
                        df_vendas = df_vendas[df_vendas['ano'].isin(anos_selecionados)]
                        logger.debug(f"Dados filtrados por anos: {df_vendas.shape[0]} registros restantes")

        try:
            # Renderiza o texto de ajuda
            TendenciaVendas.render_help_text(st)

            # Renderiza o gráfico
            tendencia = TendenciaVendas.create_trend_chart(df_vendas)
            if tendencia:
                st.plotly_chart(tendencia, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de tendência')
        except Exception as e:
            st.error('Erro ao criar gráfico')
            logger.error(f'Erro: {str(e)}')
            
    except Exception as e:
        st.error(f"Erro ao renderizar dashboard: {str(e)}")

def render_performance_vendas():
    """Renderiza o dashboard de performance de vendas"""
    # Título principal
    st.title("Performance de Vendas")
    
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
            
            # Cria uma cópia do DataFrame original para o gráfico de Vendas vs Meta
            df_vendas_meta = df.copy()
            
            # Adiciona filtro de anos logo após o carregamento dos dados
            with st.expander("🔍 Filtros de Análise"):
                anos_disponiveis = sorted(df['ano'].unique())
                if anos_disponiveis:
                    anos_selecionados = DateFilters.year_filter("performance_vendas")
                    logger.debug(f"Anos disponíveis: {anos_disponiveis}")
                    logger.debug(f"Anos selecionados: {anos_selecionados}")
                    
                    # Aplica filtro apenas se houver anos selecionados
                    if anos_selecionados and len(anos_selecionados) > 0:
                        df = df[df['ano'].isin(anos_selecionados)]
                        logger.debug(f"Dados filtrados por anos: {df.shape[0]} registros restantes")
        
        # Título da seção de meta
        st.subheader(f"Meta para {datetime.now().year}")
        
        # Slider para definir meta
        meta_percentual = st.slider(
            "Percentual de aumento para Meta",
            min_value=0,
            max_value=100,
            value=10,
            step=10,
            help="Define o percentual de aumento sobre o faturamento do ano anterior"
        )
        
        # Gráfico de Vendas vs Meta (usando df_vendas_meta - sem filtro)
        try:
            vendas_meta = create_sales_vs_target_chart(df_vendas_meta, meta_percentual)
            if vendas_meta:
                st.plotly_chart(vendas_meta, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de vendas vs meta')
        except Exception as e:
            st.error('Erro ao criar gráfico de vendas vs meta')
            logger.error(f'Erro no gráfico de vendas vs meta: {str(e)}')
        
        st.markdown("---")  # Separador visual
        
        # Demais gráficos usando df filtrado
        try:
            # Renderiza o texto de ajuda
            TendenciaVendas.render_help_text(st)

            # Renderiza o gráfico
            tendencia = TendenciaVendas.create_trend_chart(df)
            if tendencia:
                st.plotly_chart(tendencia, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de tendência')
        except Exception as e:
            st.error('Erro ao criar gráfico de tendência')
            logger.error(f'Erro no gráfico de tendência: {str(e)}')
                
    except Exception as e:
        st.error('Erro ao renderizar dashboard')
        logger.error(f'Erro na renderização: {str(e)}')

def create_trend_chart(df: pd.DataFrame) -> go.Figure:
    """Cria gráfico de tendência de vendas"""
    try:
        # Prepara os dados
        df = df.copy()
        df['emissao'] = pd.to_datetime(df['emissao'])
        df = df.sort_values('emissao')
        
        # Calcula o valor máximo para ajustar a escala
        max_valor = df['valorfaturado'].max()
        intervalo = 200000  # 200 mil
        y_max = ((max_valor // intervalo) + 1) * intervalo
        
        # Gera valores para o eixo Y
        y_valores = list(range(0, int(y_max) + intervalo, intervalo))
        y_textos = [format_currency(val) for val in y_valores]
        
        # Prepara os valores formatados para o hover
        df['valor_formatado'] = df['valorfaturado'].apply(format_currency)
        
        # Cria o gráfico
        fig = go.Figure()
        
        # Adiciona a linha de tendência
        fig.add_trace(go.Scatter(
            x=df['emissao'],
            y=df['valorfaturado'],
            mode='lines',
            name='Vendas',
            line=dict(color='#2E93fA', width=2),
            customdata=df[['valor_formatado']],
            hovertemplate='Valor: %{customdata[0]}<extra></extra>'
        ))
        
        # Atualiza o layout
        fig.update_layout(
            title='Tendência de Vendas',
            xaxis_title='Período',
            yaxis_title='Valor Faturado',
            hovermode='x unified',
            yaxis=dict(
                tickmode='array',
                tickvals=y_valores,
                ticktext=y_textos,
                range=[0, max(y_valores)]
            ),
            xaxis=dict(
                dtick='M1',
                tickformat='%B/%Y'
            ),
            hoverlabel=dict(
                bgcolor="#1e1e1e",
                font_size=12,
                font_family="Arial",
                font=dict(color="white"),
                bordercolor="#2E93fA"
            )
        )
        
        # Traduz os meses para português
        meses_pt = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
            'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
            'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
            'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
        }
        
        # Atualiza os rótulos do eixo X para português
        fig.update_xaxes(
            ticktext=[f"{meses_pt[d.strftime('%B')]}/{d.strftime('%Y')}" 
                     for d in pd.date_range(df['emissao'].min(), df['emissao'].max(), freq='M')],
            tickvals=pd.date_range(df['emissao'].min(), df['emissao'].max(), freq='M')
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Erro ao criar gráfico de tendência: {str(e)}")
        return None