import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Gestão de Estoque")
    
    # Dados de exemplo
    df_estoque = pd.DataFrame({
        'Material': ['Mat. A', 'Mat. B', 'Mat. C', 'Mat. D', 'Mat. E'],
        'Quantidade': [1000, 750, 500, 1200, 800],
        'Valor_Unit': [50.00, 75.00, 120.00, 45.00, 90.00],
        'Giro': [12, 8, 6, 15, 10],
        'Cobertura': [30, 45, 60, 24, 36]  # dias
    })
    
    # Calculando valores derivados
    df_estoque['Valor_Total'] = df_estoque['Quantidade'] * df_estoque['Valor_Unit']
    
    # KPIs
    valor_total = df_estoque['Valor_Total'].sum()
    giro_medio = df_estoque['Giro'].mean()
    cobertura_media = df_estoque['Cobertura'].mean()
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Valor Total Estoque',
            'value': CursorRules.format_currency(valor_total)
        },
        {
            'label': 'Giro Médio Anual',
            'value': f"{giro_medio:.1f}x"
        },
        {
            'label': 'Cobertura Média',
            'value': f"{cobertura_media:.0f} dias"
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de valor em estoque
        fig_valor = ChartComponents.create_pie_chart(
            df_estoque,
            values='Valor_Total',
            names='Material',
            title='Distribuição do Valor em Estoque'
        )
        st.plotly_chart(fig_valor, use_container_width=True)
    
    with col2:
        # Gráfico de giro vs cobertura
        fig_giro = ChartComponents.create_bar_chart(
            df_estoque,
            x='Material',
            y=['Giro', 'Cobertura'],
            title='Giro e Cobertura por Material'
        )
        st.plotly_chart(fig_giro, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_estoque, ['Valor_Unit', 'Valor_Total'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 