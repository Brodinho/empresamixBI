import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Fluxo de Caixa")
    
    # Dados de exemplo
    df_fluxo = pd.DataFrame({
        'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
        'Entradas': [250000.00, 280000.00, 310000.00, 290000.00, 320000.00, 350000.00],
        'Saídas': [200000.00, 230000.00, 240000.00, 250000.00, 260000.00, 280000.00],
        'Saldo': [50000.00, 50000.00, 70000.00, 40000.00, 60000.00, 70000.00]
    })
    
    # KPIs
    total_entradas = df_fluxo['Entradas'].sum()
    total_saidas = df_fluxo['Saídas'].sum()
    saldo_atual = df_fluxo['Saldo'].iloc[-1]
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total Entradas',
            'value': CursorRules.format_currency(total_entradas)
        },
        {
            'label': 'Total Saídas',
            'value': CursorRules.format_currency(total_saidas)
        },
        {
            'label': 'Saldo Atual',
            'value': CursorRules.format_currency(saldo_atual)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de entradas e saídas
        fig_fluxo = ChartComponents.create_bar_chart(
            df_fluxo,
            x='Mês',
            y=['Entradas', 'Saídas'],
            title='Entradas vs Saídas'
        )
        st.plotly_chart(fig_fluxo, use_container_width=True)
    
    with col2:
        # Gráfico de saldo
        fig_saldo = ChartComponents.create_line_chart(
            df_fluxo,
            x='Mês',
            y='Saldo',
            title='Evolução do Saldo'
        )
        st.plotly_chart(fig_saldo, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(
        df_fluxo, 
        ['Entradas', 'Saídas', 'Saldo']
    )
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 