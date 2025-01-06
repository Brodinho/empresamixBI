import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("DRE - Demonstração do Resultado")
    
    # Dados de exemplo
    df_dre = pd.DataFrame({
        'Conta': ['Receita Bruta', 'Deduções', 'Receita Líquida', 'CMV', 'Lucro Bruto', 'Despesas', 'Lucro Operacional'],
        'Valor': [1000000.00, -150000.00, 850000.00, -400000.00, 450000.00, -200000.00, 250000.00],
        'Margem': [1.00, 0.15, 0.85, 0.40, 0.45, 0.20, 0.25]
    })
    
    # KPIs
    receita_bruta = df_dre.loc[df_dre['Conta'] == 'Receita Bruta', 'Valor'].iloc[0]
    lucro_operacional = df_dre.loc[df_dre['Conta'] == 'Lucro Operacional', 'Valor'].iloc[0]
    margem_operacional = lucro_operacional / receita_bruta
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Receita Bruta',
            'value': CursorRules.format_currency(receita_bruta)
        },
        {
            'label': 'Lucro Operacional',
            'value': CursorRules.format_currency(lucro_operacional)
        },
        {
            'label': 'Margem Operacional',
            'value': CursorRules.format_percentage(margem_operacional)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de cascata
        fig_cascata = ChartComponents.create_bar_chart(
            df_dre,
            x='Conta',
            y='Valor',
            title='DRE em Cascata'
        )
        st.plotly_chart(fig_cascata, use_container_width=True)
    
    with col2:
        # Gráfico de margens
        fig_margens = ChartComponents.create_line_chart(
            df_dre,
            x='Conta',
            y='Margem',
            title='Análise de Margens'
        )
        st.plotly_chart(fig_margens, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_dre, ['Valor'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['Margem'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 