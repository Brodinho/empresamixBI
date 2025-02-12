import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Indicadores Financeiros")
    
    # Dados de exemplo
    df_indicadores = pd.DataFrame({
        'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
        'Liquidez_Corrente': [1.5, 1.6, 1.8, 1.7, 1.9, 2.0],
        'ROE': [0.15, 0.16, 0.18, 0.17, 0.19, 0.20],
        'Margem_EBITDA': [0.22, 0.23, 0.25, 0.24, 0.26, 0.27],
        'Endividamento': [0.45, 0.43, 0.40, 0.38, 0.35, 0.33]
    })
    
    # KPIs
    liquidez_atual = df_indicadores['Liquidez_Corrente'].iloc[-1]
    roe_atual = df_indicadores['ROE'].iloc[-1]
    ebitda_atual = df_indicadores['Margem_EBITDA'].iloc[-1]
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Liquidez Corrente',
            'value': f"{liquidez_atual:.2f}"
        },
        {
            'label': 'ROE',
            'value': CursorRules.format_percentage(roe_atual)
        },
        {
            'label': 'Margem EBITDA',
            'value': CursorRules.format_percentage(ebitda_atual)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de evolução dos indicadores
        fig_evolucao = ChartComponents.create_line_chart(
            df_indicadores,
            x='Mês',
            y=['Liquidez_Corrente', 'ROE', 'Margem_EBITDA'],
            title='Evolução dos Indicadores'
        )
        st.plotly_chart(fig_evolucao, use_container_width=True)
    
    with col2:
        # Gráfico de endividamento
        fig_endividamento = ChartComponents.create_bar_chart(
            df_indicadores,
            x='Mês',
            y='Endividamento',
            title='Índice de Endividamento'
        )
        st.plotly_chart(fig_endividamento, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_percentage(
        df_indicadores, 
        ['ROE', 'Margem_EBITDA', 'Endividamento']
    )
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 