"""
Visualização do Status das Ordens de Serviço
"""
import plotly.graph_objects as go
import pandas as pd
import logging
from shared.utils.formatters import format_number, format_percentage

logger = logging.getLogger(__name__)

def create_os_status_chart(df: pd.DataFrame) -> go.Figure:
    """Cria o gráfico de status das OS's"""
    try:
        # Mapeamento dos status
        status_map = {
            0: 'Abertas',
            1: 'Para Fabricar',
            2: 'Fabricadas',
            3: 'Para Faturar',
            4: 'Faturadas',
            5: 'Canceladas'
        }
        
        # Cria uma cópia do dataframe com o status mapeado
        df_plot = df.copy()
        df_plot['status_texto'] = df_plot['status'].map(status_map)
        
        # Agrupa os dados por status
        df_status = df_plot.groupby('status_texto')['os'].count().reset_index()
        
        # Calcula percentuais
        total_os = df_status['os'].sum()
        df_status['percentual'] = (df_status['os'] / total_os * 100).round(1)
        
        # Cria um mapeamento para ordenação
        ordem_status = {status: i for i, status in status_map.items()}
        df_status['ordem'] = df_status['status_texto'].map(ordem_status)
        
        # Ordena por ordem do status (0 a 5)
        df_status = df_status.sort_values('ordem', ascending=False)
        
        # Cores para cada status
        colors = {
            'Abertas': '#FFA500',        # Laranja
            'Para Fabricar': '#2E93fA',  # Azul
            'Fabricadas': '#4CAF50',     # Verde
            'Para Faturar': '#FF6B6B',   # Vermelho claro
            'Faturadas': '#4CAF50',      # Verde
            'Canceladas': '#FF4444'      # Vermelho
        }
        
        # Encontra o valor máximo para definir a escala
        max_value = df_status['os'].max()
        # Arredonda para cima para o próximo múltiplo de 100
        max_tick = ((max_value // 100) + 1) * 100
        # Cria a sequência de ticks de 100 em 100
        tick_values = list(range(0, max_tick + 100, 100))
        
        # Cria o gráfico de barras horizontais
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df_status['status_texto'],
            x=df_status['os'],
            orientation='h',
            marker_color=[colors.get(status, '#808080') for status in df_status['status_texto']],
            text=df_status.apply(
                lambda x: f"{format_number(x['os'])} OS's ({format_percentage(x['percentual'])})",
                axis=1
            ),
            textposition='auto',
            hovertemplate="Status: %{y}<br>Quantidade: %{x:,.0f} OS's<br>Percentual: %{text}<extra></extra>"
        ))
        
        # Layout
        fig.update_layout(
            title='Status das Ordens de Serviço',
            showlegend=False,
            xaxis=dict(
                title='Quantidade de OS',
                showgrid=True,
                gridcolor='rgba(128, 128, 128, 0.2)',
                zeroline=True,
                zerolinecolor='rgba(128, 128, 128, 0.2)',
                tickformat=",d",  # Formato numérico com separador de milhares
                tickmode='array',
                tickvals=tick_values,
                ticktext=[str(x) for x in tick_values]
            ),
            yaxis=dict(
                title=None,
                categoryorder='array',
                categoryarray=list(status_map.values())[::-1]  # Inverte a ordem para ficar de 5 a 0
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Erro ao criar gráfico de status das OS's: {str(e)}")
        return None 