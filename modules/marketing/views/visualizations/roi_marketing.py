import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("ROI de Marketing")
    
    # Dados de exemplo
    df_roi = pd.DataFrame({
        'Canal': ['Google Ads', 'Facebook Ads', 'Email', 'SEO', 'Influencers'],
        'Investimento': [15000.00, 12000.00, 5000.00, 8000.00, 10000.00],
        'Receita': [45000.00, 30000.00, 20000.00, 35000.00, 25000.00],
        'ROI': [2.00, 1.50, 3.00, 3.38, 1.50],
        'CAC': [25.00, 30.00, 15.00, 20.00, 35.00]
    })
    
    # KPIs
    total_investimento = df_roi['Investimento'].sum()
    total_receita = df_roi['Receita'].sum()
    roi_geral = (total_receita / total_investimento) - 1
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Investimento Total',
            'value': CursorRules.format_currency(total_investimento)
        },
        {
            'label': 'Receita Total',
            'value': CursorRules.format_currency(total_receita)
        },
        {
            'label': 'ROI Geral',
            'value': CursorRules.format_percentage(roi_geral)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de ROI por canal
        fig_roi = ChartComponents.create_bar_chart(
            df_roi,
            x='Canal',
            y='ROI',
            title='ROI por Canal'
        )
        st.plotly_chart(fig_roi, use_container_width=True)
    
    with col2:
        # Gráfico de CAC por canal
        fig_cac = ChartComponents.create_bar_chart(
            df_roi,
            x='Canal',
            y='CAC',
            title='Custo de Aquisição por Canal'
        )
        st.plotly_chart(fig_cac, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_roi, ['Investimento', 'Receita', 'CAC'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['ROI'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 