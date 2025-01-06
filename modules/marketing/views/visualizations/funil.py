import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Funil de Marketing")
    
    # Dados de exemplo
    df_funil = pd.DataFrame({
        'Etapa': ['Visitantes', 'Leads', 'MQLs', 'SQLs', 'Oportunidades', 'Clientes'],
        'Quantidade': [10000, 2000, 1000, 500, 200, 100],
        'Taxa_Conversao': [1.00, 0.20, 0.50, 0.50, 0.40, 0.50],
        'Custo_Aquisicao': [1.00, 5.00, 10.00, 20.00, 50.00, 100.00]
    })
    
    # KPIs
    total_leads = df_funil.loc[df_funil['Etapa'] == 'Leads', 'Quantidade'].iloc[0]
    total_clientes = df_funil.loc[df_funil['Etapa'] == 'Clientes', 'Quantidade'].iloc[0]
    taxa_conversao_total = total_clientes / total_leads
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total de Leads',
            'value': f"{total_leads:,.0f}"
        },
        {
            'label': 'Clientes Convertidos',
            'value': f"{total_clientes:,.0f}"
        },
        {
            'label': 'Taxa de Conversão Total',
            'value': CursorRules.format_percentage(taxa_conversao_total)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de funil
        fig_funil = ChartComponents.create_bar_chart(
            df_funil,
            x='Quantidade',
            y='Etapa',
            title='Funil de Conversão',
            horizontal=True
        )
        st.plotly_chart(fig_funil, use_container_width=True)
    
    with col2:
        # Gráfico de custo de aquisição
        fig_cac = ChartComponents.create_line_chart(
            df_funil,
            x='Etapa',
            y='Custo_Aquisicao',
            title='Custo de Aquisição por Etapa'
        )
        st.plotly_chart(fig_cac, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_funil, ['Custo_Aquisicao'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['Taxa_Conversao'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 