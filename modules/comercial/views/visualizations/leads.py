import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Gestão de Leads")
    
    # Dados de exemplo
    df_leads = pd.DataFrame({
        'Origem': ['Site', 'Indicação', 'LinkedIn', 'Email', 'Eventos'],
        'Quantidade': [150, 80, 120, 90, 60],
        'Valor_Potencial': [300000.00, 200000.00, 250000.00, 180000.00, 150000.00],
        'Taxa_Conversao': [0.15, 0.25, 0.18, 0.12, 0.20]
    })
    
    # KPIs
    total_leads = df_leads['Quantidade'].sum()
    valor_total = df_leads['Valor_Potencial'].sum()
    conv_media = df_leads['Taxa_Conversao'].mean()
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total de Leads',
            'value': total_leads
        },
        {
            'label': 'Valor Potencial',
            'value': CursorRules.format_currency(valor_total)
        },
        {
            'label': 'Conversão Média',
            'value': CursorRules.format_percentage(conv_media)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de distribuição de leads
        fig_dist = ChartComponents.create_pie_chart(
            df_leads,
            values='Quantidade',
            names='Origem',
            title='Distribuição de Leads por Origem'
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        # Gráfico de valor potencial
        fig_valor = ChartComponents.create_bar_chart(
            df_leads,
            x='Origem',
            y='Valor_Potencial',
            title='Valor Potencial por Origem'
        )
        st.plotly_chart(fig_valor, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_leads, ['Valor_Potencial'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['Taxa_Conversao'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 