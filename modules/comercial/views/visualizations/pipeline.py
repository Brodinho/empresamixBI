import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Análise de Pipeline")
    
    # Dados de exemplo
    df_pipeline = pd.DataFrame({
        'Etapa': ['Prospecção', 'Qualificação', 'Proposta', 'Negociação', 'Fechamento'],
        'Valor': [500000.00, 350000.00, 200000.00, 150000.00, 100000.00],
        'Quantidade': [100, 70, 40, 25, 15],
        'Taxa_Conversao': [1.00, 0.70, 0.57, 0.63, 0.60]
    })
    
    # KPIs
    valor_total = df_pipeline['Valor'].sum()
    qtd_total = df_pipeline['Quantidade'].sum()
    taxa_media = df_pipeline['Taxa_Conversao'].mean()
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Valor Total Pipeline',
            'value': CursorRules.format_currency(valor_total)
        },
        {
            'label': 'Oportunidades',
            'value': qtd_total
        },
        {
            'label': 'Taxa Média Conversão',
            'value': CursorRules.format_percentage(taxa_media)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de funil
        fig_funil = ChartComponents.create_bar_chart(
            df_pipeline,
            x='Valor',
            y='Etapa',
            title='Funil de Vendas',
            horizontal=True
        )
        st.plotly_chart(fig_funil, use_container_width=True)
    
    with col2:
        # Gráfico de conversão
        fig_conversao = ChartComponents.create_line_chart(
            df_pipeline,
            x='Etapa',
            y='Taxa_Conversao',
            title='Taxa de Conversão por Etapa'
        )
        st.plotly_chart(fig_conversao, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_pipeline, ['Valor'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['Taxa_Conversao'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 