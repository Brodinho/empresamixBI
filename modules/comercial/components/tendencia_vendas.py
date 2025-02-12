import plotly.graph_objects as go
import pandas as pd
from shared.utils.formatters import format_currency, format_date
import logging

logger = logging.getLogger(__name__)

class TendenciaVendas:
    @staticmethod
    def render_help_text(st) -> None:
        """Renderiza texto de ajuda sobre o gráfico de tendência"""
        with st.expander("📊 Como interpretar o gráfico de Tendência de Vendas?", expanded=False):
            st.markdown("""
            ### 📈 Análise de Tendência de Vendas
            
            Este gráfico apresenta a evolução diária das vendas ao longo do tempo, permitindo:
            
            🔍 **Identificar Padrões**:
            - Picos de vendas
            - Períodos sazonais
            - Tendências de crescimento ou queda
            
            📅 **Análise Temporal**:
            - Visualização dia a dia
            - Comparação entre períodos
            - Identificação de ciclos de venda
            
            💡 **Dicas de Interpretação**:
            - Os picos indicam dias com maior volume de vendas
            - Vales representam períodos de menor movimento
            - A linha de tendência ajuda a identificar a direção geral das vendas
            
            ⚠️ **Observações**:
            - Valores incluem todas as vendas faturadas
            - Hover sobre os pontos para ver valores específicos
            - Use os filtros acima para ajustar o período de análise
            """)

    @staticmethod
    def create_trend_chart(df: pd.DataFrame) -> go.Figure:
        """Cria gráfico de linha mostrando a tendência de vendas ao longo do tempo"""
        try:
            # Preparação dos dados
            df['emissao'] = pd.to_datetime(df['emissao'])
            df = df.sort_values('emissao')
            
            # Calcula o valor máximo para ajustar a escala
            max_valor = df['valorfaturado'].max()
            intervalo = 200000  # 200 mil
            y_max = ((max_valor // intervalo) + 1) * intervalo
            
            # Gera valores para o eixo Y usando format_currency
            y_valores = list(range(0, int(y_max) + intervalo, intervalo))
            y_textos = [format_currency(val) for val in y_valores]
            
            # Prepara os valores formatados para o hover usando format_currency
            df['valor_formatado'] = df['valorfaturado'].apply(format_currency)
            df['data_formatada'] = df['emissao'].apply(lambda x: format_date(x))
            
            # Criação do gráfico
            fig = go.Figure()
            
            # Linha principal de vendas
            fig.add_trace(
                go.Scatter(
                    x=df['emissao'],
                    y=df['valorfaturado'],
                    mode='lines',
                    name='Vendas',
                    line=dict(color='#1f77b4', width=3),
                    customdata=df[['data_formatada', 'valor_formatado']],
                    hovertemplate='Data: %{customdata[0]}<br>' +
                                'Valor: %{customdata[1]}<extra></extra>'
                )
            )
            
            # Configuração do layout
            fig.update_layout(
                title='Tendência de Vendas',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400,
                yaxis=dict(
                    tickmode='array',
                    tickvals=y_valores,
                    ticktext=y_textos,
                    range=[0, max(y_valores)],
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title='Valor Faturado'
                ),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title='Período',
                    tickangle=45
                ),
                hovermode='x unified',
                hoverlabel=dict(
                    bgcolor="#1e1e1e",
                    font_size=12,
                    font_family="Arial",
                    font=dict(color="white"),
                    bordercolor="#2E93fA"
                )
            )
            
            # Atualiza os rótulos do eixo X usando format_date
            dates = pd.date_range(df['emissao'].min(), df['emissao'].max(), freq='M')
            fig.update_xaxes(
                ticktext=[format_date(d, "%B/%Y") for d in dates],
                tickvals=dates
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de tendência: {str(e)}")
            return None 