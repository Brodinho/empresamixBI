"""
Visualização dos Gargalos de Produção
"""
import plotly.graph_objects as go
import pandas as pd
import logging
from shared.utils.formatters import format_number, format_percentage

logger = logging.getLogger(__name__)

def create_os_gargalos_chart(df: pd.DataFrame) -> go.Figure:
    """Cria o gráfico de gargalos de produção"""
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
        
        # Remove status "Canceladas" para o funil
        df_status = df_status[df_status['status_texto'] != 'Canceladas']
        
        # Ordena os status na ordem do processo
        ordem_processo = ['Abertas', 'Para Fabricar', 'Fabricadas', 'Para Faturar', 'Faturadas']
        df_status = df_status.set_index('status_texto').reindex(ordem_processo).reset_index()
        
        # Calcula o total acumulado em cada etapa (incluindo as que já passaram)
        df_status['total_acumulado'] = df_status['os'].iloc[::-1].cumsum().iloc[::-1]
        
        # Cores para cada etapa
        colors = [
            '#FFA500',  # Laranja
            '#2E93fA',  # Azul
            '#4CAF50',  # Verde
            '#FF6B6B',  # Vermelho claro
            '#4CAF50',  # Verde
        ]
        
        # Cria o gráfico de funil
        fig = go.Figure()
        
        fig.add_trace(go.Funnel(
            name='Quantidade',
            y=df_status['status_texto'],
            x=df_status['total_acumulado'],  # Usa o total acumulado ao invés da contagem simples
            textposition="auto",
            textinfo="value+percent initial",
            opacity=0.65,
            marker={
                "color": colors,
                "line": {"width": 2, "color": colors}
            },
            text=df_status.apply(
                lambda x: f"{format_number(x['total_acumulado'])} OS's",
                axis=1
            ),
            hovertemplate="Status: %{y}<br>Quantidade: %{text}<br>Taxa: %{percentInitial:.1%}<extra></extra>"
        ))
        
        # Layout
        fig.update_layout(
            title='Gargalos de Produção',
            showlegend=False,
            yaxis=dict(
                title=None,
                categoryorder='array',
                categoryarray=ordem_processo
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            funnelmode="stack",
            funnelgap=0.1
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Erro ao criar gráfico de gargalos de produção: {str(e)}")
        return None 