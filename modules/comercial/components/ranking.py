import plotly.graph_objects as go
import pandas as pd
from ..constants.chart_constants import RANKING_COLORS, RANKING_CONFIG

class RegionRanking:
    @staticmethod
    def create_ranking_chart(df: pd.DataFrame) -> go.Figure:
        """Cria gráfico de ranking das top 5 regiões por faturamento"""
        
        # Calcula o faturamento total para percentuais
        total_faturamento = df['faturamento'].sum()
        
        # Ordena e pega os top 5
        top_5 = df.nlargest(5, 'faturamento')[['location_name', 'faturamento', 'tipo_venda']]
        
        # Calcula os percentuais
        top_5['percentual'] = (top_5['faturamento'] / total_faturamento * 100)
        
        # Formata os valores para exibição
        top_5['faturamento_fmt'] = top_5['faturamento'].apply(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        top_5['percentual_fmt'] = top_5['percentual'].apply(
            lambda x: f"{x:.1f}%"
        )
        
        # Cria o gráfico
        fig = go.Figure()
        
        # Adiciona as barras
        fig.add_trace(go.Bar(
            x=top_5['faturamento'],
            y=top_5['location_name'],
            orientation='h',
            text=top_5.apply(
                lambda row: f"{row['faturamento_fmt']}<br>{row['percentual_fmt']}", 
                axis=1
            ),
            textposition='outside',
            marker=dict(
                color=[RANKING_COLORS[tipo] for tipo in top_5['tipo_venda']],
                opacity=0.7
            )
        ))
        
        # Configura o layout
        fig.update_layout(
            title='Top 5 Regiões por Faturamento',
            showlegend=False,
            xaxis=dict(
                title='Faturamento',
                showgrid=True,
                gridcolor=RANKING_CONFIG['grid_color'],
                zeroline=False
            ),
            yaxis=dict(
                title='',
                autorange='reversed'
            ),
            plot_bgcolor=RANKING_CONFIG['background'],
            paper_bgcolor=RANKING_CONFIG['background'],
            margin=RANKING_CONFIG['margin'],
            height=RANKING_CONFIG['height'],
            font=dict(color='white')  # Texto em branco para combinar com o tema escuro
        )
        
        return fig 