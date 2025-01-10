"""
Gráfico de Crescimento Mensal
"""
import plotly.graph_objects as go
import pandas as pd
import logging
from shared.utils.formatters import format_percentage

logger = logging.getLogger(__name__)

def create_monthly_growth_chart(df: pd.DataFrame) -> go.Figure:
    """Cria o gráfico de crescimento mensal"""
    try:
        fig = go.Figure()
        
        # Barras de crescimento
        fig.add_trace(go.Bar(
            x=df['Mês'],
            y=df['Crescimento'],
            marker_color='#2196F3',
            text=[format_percentage(x) for x in df['Crescimento']],
            textposition='auto',
        ))
        
        # Layout
        fig.update_layout(
            title='Crescimento Mensal',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            yaxis=dict(
                tickformat=',.0%',
                gridcolor='rgba(128, 128, 128, 0.2)',
                zeroline=True,
                zerolinecolor='rgba(128, 128, 128, 0.2)'
            ),
            xaxis=dict(
                gridcolor='rgba(128, 128, 128, 0.2)',
            ),
            showlegend=False
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Erro ao criar gráfico de crescimento mensal: {str(e)}")
        return None 