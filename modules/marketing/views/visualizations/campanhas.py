import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Campanhas de Marketing")
    
    # Dados de exemplo
    df_campanhas = pd.DataFrame({
        'Campanha': ['Black Friday', 'Natal', 'Páscoa', 'Dia das Mães', 'Inverno'],
        'Investimento': [50000.00, 45000.00, 30000.00, 35000.00, 40000.00],
        'Retorno': [150000.00, 120000.00, 75000.00, 90000.00, 95000.00],
        'ROI': [2.00, 1.67, 1.50, 1.57, 1.38],
        'Conversao': [0.15, 0.12, 0.10, 0.11, 0.09]
    })
    
    # KPIs
    total_investimento = df_campanhas['Investimento'].sum()
    total_retorno = df_campanhas['Retorno'].sum()
    roi_medio = (total_retorno / total_investimento) - 1
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total Investido',
            'value': CursorRules.format_currency(total_investimento)
        },
        {
            'label': 'Retorno Total',
            'value': CursorRules.format_currency(total_retorno)
        },
        {
            'label': 'ROI Médio',
            'value': CursorRules.format_percentage(roi_medio)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de ROI por campanha
        fig_roi = ChartComponents.create_bar_chart(
            df_campanhas,
            x='Campanha',
            y='ROI',
            title='ROI por Campanha'
        )
        st.plotly_chart(fig_roi, use_container_width=True)
    
    with col2:
        # Gráfico de investimento vs retorno
        fig_invest = ChartComponents.create_bar_chart(
            df_campanhas,
            x='Campanha',
            y=['Investimento', 'Retorno'],
            title='Investimento vs Retorno'
        )
        st.plotly_chart(fig_invest, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_campanhas, ['Investimento', 'Retorno'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['ROI', 'Conversao'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 