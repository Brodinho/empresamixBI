import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Análise de Capacidade")
    
    # Dados de exemplo
    df_capacidade = pd.DataFrame({
        'Recurso': ['Máq. 01', 'Máq. 02', 'Máq. 03', 'Máq. 04', 'Máq. 05'],
        'Capacidade_Total': [480, 480, 480, 480, 480],  # minutos/dia
        'Carga_Alocada': [420, 450, 380, 440, 400],     # minutos/dia
        'Utilizacao': [0.88, 0.94, 0.79, 0.92, 0.83],
        'Ociosidade': [0.12, 0.06, 0.21, 0.08, 0.17]
    })
    
    # KPIs
    utilizacao_media = df_capacidade['Utilizacao'].mean()
    capacidade_total = df_capacidade['Capacidade_Total'].sum()
    carga_total = df_capacidade['Carga_Alocada'].sum()
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Utilização Média',
            'value': CursorRules.format_percentage(utilizacao_media)
        },
        {
            'label': 'Capacidade Total',
            'value': f"{capacidade_total/60:.1f}h"
        },
        {
            'label': 'Carga Total',
            'value': f"{carga_total/60:.1f}h"
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de utilização
        fig_util = ChartComponents.create_bar_chart(
            df_capacidade,
            x='Recurso',
            y=['Utilizacao', 'Ociosidade'],
            title='Utilização vs Ociosidade por Recurso'
        )
        st.plotly_chart(fig_util, use_container_width=True)
    
    with col2:
        # Gráfico de carga vs capacidade
        fig_carga = ChartComponents.create_bar_chart(
            df_capacidade,
            x='Recurso',
            y=['Capacidade_Total', 'Carga_Alocada'],
            title='Capacidade vs Carga Alocada'
        )
        st.plotly_chart(fig_carga, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_percentage(
        df_capacidade, 
        ['Utilizacao', 'Ociosidade']
    )
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 