import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Treinamento e Desenvolvimento")
    
    # Dados de exemplo
    df_treinamento = pd.DataFrame({
        'Treinamento': ['Liderança', 'Técnico', 'Compliance', 'Segurança', 'Qualidade'],
        'Participantes': [25, 40, 100, 80, 60],
        'Horas': [16, 24, 8, 12, 16],
        'Aproveitamento': [0.88, 0.92, 0.95, 0.90, 0.89],
        'Investimento': [12000.00, 15000.00, 8000.00, 6000.00, 9000.00]
    })
    
    # Calculando valores derivados
    df_treinamento['Custo_Hora'] = df_treinamento['Investimento'] / (df_treinamento['Participantes'] * df_treinamento['Horas'])
    
    # KPIs
    total_participantes = df_treinamento['Participantes'].sum()
    total_horas = (df_treinamento['Participantes'] * df_treinamento['Horas']).sum()
    investimento_total = df_treinamento['Investimento'].sum()
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total Participantes',
            'value': f"{total_participantes:,.0f}"
        },
        {
            'label': 'Total Horas',
            'value': f"{total_horas:,.0f}h"
        },
        {
            'label': 'Investimento Total',
            'value': CursorRules.format_currency(investimento_total)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de participantes e horas
        fig_participantes = ChartComponents.create_bar_chart(
            df_treinamento,
            x='Treinamento',
            y=['Participantes', 'Horas'],
            title='Participantes e Horas por Treinamento'
        )
        st.plotly_chart(fig_participantes, use_container_width=True)
    
    with col2:
        # Gráfico de aproveitamento
        fig_aproveitamento = ChartComponents.create_line_chart(
            df_treinamento,
            x='Treinamento',
            y='Aproveitamento',
            title='Taxa de Aproveitamento por Treinamento'
        )
        st.plotly_chart(fig_aproveitamento, use_container_width=True)
    
    # Gráfico adicional de custo por hora
    fig_custo = ChartComponents.create_bar_chart(
        df_treinamento,
        x='Treinamento',
        y='Custo_Hora',
        title='Custo por Hora/Participante'
    )
    st.plotly_chart(fig_custo, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(
        df_treinamento, 
        ['Investimento', 'Custo_Hora']
    )
    df_formatted = CursorUtils.format_df_percentage(
        df_formatted, 
        ['Aproveitamento']
    )
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 