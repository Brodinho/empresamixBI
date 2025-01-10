"""
Visualização do Ranking de Regiões
"""
import plotly.graph_objects as go
import pandas as pd
import logging
from shared.utils.formatters import format_currency

logger = logging.getLogger(__name__)

def create_region_ranking(df: pd.DataFrame) -> go.Figure:
    """Cria o ranking de regiões"""
    try:
        # Cria cópia do DataFrame
        df_ranking = df.copy()
        
        # Trata vendas internas (mantém agrupamento por UF)
        df_interno = df_ranking[df_ranking['uf'] != 'EX'].groupby(['uf', 'tipo_venda'])['valorfaturado'].sum().reset_index()
        
        # Trata vendas externas (agrupa por país)
        df_externo = df_ranking[df_ranking['uf'] == 'EX'].groupby(['codPais', 'pais', 'tipo_venda'])['valorfaturado'].sum().reset_index()
        df_externo['uf'] = df_externo['pais']  # Usa nome do país como identificador
        
        # Combina os DataFrames
        ranking_data = pd.concat([df_interno, df_externo])
        
        # Ordena e pega top 5
        ranking_data = ranking_data.nlargest(5, 'valorfaturado')
        
        # Calcula percentuais
        total_faturamento = ranking_data['valorfaturado'].sum()
        ranking_data['percentual'] = (ranking_data['valorfaturado'] / total_faturamento * 100).round(1)
        
        # Cria gráfico
        fig = go.Figure()
        
        # Barras para cada tipo de venda
        colors = {'INTERNO': 'blue', 'EXTERNO': 'green'}
        
        for tipo in ['INTERNO', 'EXTERNO']:
            df_tipo = ranking_data[ranking_data['tipo_venda'] == tipo]
            
            if not df_tipo.empty:
                fig.add_trace(go.Bar(
                    y=df_tipo['uf'],
                    x=df_tipo['valorfaturado'],
                    orientation='h',
                    name=tipo,
                    marker_color=colors[tipo],
                    text=df_tipo.apply(
                        lambda x: f"{format_currency(x['valorfaturado'])} ({x['percentual']}%)",
                        axis=1
                    ),
                    textposition='auto',
                    hoverinfo='none'
                ))
        
        # Layout
        fig.update_layout(
            title='Top 5 Regiões por Faturamento',
            barmode='group',
            yaxis={'categoryorder':'total ascending'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            # Configuração do eixo X sem valores monetários
            xaxis=dict(
                showticklabels=False,  # Remove os rótulos do eixo
                showgrid=True,         # Mantém as linhas de grade
                gridcolor='rgba(128, 128, 128, 0.2)',  # Cor suave para as linhas de grade
                zeroline=True,         # Mantém a linha do zero
                zerolinecolor='rgba(128, 128, 128, 0.2)'  # Cor suave para a linha do zero
            )
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Erro ao criar ranking: {str(e)}")
        return None 