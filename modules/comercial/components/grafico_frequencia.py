import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import streamlit as st
from shared.utils.formatters import format_number

def criar_grafico_frequencia(df):
    """
    Cria um gráfico de distribuição da frequência de compras dos clientes
    """
    try:
        # Adiciona o expander explicativo
        with st.expander("ℹ️ Como interpretar a Frequência?"):
            st.markdown("""
                ### Interpretando o Gráfico de Frequência
                
                Este gráfico mostra como os clientes estão distribuídos de acordo com o número de compras realizadas:
                
                - **Eixo X**: Número de compras realizadas por cliente
                - **Eixo Y**: Densidade de clientes
                - **Barras**: Quantidade de clientes em cada faixa de frequência
                - **Linha**: Tendência geral da distribuição
                
                📊 **Linhas de Referência**:
                - **Linha Verde**: Média de compras por cliente
                - **Linha Laranja**: Mediana de compras por cliente
                
                💡 **Dica**: 
                - Clientes com maior frequência (mais à direita) são mais fiéis
                - Grande concentração à esquerda indica oportunidade de aumentar recorrência
            """)
        
        # Cria o histograma com curva de densidade
        hist_data = [df['frequencia']]
        group_labels = ['Frequência']
        
        # Cores personalizadas
        colors = ['#2E75B6']
        
        # Cria a figura com o histograma e curva de densidade
        fig = ff.create_distplot(
            hist_data,
            group_labels,
            colors=colors,
            bin_size=5,  # Ajustado para frequência
            show_rug=False
        )
        
        # Personaliza o layout
        fig.update_layout(
            title={
                'text': 'Distribuição da Frequência de Compras',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Número de Compras',
            yaxis_title='Densidade',
            showlegend=False,
            template='plotly_dark',
            height=400,
            margin=dict(t=50, l=50, r=30, b=50),
            hovermode='x'
        )
        
        # Formata o hover template
        fig.update_traces(
            hovertemplate="<br>".join([
                "Compras: %{x:.0f}",
                "Densidade: %{y:.4f}",
                "<extra></extra>"
            ])
        )
        
        # Adiciona estatísticas
        mediana = df['frequencia'].median()
        media = df['frequencia'].mean()
        
        # Linha da mediana
        fig.add_vline(
            x=mediana,
            line_dash="dash",
            line_color="#FF9800",
            annotation=dict(
                text=f"Mediana: {format_number(mediana, decimals=1)} compras",
                yanchor="bottom",
                y=0.85,
                font=dict(color="#FF9800")
            )
        )
        
        # Linha da média
        fig.add_vline(
            x=media,
            line_dash="dash",
            line_color="#4CAF50",
            annotation=dict(
                text=f"Média: {format_number(media, decimals=1)} compras",
                yanchor="bottom",
                y=1.0,
                font=dict(color="#4CAF50")
            )
        )
        
        # Renderiza o gráfico
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro ao criar gráfico de frequência: {str(e)}")
        logger.error(f"Erro ao criar gráfico de frequência: {str(e)}") 