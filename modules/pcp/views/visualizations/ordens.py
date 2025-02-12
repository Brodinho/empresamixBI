import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Ordens de Produção")
    
    # Dados de exemplo
    df_ordens = pd.DataFrame({
        'OP': ['OP001', 'OP002', 'OP003', 'OP004', 'OP005'],
        'Produto': ['Prod A', 'Prod B', 'Prod C', 'Prod A', 'Prod B'],
        'Status': ['Em Produção', 'Aguardando', 'Finalizada', 'Em Produção', 'Finalizada'],
        'Progresso': [0.65, 0.00, 1.00, 0.45, 1.00],
        'Valor_Total': [25000.00, 18000.00, 32000.00, 22000.00, 19000.00]
    })
    
    # KPIs
    total_ordens = len(df_ordens)
    valor_total = df_ordens['Valor_Total'].sum()
    ordens_finalizadas = len(df_ordens[df_ordens['Status'] == 'Finalizada'])
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total de Ordens',
            'value': total_ordens
        },
        {
            'label': 'Valor Total',
            'value': CursorRules.format_currency(valor_total)
        },
        {
            'label': 'Finalizadas',
            'value': f"{ordens_finalizadas}/{total_ordens}"
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de status
        df_status = df_ordens['Status'].value_counts().reset_index()
        df_status.columns = ['Status', 'Quantidade']
        fig_status = ChartComponents.create_pie_chart(
            df_status,
            values='Quantidade',
            names='Status',
            title='Distribuição por Status'
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Gráfico de progresso
        fig_progresso = ChartComponents.create_bar_chart(
            df_ordens,
            x='OP',
            y='Progresso',
            title='Progresso por Ordem'
        )
        st.plotly_chart(fig_progresso, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_ordens, ['Valor_Total'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['Progresso'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 