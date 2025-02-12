import plotly.express as px
import pandas as pd
from ..constants.map_constants import MAP_COLORS, MAPBOX_CONFIG, HOVER_TEMPLATE

class TerritoryMap:
    @staticmethod
    def create_scatter_mapbox(df: pd.DataFrame) -> px.scatter_mapbox:
        """Cria mapa de dispersão com vendas por território"""
        
        # Normaliza o tamanho das bolhas
        max_fat = df['faturamento'].max()
        df['size'] = (df['faturamento'] / max_fat * 50) + 10
        
        # Formata os valores para o hover
        df['faturamento_fmt'] = df['faturamento'].apply(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        
        # Cria o mapa usando Plotly Express
        fig = px.scatter_mapbox(
            df,
            lat='latitude',
            lon='longitude',
            size='size',
            color='tipo_venda',
            color_discrete_map=MAP_COLORS,
            hover_name='location_name',
            hover_data={
                'faturamento_fmt': True,
                'latitude': False,
                'longitude': False,
                'size': False,
                'tipo_venda': False,
                'faturamento': False
            },
            labels={
                'faturamento_fmt': 'Faturamento',
                'tipo_venda': 'Tipo de Venda'
            }
        )
        
        # Configura o layout
        fig.update_layout(
            mapbox=dict(
                style='carto-positron',
                zoom=3.5,
                center=dict(lat=-15.7801, lon=-47.9292)
            ),
            showlegend=True,
            legend_title_text='Tipo de Venda',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99,
                bgcolor="rgba(0, 0, 0, 0.8)",
                font=dict(color="white"),
                bordercolor="rgba(255, 255, 255, 0.3)",
                borderwidth=1
            ),
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Atualiza o template do hover
        fig.update_traces(
            hovertemplate="<b>%{hovertext}</b><br>Faturamento: %{customdata[0]}<extra></extra>"
        )
        
        return fig 