import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents
from shared.components.layouts import DashboardLayout
from ..performance.timeline_faturamento import create_timeline, load_data

def render_performance():
    """Renderiza o dashboard de Performance de Vendas"""
    st.header("📈 Performance de Vendas")
    
    # Dados de exemplo
    df_vendas = pd.DataFrame({
        'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
        'Vendas': [150000.00, 165000.00, 180000.00, 175000.00, 190000.00, 200000.00],
        'Meta': [160000.00, 160000.00, 170000.00, 170000.00, 180000.00, 180000.00],
        'Crescimento': [0.00, 0.10, 0.09, -0.03, 0.09, 0.05]
    })
    
    # KPIs
    total_vendas = df_vendas['Vendas'].sum()
    media_vendas = df_vendas['Vendas'].mean()
    crescimento_total = (df_vendas['Vendas'].iloc[-1] / df_vendas['Vendas'].iloc[0] - 1)
    
    # Layout de métricas
    metrics = [
        {
            'label': 'Total de Vendas',
            'value': CursorRules.format_currency(total_vendas)
        },
        {
            'label': 'Média Mensal',
            'value': CursorRules.format_currency(media_vendas)
        },
        {
            'label': 'Crescimento',
            'value': CursorRules.format_percentage(crescimento_total)
        }
    ]
    DashboardLayout.create_metric_row(metrics)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de vendas vs meta
        fig_vendas = ChartComponents.create_line_chart(
            df_vendas,
            x='Mês',
            y=['Vendas', 'Meta'],
            title='Vendas vs Meta'
        )
        st.plotly_chart(fig_vendas, use_container_width=True)
    
    with col2:
        # Gráfico de crescimento
        fig_crescimento = ChartComponents.create_bar_chart(
            df_vendas,
            x='Mês',
            y='Crescimento',
            title='Crescimento Mensal'
        )
        st.plotly_chart(fig_crescimento, use_container_width=True)
    
    # Adiciona o gráfico de timeline após as duas colunas
    st.subheader("Evolução do Faturamento")
    
    # Carrega dados do faturamento
    df_faturamento = load_data()
    
    if df_faturamento is not None:
        # Obtém os últimos 5 anos disponíveis
        available_years = sorted(df_faturamento['data'].dt.year.unique(), reverse=True)[-5:]
        
        # Cria e exibe o gráfico de timeline
        fig_timeline = create_timeline(df_faturamento, available_years)
        if fig_timeline:
            st.plotly_chart(
                fig_timeline,
                use_container_width=True,
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToAdd': ['fullscreen']
                }
            )
    
    # Tabela de dados
    st.subheader("Detalhamento")
    df_formatted = CursorUtils.format_df_currency(df_vendas, ['Vendas', 'Meta'])
    df_formatted = CursorUtils.format_df_percentage(df_formatted, ['Crescimento'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df_formatted, page - 1, page_size=10)
    st.dataframe(df_paged, use_container_width=True) 