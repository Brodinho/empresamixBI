"""
Gráfico de Vendas vs Meta
"""
import plotly.graph_objects as go
import pandas as pd
import logging
import locale
from typing import List

logger = logging.getLogger(__name__)

# Configura locale para português brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatar_moeda_br(valor: float) -> str:
    """Formata valor para o padrão monetário brasileiro"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

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
    fig = go.Figure()
    
    # Calcula o valor máximo para ajustar a escala
    max_vendas = df['Vendas'].max()
    max_meta = df['Meta'].max()
    max_valor = max(max_vendas, max_meta)
    
    # Gera valores para o eixo Y
    y_valores = criar_valores_eixo(max_valor)
    y_textos = [formatar_moeda_br(val) for val in y_valores]
    
    # Prepara os valores formatados para o hover
    df['vendas_formatado'] = df['Vendas'].apply(formatar_moeda_br)
    df['meta_formatado'] = df['Meta'].apply(formatar_moeda_br)
    
    # Linha de Vendas
    fig.add_trace(go.Scatter(
        x=df['Mês'],
        y=df['Vendas'],
        name='Vendas',
        line=dict(color='#2E93fA', width=2),
        customdata=df['vendas_formatado'],
        hovertemplate="Vendas: %{customdata}<extra></extra>"
    ))
    
    # Linha de Meta
    fig.add_trace(go.Scatter(
        x=df['Mês'],
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
            ticktext=df['Mês'],
            tickvals=list(range(len(df['Mês'])))
        ),
        hoverlabel=dict(
            bgcolor="#1e1e1e",
            font_size=12,
            font_family="Arial",
            font=dict(
                color="white"
            ),
            bordercolor="#2E93fA"
        )
    )
    
    return fig 