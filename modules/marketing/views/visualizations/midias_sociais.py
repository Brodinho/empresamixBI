import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Análise de Mídias Sociais")
    
    # Dados de exemplo
    df_midias = pd.DataFrame({
        'Rede': ['Instagram', 'Facebook', 'LinkedIn', 'Twitter', 'YouTube'],
        'Seguidores': [50000, 35000, 25000, 15000, 10000],
        'Engajamento': [0.045, 0.032, 0.058, 0.025, 0.065],
        'Investimento': [8000.00, 6000.00, 7000.00, 3000.00, 5000.00],
        'Conversoes': [250, 180, 220, 80, 120]
    })
    
    # KPIs
    total_seguidores = df_midias['Seguidores'].sum()
    total_investimento = df_midias['Investimento'].sum()
    media_engajamento = df_midias['Engajamento'].mean()
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total de Seguidores',
            'value': f"{total_seguidores:,.0f}"
        },
        {
            'label': 'Investimento Total',
            'value': CursorRules.format_currency(total_investimento)
        },
        {
            'label': 'Média de Engajamento',
            'value': CursorRules.format_percentage(media_engajamento)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de seguidores
        fig_seguidores = ChartComponents.create_pie_chart(
            df_midias,
            values='Seguidores',
            names='Rede',
            title='Distribuição de Seguidores'
        )
        st.plotly_chart(fig_seguidores, use_container_width=True)
    
    with col2:
        # Gráfico de engajamento
        fig_engajamento = ChartComponents.create_bar_chart(
            df_midias,
            x='Rede',
            y='Engajamento',
            title='Taxa de Engajamento por Rede'
        )
        st.plotly_chart(fig_engajamento, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_midias, ['Investimento'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['Engajamento'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 