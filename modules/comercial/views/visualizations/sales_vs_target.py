"""
Gráfico de Vendas vs Meta
"""
import plotly.graph_objects as go
import pandas as pd
import logging
from typing import List
from shared.utils.formatters import format_currency, format_number

logger = logging.getLogger(__name__)

def criar_valores_eixo(max_valor: float) -> List[float]:
    """Cria valores para o eixo Y com intervalos adequados"""
    if max_valor <= 0:
        return [0, 1000, 2000, 3000, 4000, 5000]
    
    magnitude = len(str(int(max_valor))) - 1
    base = 10 ** magnitude
    step = base / 2
    valores = [i * step for i in range(0, int((max_valor * 1.2) / step) + 1)]
    return valores

def create_sales_vs_target_chart(df: pd.DataFrame) -> go.Figure:
    """Cria gráfico de vendas vs meta"""
    try:
        fig = go.Figure()
        
        # Calcula o valor máximo para ajustar a escala
        max_vendas = df['Vendas'].max() if 'Vendas' in df.columns else 0
        max_meta = df['Meta'].max() if 'Meta' in df.columns else 0
        max_valor = max(max_vendas, max_meta)
        
        # Gera valores para o eixo Y
        y_valores = criar_valores_eixo(max_valor)
        y_textos = [format_currency(val) for val in y_valores]
        
        # Prepara os valores formatados para o hover
        if 'Vendas' in df.columns and 'Meta' in df.columns:
            df['vendas_formatado'] = df['Vendas'].apply(format_currency)
            df['meta_formatado'] = df['Meta'].apply(format_currency)
            
            # Linha de Vendas
            fig.add_trace(go.Scatter(
                x=df['Mês'] if 'Mês' in df.columns else df.index,
                y=df['Vendas'],
                name='Vendas',
                line=dict(color='#2E93fA', width=2),
                customdata=df['vendas_formatado'],
                hovertemplate="Vendas: %{customdata}<extra></extra>"
            ))
            
            # Linha de Meta
            fig.add_trace(go.Scatter(
                x=df['Mês'] if 'Mês' in df.columns else df.index,
                y=df['Meta'],
                name='Meta',
                line=dict(color='#FFA500', width=2, dash='dash'),
                customdata=df['meta_formatado'],
                hovertemplate="Meta: %{customdata}<extra></extra>"
            ))
        
        # Configuração do layout
        fig.update_layout(
            title='Vendas vs Meta',
            xaxis_title='',
            yaxis_title='',
            hovermode='x unified',
            yaxis=dict(
                tickmode='array',
                tickvals=y_valores,
                ticktext=y_textos,
                range=[0, max(y_valores)]
            ),
            xaxis=dict(
                tickangle=45,
                tickmode='array',
                ticktext=df['Mês'] if 'Mês' in df.columns else df.index,
                tickvals=list(range(len(df.index)))
            ),
            hoverlabel=dict(
                bgcolor="#1e1e1e",
                font_size=12,
                font_family="Arial",
                font=dict(color="white"),
                bordercolor="#2E93fA"
            )
        )
        
        return fig
    except Exception as e:
        logger.error(f"Erro ao criar gráfico de vendas vs meta: {str(e)}")
        return None 