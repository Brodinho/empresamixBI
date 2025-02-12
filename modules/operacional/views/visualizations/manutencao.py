import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Manutenção")
    
    # Dados de exemplo
    df_manutencao = pd.DataFrame({
        'Equipamento': ['Máq. 01', 'Máq. 02', 'Máq. 03', 'Máq. 04', 'Máq. 05'],
        'Disponibilidade': [0.92, 0.88, 0.95, 0.90, 0.93],
        'MTBF': [720, 600, 840, 680, 750],  # horas
        'MTTR': [4, 6, 3, 5, 4],  # horas
        'Custo_Manutencao': [12000.00, 15000.00, 8500.00, 13500.00, 11000.00]
    })
    
    # KPIs
    disponibilidade_media = df_manutencao['Disponibilidade'].mean()
    mtbf_medio = df_manutencao['MTBF'].mean()
    custo_total = df_manutencao['Custo_Manutencao'].sum()
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Disponibilidade Média',
            'value': CursorRules.format_percentage(disponibilidade_media)
        },
        {
            'label': 'MTBF Médio',
            'value': f"{mtbf_medio:.0f}h"
        },
        {
            'label': 'Custo Total',
            'value': CursorRules.format_currency(custo_total)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de disponibilidade
        fig_disp = ChartComponents.create_bar_chart(
            df_manutencao,
            x='Equipamento',
            y='Disponibilidade',
            title='Disponibilidade por Equipamento'
        )
        st.plotly_chart(fig_disp, use_container_width=True)
    
    with col2:
        # Gráfico de MTBF vs MTTR
        fig_mtbf = ChartComponents.create_bar_chart(
            df_manutencao,
            x='Equipamento',
            y=['MTBF', 'MTTR'],
            title='MTBF vs MTTR por Equipamento'
        )
        st.plotly_chart(fig_mtbf, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_manutencao, ['Custo_Manutencao'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['Disponibilidade'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 