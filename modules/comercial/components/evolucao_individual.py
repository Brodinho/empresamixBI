import plotly.graph_objects as go
import pandas as pd
from shared.utils.formatters import format_currency
import logging

logger = logging.getLogger(__name__)

def criar_evolucao_individual(df: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de evolução de vendas por vendedor ao longo do tempo
    """
    try:
        # Prepara os dados
        df = df.copy()
        df['emissao'] = pd.to_datetime(df['emissao'])
        df['mes_ano'] = df['emissao'].dt.strftime('%Y-%m')
        
        # Agrupa dados por mês e vendedor
        evolucao = df.groupby(['mes_ano', 'vendedor'])['valorfaturado'].sum().reset_index()
        
        # Pivota a tabela para ter vendedores como colunas
        evolucao_pivot = evolucao.pivot(
            index='mes_ano',
            columns='vendedor',
            values='valorfaturado'
        ).fillna(0)
        
        # Cria o gráfico
        fig = go.Figure()
        
        # Adiciona uma linha para cada vendedor
        for vendedor in evolucao_pivot.columns:
            valores = evolucao_pivot[vendedor]
            valores_formatados = [format_currency(v) for v in valores]
            
            fig.add_trace(go.Scatter(
                x=evolucao_pivot.index,
                y=valores,
                name=vendedor,
                mode='lines+markers',
                line=dict(width=2),
                marker=dict(size=6),
                hovertemplate=(
                    f"<b>{vendedor}</b><br>" +
                    "Mês: %{x}<br>" +
                    "Valor: %{text}<br>" +
                    "<extra></extra>"
                ),
                text=valores_formatados
            ))
        
        # Atualiza o layout
        fig.update_layout(
            title={
                'text': 'Evolução de Vendas por Vendedor',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Período',
            yaxis_title='Valor Faturado',
            template='plotly_dark',
            height=400,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            # Formata os valores do eixo Y
            yaxis=dict(
                tickformat="R$,.0f",
                hoverformat="R$,.2f"
            ),
            hovermode='x unified'
        )
        
        # Traduz os meses para português
        meses_pt = {
            '01': 'Jan', '02': 'Fev', '03': 'Mar',
            '04': 'Abr', '05': 'Mai', '06': 'Jun',
            '07': 'Jul', '08': 'Ago', '09': 'Set',
            '10': 'Out', '11': 'Nov', '12': 'Dez'
        }
        
        # Formata as datas no eixo X
        fig.update_xaxes(
            ticktext=[f"{meses_pt[d.split('-')[1]]}/{d.split('-')[0]}" 
                     for d in evolucao_pivot.index],
            tickvals=evolucao_pivot.index
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Erro ao criar gráfico de evolução individual: {str(e)}")
        return None 