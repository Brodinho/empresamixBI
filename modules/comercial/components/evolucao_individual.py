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
        
        # Calcula os valores para os ticks do eixo Y
        y_max = evolucao_pivot.max().max()
        y_step = y_max / 7  # Divide em 7 partes
        y_ticks = [i * y_step for i in range(8)]  # Cria 8 pontos
        
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
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            margin=dict(t=120, l=50),
            xaxis_title='Período',
            yaxis=dict(
                title='Valor Faturado',
                tickvals=y_ticks,
                ticktext=[format_currency(v) for v in y_ticks]
            ),
            height=400,
            template='plotly_dark',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=1.1,
                xanchor="left",
                x=0,
                bgcolor='rgba(0,0,0,0)'
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