"""
Visualização da Distribuição de Clientes por Região
"""
import plotly.graph_objects as go
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def create_client_distribution(df: pd.DataFrame) -> go.Figure:
    """Cria o gráfico de distribuição de clientes por região"""
    try:
        # Cria cópia do DataFrame
        df_clientes = df.copy()
        
        # Separa clientes internos e externos
        df_interno = df_clientes[df_clientes['uf'] != 'EX'].groupby('uf')['codcli'].nunique().reset_index()
        df_interno['tipo'] = 'INTERNO'
        
        df_externo = df_clientes[df_clientes['uf'] == 'EX'].groupby('pais')['codcli'].nunique().reset_index()
        df_externo['tipo'] = 'EXTERNO'
        df_externo['uf'] = df_externo['pais']
        
        # Combina os DataFrames
        distribution_data = pd.concat([df_interno, df_externo])
        
        # Ordena e pega top 10
        distribution_data = distribution_data.nlargest(10, 'codcli')
        
        # Calcula percentuais
        total_clientes = distribution_data['codcli'].sum()
        distribution_data['percentual'] = (distribution_data['codcli'] / total_clientes * 100).round(1)
        
        # Cria gráfico
        fig = go.Figure()
        
        # Cores para interno e externo
        colors = {'INTERNO': 'blue', 'EXTERNO': 'green'}
        
        # Adiciona barras para cada tipo
        for tipo in ['INTERNO', 'EXTERNO']:
            df_tipo = distribution_data[distribution_data['tipo'] == tipo]
            
            if not df_tipo.empty:
                fig.add_trace(go.Bar(
                    x=df_tipo['codcli'],
                    y=df_tipo['uf'],
                    orientation='h',
                    name=tipo,
                    marker_color=colors[tipo],
                    text=df_tipo.apply(
                        lambda x: f"{int(x['codcli'])} clientes ({x['percentual']}%)",
                        axis=1
                    ),
                    textposition='auto',
                    hoverinfo='text'
                ))
        
        # Layout
        fig.update_layout(
            title='Top 10 Regiões por Número de Clientes',
            barmode='group',
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,  # Reduzido pois agora são menos regiões
            xaxis=dict(
                showticklabels=False,  # Remove números do eixo X
                showgrid=True,
                gridcolor='rgba(128, 128, 128, 0.2)',
                zeroline=True,
                zerolinecolor='rgba(128, 128, 128, 0.2)',
                title=None  # Remove título do eixo X
            ),
            yaxis=dict(
                title=None,  # Remove título do eixo Y
                categoryorder='total ascending'
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Erro ao criar distribuição de clientes: {str(e)}")
        return None 