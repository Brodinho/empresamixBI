import streamlit as st
import pandas as pd
from shared.utils.cursor_utils import CursorUtils
from shared.components.charts import ChartComponents

def render_territorio():
    """Renderiza o dashboard de Análise Territorial"""
    # Remove padding
    st.markdown("""
        <style>
            .block-container {
                padding: 0rem !important;
            }
            .element-container {
                padding: 0.5rem !important;
            }
            div[data-testid="stVerticalBlock"] {
                padding: 0rem !important;
            }
            div[data-testid="stHorizontalBlock"] {
                padding: 0rem !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.header("📍 Análise de Território")
    
    # KPIs principais
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Vendas", "R$ 1.450,00M", "+8%")
    with col2:
        st.metric("Meta Total", "R$ 1.530,00M", "")
    with col3:
        st.metric("Atingimento Geral", "94.8%", "-2.2%")
    
    # Gráficos de análise
    col1, col2 = st.columns(2)
    
    with col1:
        # Dados de exemplo - Vendas vs Meta por Região
        df_vendas_meta = pd.DataFrame({
            'Região': ['Sul', 'Sudeste', 'Norte', 'Nordeste', 'Centro-Oeste'],
            'Vendas': [280, 520, 150, 320, 180],
            'Meta': [300, 500, 180, 350, 200]
        })
        
        fig_vendas = ChartComponents.create_bar_chart(
            df_vendas_meta,
            x='Região',
            y=['Vendas', 'Meta'],
            title='Vendas vs Meta por Região'
        )
        st.plotly_chart(fig_vendas, use_container_width=True)
    
    with col2:
        # Dados de exemplo - Atingimento por Região
        df_atingimento = pd.DataFrame({
            'Região': ['Sul', 'Sudeste', 'Norte', 'Nordeste', 'Centro-Oeste'],
            'Atingimento': [0.93, 1.04, 0.83, 0.91, 0.90]
        })
        
        fig_atingimento = ChartComponents.create_line_chart(
            df_atingimento,
            x='Região',
            y=['Atingimento'],
            title='Atingimento por Região'
        )
        st.plotly_chart(fig_atingimento, use_container_width=True)
    
    # Detalhamento com paginação
    st.subheader("Detalhamento por Região")
    try:
        # Dados de exemplo para o detalhamento
        df_detalhamento = pd.DataFrame({
            'Região': ['Sul', 'Sudeste', 'Norte', 'Nordeste', 'Centro-Oeste'] * 4,
            'Vendedor': ['João', 'Maria', 'Pedro', 'Ana', 'Carlos'] * 4,
            'Vendas': [100, 150, 80, 120, 90] * 4,
            'Meta': [120, 140, 100, 130, 100] * 4,
            'Atingimento': ['83%', '107%', '80%', '92%', '90%'] * 4
        })
        
        # Configuração da paginação
        items_per_page = 10
        total_items = len(df_detalhamento)
        page = st.number_input('Página', min_value=1, value=1)
        
        # Calcula os índices de início e fim
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)
        
        # Aplica a paginação
        df_paged = df_detalhamento.iloc[start_idx:end_idx]
        
        # Exibe o dataframe paginado
        st.dataframe(df_paged, use_container_width=True)
        
        # Exibe informações da paginação
        st.caption(f"Mostrando {start_idx + 1} a {end_idx} de {total_items} registros")
        
    except Exception as e:
        st.error(f"Erro ao carregar o detalhamento: {str(e)}")
        st.error("Por favor, contate o suporte técnico.") 