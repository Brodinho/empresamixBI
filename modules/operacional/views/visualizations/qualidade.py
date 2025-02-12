import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Controle de Qualidade")
    
    # Dados de exemplo
    df_qualidade = pd.DataFrame({
        'Produto': ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E'],
        'Producao_Total': [1000, 800, 1200, 600, 900],
        'Defeitos': [20, 24, 18, 15, 27],
        'Taxa_Defeito': [0.020, 0.030, 0.015, 0.025, 0.030],
        'Custo_Retrabalho': [2000.00, 2400.00, 1800.00, 1500.00, 2700.00]
    })
    
    # KPIs
    total_producao = df_qualidade['Producao_Total'].sum()
    total_defeitos = df_qualidade['Defeitos'].sum()
    taxa_defeito_geral = total_defeitos / total_producao
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total Produzido',
            'value': f"{total_producao:,.0f}"
        },
        {
            'label': 'Total Defeitos',
            'value': f"{total_defeitos:,.0f}"
        },
        {
            'label': 'Taxa de Defeitos',
            'value': CursorRules.format_percentage(taxa_defeito_geral)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de taxa de defeitos
        fig_defeitos = ChartComponents.create_bar_chart(
            df_qualidade,
            x='Produto',
            y='Taxa_Defeito',
            title='Taxa de Defeitos por Produto'
        )
        st.plotly_chart(fig_defeitos, use_container_width=True)
    
    with col2:
        # Gráfico de custo de retrabalho
        fig_retrabalho = ChartComponents.create_bar_chart(
            df_qualidade,
            x='Produto',
            y='Custo_Retrabalho',
            title='Custo de Retrabalho por Produto'
        )
        st.plotly_chart(fig_retrabalho, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_qualidade, ['Custo_Retrabalho'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['Taxa_Defeito'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 