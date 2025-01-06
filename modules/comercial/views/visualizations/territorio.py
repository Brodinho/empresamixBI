import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Análise de Território")
    
    # Dados de exemplo
    df_territorio = pd.DataFrame({
        'Região': ['Sul', 'Sudeste', 'Norte', 'Nordeste', 'Centro-Oeste'],
        'Vendas': [280000.00, 520000.00, 150000.00, 320000.00, 180000.00],
        'Meta': [300000.00, 500000.00, 180000.00, 350000.00, 200000.00],
        'Atingimento': [0.93, 1.04, 0.83, 0.91, 0.90]
    })
    
    # KPIs
    total_vendas = df_territorio['Vendas'].sum()
    total_meta = df_territorio['Meta'].sum()
    atingimento_geral = total_vendas / total_meta
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total Vendas',
            'value': CursorRules.format_currency(total_vendas)
        },
        {
            'label': 'Meta Total',
            'value': CursorRules.format_currency(total_meta)
        },
        {
            'label': 'Atingimento Geral',
            'value': CursorRules.format_percentage(atingimento_geral)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de vendas por região
        fig_vendas = ChartComponents.create_bar_chart(
            df_territorio,
            x='Região',
            y=['Vendas', 'Meta'],
            title='Vendas vs Meta por Região'
        )
        st.plotly_chart(fig_vendas, use_container_width=True)
    
    with col2:
        # Gráfico de atingimento
        fig_atingimento = ChartComponents.create_line_chart(
            df_territorio,
            x='Região',
            y='Atingimento',
            title='Atingimento por Região'
        )
        st.plotly_chart(fig_atingimento, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_territorio, ['Vendas', 'Meta'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['Atingimento'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 