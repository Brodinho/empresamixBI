import plotly.graph_objects as go
import pandas as pd
from shared.utils.formatters import format_currency
import logging

logger = logging.getLogger(__name__)

def criar_mix_produtos_vendedor(df: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico treemap do mix de produtos por vendedor
    """
    try:
        # Prepara os dados
        df_mix = df.groupby(['vendedor', 'grupo', 'subGrupo'])['valorfaturado'].sum().reset_index()
        
        # Calcula percentuais para cada nível
        total_geral = df_mix['valorfaturado'].sum()
        
        # Calcula percentuais por vendedor
        df_mix['perc_vendedor'] = df_mix.groupby('vendedor')['valorfaturado'].transform(
            lambda x: (x.sum() / total_geral) * 100
        )
        
        # Calcula percentuais por grupo dentro de cada vendedor
        df_mix['perc_grupo'] = df_mix.groupby(['vendedor', 'grupo'])['valorfaturado'].transform(
            lambda x: (x.sum() / x.sum()) * 100
        )
        
        # Prepara os dados para o treemap
        fig = go.Figure(go.Treemap(
            labels=[
                f"{row['vendedor']}<br>{row['grupo']}<br>{row['subGrupo']}"
                for _, row in df_mix.iterrows()
            ],
            parents=[
                f"{row['vendedor']}<br>{row['grupo']}"
                if row['subGrupo'] else (
                    f"{row['vendedor']}"
                    if row['grupo'] else ""
                )
                for _, row in df_mix.iterrows()
            ],
            values=df_mix['valorfaturado'],
            textinfo="label+value+percent parent",
            hovertemplate=(
                "<b>%{label}</b><br>" +
                "Valor: %{customdata[0]}<br>" +
                "% do Total: %{customdata[1]:.1f}%<br>" +
                "<extra></extra>"
            ),
            customdata=[
                [format_currency(val), perc] 
                for val, perc in zip(df_mix['valorfaturado'], df_mix['perc_vendedor'])
            ],
            marker=dict(
                colors=df_mix['valorfaturado'],
                colorscale='Blues',
                showscale=True
            )
        ))
        
        # Atualiza o layout
        fig.update_layout(
            title={
                'text': 'Mix de Produtos por Vendedor',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            template='plotly_dark',
            height=500,
            margin=dict(t=50, l=25, r=25, b=25)
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Erro ao criar gráfico de mix de produtos: {str(e)}")
        return None 