import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout

def render():
    st.title("Avaliação de Desempenho")
    
    # Dados de exemplo
    df_desempenho = pd.DataFrame({
        'Departamento': ['Comercial', 'TI', 'Operações', 'Marketing', 'RH'],
        'Media_Avaliacao': [0.85, 0.92, 0.88, 0.87, 0.90],
        'Meta_Atingida': [0.90, 0.95, 0.85, 0.88, 0.92],
        'Colaboradores': [20, 15, 30, 12, 8],
        'Bonus_Previsto': [50000.00, 45000.00, 75000.00, 35000.00, 25000.00]
    })
    
    # KPIs
    media_geral = df_desempenho['Media_Avaliacao'].mean()
    total_colaboradores = df_desempenho['Colaboradores'].sum()
    total_bonus = df_desempenho['Bonus_Previsto'].sum()
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Média Geral',
            'value': CursorRules.format_percentage(media_geral)
        },
        {
            'label': 'Total Colaboradores',
            'value': total_colaboradores
        },
        {
            'label': 'Total Bônus',
            'value': CursorRules.format_currency(total_bonus)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de avaliação vs meta
        fig_avaliacao = ChartComponents.create_bar_chart(
            df_desempenho,
            x='Departamento',
            y=['Media_Avaliacao', 'Meta_Atingida'],
            title='Avaliação vs Meta por Departamento'
        )
        st.plotly_chart(fig_avaliacao, use_container_width=True)
    
    with col2:
        # Gráfico de bônus
        fig_bonus = ChartComponents.create_bar_chart(
            df_desempenho,
            x='Departamento',
            y='Bonus_Previsto',
            title='Bônus Previsto por Departamento'
        )
        st.plotly_chart(fig_bonus, use_container_width=True)
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_desempenho, ['Bonus_Previsto'])
    df_formatted = CursorUtils.format_df_percentage(
        df_formatted, 
        ['Media_Avaliacao', 'Meta_Atingida']
    )
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page)
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 