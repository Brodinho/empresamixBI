import plotly.graph_objects as go
import pandas as pd
from shared.utils.formatters import format_currency
import logging

logger = logging.getLogger(__name__)

class VendasPorRegiao:
    @staticmethod
    def create_sales_region_chart(df: pd.DataFrame) -> go.Figure:
        """Cria gráfico de vendas por região (top 10)"""
        try:
            # Cria coluna de região considerando UF e países
            df['location_name'] = df.apply(
                lambda row: row['pais'] if row['uf'] == 'EX' else row['uf'], 
                axis=1
            )
            
            # Agrupa dados apenas por região (soma total do período)
            vendas_regiao = df.groupby('location_name')['valorfaturado'].sum().reset_index()
            
            # Seleciona top 10 e ordena (decrescente para visualização)
            vendas_regiao = vendas_regiao.nlargest(10, 'valorfaturado')
            vendas_regiao = vendas_regiao.sort_values('valorfaturado', ascending=False)
            
            # Cria o gráfico
            fig = go.Figure()
            
            # Adiciona uma única barra por região
            fig.add_trace(go.Bar(
                x=vendas_regiao['valorfaturado'],
                y=vendas_regiao['location_name'],
                orientation='h',
                text=vendas_regiao['valorfaturado'].apply(format_currency),
                textposition='auto',
                marker=dict(color='#1f77b4', opacity=0.7),
                hoverinfo='none'
            ))
            
            # Configura o layout
            fig.update_layout(
                title='Top 10 Regiões em Vendas',
                showlegend=False,
                xaxis=dict(
                    title='Faturamento',
                    showgrid=True,
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    zeroline=False,
                    # Configuração dos ticks do eixo x
                    tickmode='array',
                    tickvals=[i * 5000000 for i in range(10)],  # Valores de 0 a 45M, de 5 em 5
                    ticktext=[f"{i * 5} milhões" for i in range(10)]  # Textos correspondentes
                ),
                yaxis=dict(
                    title='',
                    autorange='reversed'  # Mantém ordem decrescente
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=50, r=50, t=50, b=50),
                height=400,
                font=dict(color='white')
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar gráfico de vendas por região: {str(e)}")
            return None 