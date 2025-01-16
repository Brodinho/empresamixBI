import plotly.graph_objects as go
import pandas as pd
import logging
from shared.utils.formatters import format_currency, format_number, format_percentage

# Configuração do logger
logger = logging.getLogger(__name__)

def criar_analise_conversao_vendedor(df: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de análise de conversão por vendedor com escalas ajustadas
    """
    try:
        # Agrupa dados por vendedor
        metricas_vendedor = df.groupby('vendedor').agg({
            'codcli': 'nunique',  # Número de clientes únicos
            'nota': 'count',      # Número total de vendas
            'valorfaturado': 'sum'  # Soma total
        }).reset_index()
        
        # Calcula valor médio por venda e vendas por cliente
        metricas_vendedor['valor_medio'] = (
            metricas_vendedor['valorfaturado'] / 
            metricas_vendedor['nota']
        )
        metricas_vendedor['vendas_por_cliente'] = (
            metricas_vendedor['nota'] / 
            metricas_vendedor['codcli']
        )
        
        # Ordena por valor médio (decrescente) e inverte a ordem das linhas
        metricas_vendedor = (
            metricas_vendedor
            .sort_values('valor_medio', ascending=True)  # Ordena crescente primeiro
            .reset_index(drop=True)  # Reseta o índice
        )
        
        # Cria o gráfico com os dados ordenados
        fig = go.Figure()
        
        # Define posições das barras para evitar sobreposição
        bar_positions = [-0.3, 0, 0.3]  # Posições relativas das barras
        
        # Adiciona barras para Valor Médio
        fig.add_trace(go.Bar(
            name='Valor Médio por Venda',
            x=metricas_vendedor['valor_medio'],
            y=metricas_vendedor['vendedor'],
            orientation='h',
            marker_color='#2E75B6',
            text=[format_currency(v) for v in metricas_vendedor['valor_medio']],
            textposition='auto',
            hovertemplate="Valor Médio: %{text}<br>Vendedor: %{y}<extra></extra>",
            xaxis='x',
            offset=bar_positions[0],
            width=0.2
        ))
        
        # Adiciona barras para Vendas por Cliente
        fig.add_trace(go.Bar(
            name='Vendas por Cliente',
            x=metricas_vendedor['vendas_por_cliente'],
            y=metricas_vendedor['vendedor'],
            orientation='h',
            marker_color='#4CAF50',
            text=[f"{v:.1f}" for v in metricas_vendedor['vendas_por_cliente']],
            textposition='auto',
            hovertemplate="Vendas/Cliente: %{text}<br>Vendedor: %{y}<extra></extra>",
            xaxis='x2',
            offset=bar_positions[1],
            width=0.2
        ))
        
        # Adiciona barras para Total de Clientes
        fig.add_trace(go.Bar(
            name='Total de Clientes',
            x=metricas_vendedor['codcli'],
            y=metricas_vendedor['vendedor'],
            orientation='h',
            marker_color='#FF9800',
            text=[f"{int(v)}" for v in metricas_vendedor['codcli']],
            textposition='auto',
            hovertemplate="Total Clientes: %{text}<br>Vendedor: %{y}<extra></extra>",
            xaxis='x3',
            offset=bar_positions[2],
            width=0.2
        ))
        
        # Atualiza o layout
        fig.update_layout(
            title={
                'text': 'Análise de Conversão por Vendedor',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis=dict(
                title="Valor Médio por Venda (R$)",
                side="bottom",
                position=0,
                domain=[0, 0.3],
                range=[0, max(metricas_vendedor['valor_medio']) * 1.2],
                tickformat=",.0f",
                tickprefix="R$ "
            ),
            xaxis2=dict(
                title="Quantidade Média de Vendas por Cliente",
                side="bottom",
                position=0,
                domain=[0.35, 0.65],
                range=[0, max(metricas_vendedor['vendas_por_cliente']) * 1.2],
                tickformat=".1f",
                showgrid=True,
                gridcolor='rgba(128, 128, 128, 0.2)'
            ),
            xaxis3=dict(
                title="Quantidade Total de Clientes Atendidos",
                side="bottom",
                position=0,
                domain=[0.7, 1.0],
                range=[0, max(metricas_vendedor['codcli']) * 1.2],
                tickformat=",.0f",
                showgrid=True,
                gridcolor='rgba(128, 128, 128, 0.2)'
            ),
            height=max(500, len(metricas_vendedor) * 35),
            margin=dict(l=200, r=100, t=120, b=150),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            barmode='group',
            template='plotly_dark'
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Erro ao criar gráfico de análise de conversão: {str(e)}")
        return None 