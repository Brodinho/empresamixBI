import plotly.graph_objects as go
import pandas as pd
from shared.utils.formatters import format_currency, format_date
import logging

logger = logging.getLogger(__name__)

class TendenciaVendas:
    @staticmethod
    def create_trend_chart(df: pd.DataFrame) -> go.Figure:
        """Cria gráfico de linha mostrando a tendência de vendas ao longo do tempo"""
        try:
            # Preparação dos dados
            df['emissao'] = pd.to_datetime(df['emissao'])
            dados = df.groupby('emissao')['valorfaturado'].sum().reset_index()
            dados = dados.sort_values('emissao')
            
            # Criação do gráfico
            fig = go.Figure()
            
            # Linha principal de vendas
            fig.add_trace(
                go.Scatter(
                    x=dados['emissao'],
                    y=dados['valorfaturado'],
                    mode='lines',
                    name='Vendas',
                    line=dict(color='#1f77b4', width=3),
                    hovertemplate='Data: %{x}<br>Valor: ' + format_currency('%{y:.2f}') + '<extra></extra>'
                )
            )
            
            # Configuração do layout
            fig.update_layout(
                title='Tendência de Vendas',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400,
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title='Período'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    title='Valor Faturado',
                    tickformat=',.2f'
                ),
                hovermode='x unified'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de tendência: {str(e)}")
            return None 