import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Orçamento")
    
    # Dados de exemplo
    df_orcamento = pd.DataFrame({
        'Centro_Custo': ['Comercial', 'Operações', 'Marketing', 'RH', 'TI'],
        'Orcado': [200000.00, 350000.00, 150000.00, 120000.00, 80000.00],
        'Realizado': [180000.00, 320000.00, 145000.00, 115000.00, 85000.00],
        'Variacao': [-0.10, -0.09, -0.03, -0.04, 0.06]
    })
    
    # KPIs
    total_orcado = df_orcamento['Orcado'].sum()
    total_realizado = df_orcamento['Realizado'].sum()
    variacao_total = (total_realizado / total_orcado) - 1
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total Orçado',
            'value': CursorRules.format_currency(total_orcado)
        },
        {
            'label': 'Total Realizado',
            'value': CursorRules.format_currency(total_realizado)
        },
        {
            'label': 'Variação Total',
            'value': CursorRules.format_percentage(variacao_total)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de comparação orçado vs realizado
        fig_comparacao = ChartComponents.create_bar_chart(
            df_orcamento,
            x='Centro_Custo',
            y=['Orcado', 'Realizado'],
            title='Orçado vs Realizado por Centro de Custo'
        )
        st.plotly_chart(fig_comparacao, use_container_width=True)
    
    with col2:
        # Gráfico de variações
        fig_variacao = ChartComponents.create_bar_chart(
            df_orcamento,
            x='Centro_Custo',
            y='Variacao',
            title='Variação Orçamentária (%)'
        )
        st.plotly_chart(fig_variacao, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_orcamento, ['Orcado', 'Realizado'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['Variacao'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 