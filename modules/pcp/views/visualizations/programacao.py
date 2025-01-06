import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Programação da Produção")
    
    # Dados de exemplo
    df_programacao = pd.DataFrame({
        'Ordem': ['OP001', 'OP002', 'OP003', 'OP004', 'OP005'],
        'Produto': ['Prod A', 'Prod B', 'Prod C', 'Prod A', 'Prod B'],
        'Quantidade': [1000, 800, 1200, 900, 750],
        'Tempo_Previsto': [480, 360, 600, 420, 330],  # minutos
        'Eficiencia': [0.95, 0.92, 0.88, 0.94, 0.91]
    })
    
    # KPIs
    total_ordens = len(df_programacao)
    total_tempo = df_programacao['Tempo_Previsto'].sum()
    eficiencia_media = df_programacao['Eficiencia'].mean()
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total de Ordens',
            'value': total_ordens
        },
        {
            'label': 'Tempo Total',
            'value': f"{total_tempo/60:.1f}h"
        },
        {
            'label': 'Eficiência Média',
            'value': CursorRules.format_percentage(eficiencia_media)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de tempo por ordem
        fig_tempo = ChartComponents.create_bar_chart(
            df_programacao,
            x='Ordem',
            y='Tempo_Previsto',
            title='Tempo Previsto por Ordem'
        )
        st.plotly_chart(fig_tempo, use_container_width=True)
    
    with col2:
        # Gráfico de eficiência
        fig_eficiencia = ChartComponents.create_line_chart(
            df_programacao,
            x='Ordem',
            y='Eficiencia',
            title='Eficiência por Ordem'
        )
        st.plotly_chart(fig_eficiencia, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_percentage(df_programacao, ['Eficiencia'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 