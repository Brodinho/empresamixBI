import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import streamlit as st
from shared.utils.formatters import format_number, format_currency

def criar_grafico_recencia(df):
    """
    Cria um gráfico de distribuição da recência dos clientes
    usando histograma com curva de densidade
    """
    try:
        # Adiciona o expander explicativo
        with st.expander("ℹ️ Como interpretar a Recência?"):
            st.markdown("""
                ### Interpretando o Gráfico de Recência
                
                Este gráfico mostra a distribuição dos clientes com base no tempo desde sua última compra:
                
                - **Eixo X**: Representa os dias desde a última compra
                - **Eixo Y**: Mostra a densidade de clientes
                - **Barras**: Indicam a quantidade de clientes em cada faixa de recência
                - **Linha**: Representa a tendência geral da distribuição
                
                📊 **Linhas de Referência**:
                - **Linha Verde**: Média de dias desde a última compra
                - **Linha Laranja**: Mediana de dias desde a última compra
                
                💡 **Dica**: Clientes com menor recência (mais à esquerda) são mais ativos e podem ser mais propensos a novas compras.
            """)
        
        # Cria o histograma com curva de densidade
        hist_data = [df['recencia']]
        group_labels = ['Recência']
        
        # Cores personalizadas
        colors = ['#2E75B6']  # Azul corporativo
        
        # Cria a figura com o histograma e curva de densidade
        fig = ff.create_distplot(
            hist_data,
            group_labels,
            colors=colors,
            bin_size=30,
            show_rug=False
        )
        
        # Personaliza o layout
        fig.update_layout(
            title={
                'text': 'Distribuição da Recência dos Clientes',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Dias desde a última compra',
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
                "Dias: %{x:.0f}",
                "Densidade: %{y:.4f}",
                "<extra></extra>"
            ])
        )
        
        # Adiciona anotações com estatísticas em posições diferentes
        mediana = df['recencia'].median()
        media = df['recencia'].mean()
        
        # Linha da mediana (mais baixa)
        fig.add_vline(
            x=mediana,
            line_dash="dash",
            line_color="#FF9800",
            annotation=dict(
                text=f"Mediana: {format_number(mediana, decimals=0)} dias",
                yanchor="bottom",
                y=0.85,  # Posição mais baixa
                font=dict(color="#FF9800")
            )
        )
        
        # Linha da média (mais alta)
        fig.add_vline(
            x=media,
            line_dash="dash",
            line_color="#4CAF50",
            annotation=dict(
                text=f"Média: {format_number(media, decimals=0)} dias",
                yanchor="bottom",
                y=1.0,  # Posição mais alta
                font=dict(color="#4CAF50")
            )
        )
        
        # Renderiza o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro ao criar gráfico de recência: {str(e)}")
        logger.error(f"Erro ao criar gráfico de recência: {str(e)}") 