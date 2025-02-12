import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Produção")
    
    # Dados de exemplo
    df_producao = pd.DataFrame({
        'Produto': ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E'],
        'Quantidade': [1000, 800, 1200, 600, 900],
        'Eficiencia': [0.92, 0.88, 0.95, 0.87, 0.91],
        'Custo_Unit': [50.00, 75.00, 45.00, 80.00, 60.00],
        'Setup_Medio': [45, 60, 40, 55, 50]  # minutos
    })
    
    # KPIs
    total_producao = df_producao['Quantidade'].sum()
    eficiencia_media = df_producao['Eficiencia'].mean()
    custo_medio = df_producao['Custo_Unit'].mean()
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total Produzido',
            'value': f"{total_producao:,.0f}"
        },
        {
            'label': 'Eficiência Média',
            'value': CursorRules.format_percentage(eficiencia_media)
        },
        {
            'label': 'Custo Médio',
            'value': CursorRules.format_currency(custo_medio)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de produção por produto
        fig_producao = ChartComponents.create_bar_chart(
            df_producao,
            x='Produto',
            y='Quantidade',
            title='Quantidade Produzida por Produto'
        )
        st.plotly_chart(fig_producao, use_container_width=True)
    
    with col2:
        # Gráfico de eficiência
        fig_eficiencia = ChartComponents.create_line_chart(
            df_producao,
            x='Produto',
            y='Eficiencia',
            title='Eficiência por Produto'
        )
        st.plotly_chart(fig_eficiencia, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_producao, ['Custo_Unit'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['Eficiencia'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 