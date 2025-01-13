import plotly.graph_objects as go
import pandas as pd
from ..constants.chart_constants import RANKING_COLORS, RANKING_CONFIG

class VendasPorRegiao:
    @staticmethod
    def create_sales_region_chart(df: pd.DataFrame) -> go.Figure:
        """Cria gráfico de vendas por região com comparativo anual"""
        
        # Cria coluna de região considerando UF e países
        df['location_name'] = df.apply(
            lambda row: row['pais'] if row['uf'] == 'EX' else row['uf'], 
            axis=1
        )
        
        # Agrupa dados por região e ano
        vendas_regiao = df.groupby(['location_name', 'ano'])['valorfaturado'].sum().reset_index()
        
        # Pivota os dados para ter anos como colunas
        vendas_pivot = vendas_regiao.pivot(
            index='location_name',
            columns='ano',
            values='valorfaturado'
        ).reset_index()
        
        # Ordena por valor total decrescente
        total_por_regiao = vendas_pivot.iloc[:, 1:].sum(axis=1)
        vendas_pivot['total'] = total_por_regiao
        vendas_pivot = vendas_pivot.sort_values('total', ascending=True)
        vendas_pivot = vendas_pivot.drop('total', axis=1)
        
        # Cria o gráfico
        fig = go.Figure()
        
        # Adiciona barras para cada ano
        anos = [col for col in vendas_pivot.columns if col != 'location_name']
        for ano in anos:
            fig.add_trace(go.Bar(
                name=str(ano),
                x=vendas_pivot[ano],
                y=vendas_pivot['location_name'],
                orientation='h',
                text=vendas_pivot[ano].apply(
                    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                ),
                textposition='auto',
                marker=dict(
                    opacity=0.7
                )
            ))
        
        # Configura o layout
        fig.update_layout(
            title='Vendas por Região',
            barmode='group',
            showlegend=True,
            legend_title_text='Ano',
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
            height=400,
            font=dict(color='white')
        )
        
        return fig 