"""
Visualização do Tempo Médio em cada etapa das OS's
"""
import plotly.graph_objects as go
import pandas as pd
import logging
from shared.utils.formatters import format_number

logger = logging.getLogger(__name__)

def create_os_tempo_medio_chart(df: pd.DataFrame) -> go.Figure:
    """Cria o gráfico de tempo médio em cada etapa das OS's"""
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
        
        # Calcula o tempo em cada status (em dias)
        df_plot['tempo_status'] = (pd.Timestamp.now() - df_plot['data']).dt.days
        
        # Agrupa os dados por status e calcula a média de tempo
        df_tempo = df_plot.groupby('status_texto')['tempo_status'].mean().round(1).reset_index()
        
        # Cria um mapeamento para ordenação
        ordem_status = {status: i for i, status in status_map.items()}
        df_tempo['ordem'] = df_tempo['status_texto'].map(ordem_status)
        
        # Ordena por ordem do status (0 a 5)
        df_tempo = df_tempo.sort_values('ordem', ascending=False)
        
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
        max_value = df_tempo['tempo_status'].max()
        # Arredonda para cima para o próximo múltiplo de 10
        max_tick = ((max_value // 10) + 1) * 10
        # Cria a sequência de ticks de 10 em 10
        tick_values = list(range(0, int(max_tick) + 10, 10))
        
        # Cria o gráfico de barras horizontais
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df_tempo['status_texto'],
            x=df_tempo['tempo_status'],
            orientation='h',
            marker_color=[colors.get(status, '#808080') for status in df_tempo['status_texto']],
            text=df_tempo['tempo_status'].apply(lambda x: f"{format_number(x)} dias"),
            textposition='auto',
            hovertemplate="Status: %{y}<br>Tempo Médio: %{text}<extra></extra>"
        ))
        
        # Layout
        fig.update_layout(
            title='Tempo Médio em cada Etapa',
            showlegend=False,
            xaxis=dict(
                title='Dias',
                showgrid=True,
                gridcolor='rgba(128, 128, 128, 0.2)',
                zeroline=True,
                zerolinecolor='rgba(128, 128, 128, 0.2)',
                tickformat=",.1f",  # Formato numérico com uma casa decimal
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
        logger.error(f"Erro ao criar gráfico de tempo médio das OS's: {str(e)}")
        return None 