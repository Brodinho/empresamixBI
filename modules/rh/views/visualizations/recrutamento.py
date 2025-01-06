import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Recrutamento e Seleção")
    
    # Dados de exemplo
    df_recrutamento = pd.DataFrame({
        'Vaga': ['Analista', 'Desenvolvedor', 'Gerente', 'Técnico', 'Coordenador'],
        'Candidatos': [120, 150, 80, 100, 90],
        'Entrevistados': [30, 40, 25, 35, 28],
        'Aprovados': [5, 8, 3, 6, 4],
        'Custo_Processo': [5000.00, 6000.00, 8000.00, 4500.00, 5500.00]
    })
    
    # Calculando taxas
    df_recrutamento['Taxa_Entrevista'] = df_recrutamento['Entrevistados'] / df_recrutamento['Candidatos']
    df_recrutamento['Taxa_Aprovacao'] = df_recrutamento['Aprovados'] / df_recrutamento['Entrevistados']
    
    # KPIs
    total_candidatos = df_recrutamento['Candidatos'].sum()
    total_aprovados = df_recrutamento['Aprovados'].sum()
    custo_total = df_recrutamento['Custo_Processo'].sum()
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total Candidatos',
            'value': f"{total_candidatos:,.0f}"
        },
        {
            'label': 'Total Aprovados',
            'value': f"{total_aprovados:,.0f}"
        },
        {
            'label': 'Custo Total',
            'value': CursorRules.format_currency(custo_total)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de funil de recrutamento
        fig_funil = ChartComponents.create_bar_chart(
            df_recrutamento,
            x='Vaga',
            y=['Candidatos', 'Entrevistados', 'Aprovados'],
            title='Funil de Recrutamento'
        )
        st.plotly_chart(fig_funil, use_container_width=True)
    
    with col2:
        # Gráfico de taxas
        fig_taxas = ChartComponents.create_line_chart(
            df_recrutamento,
            x='Vaga',
            y=['Taxa_Entrevista', 'Taxa_Aprovacao'],
            title='Taxas de Conversão'
        )
        st.plotly_chart(fig_taxas, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_recrutamento, ['Custo_Processo'])
    df_formatted = CursorUtils.format_df_percentage(
        df_formatted, 
        ['Taxa_Entrevista', 'Taxa_Aprovacao']
    )
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 