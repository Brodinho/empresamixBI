import streamlit as st
from ...components import TerritoryMap, RegionRanking
from ...services.api_service import ComercialAPIService
from shared.utils.formatters import format_currency, format_percentage, format_tooltip_currency

def create_metrics_section(df):
    """Cria seção de métricas no topo do dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    # Cálculos das métricas
    total_faturamento = df['faturamento'].sum()
    
    # Separar mercado interno e externo
    df_interno = df[df['tipo_venda'] == 'INTERNO']
    df_externo = df[df['tipo_venda'] == 'EXTERNO']
    
    faturamento_interno = df_interno['faturamento'].sum()
    faturamento_externo = df_externo['faturamento'].sum()
    
    # Contagem de territórios
    total_estados = len(df_interno['location_name'].unique())
    total_paises = len(df_externo['location_name'].unique())
    
    with col1:
        help_text = (
            f"Detalhamento:\n"
            f"• Estados: {total_estados} de 27 estados brasileiros\n"
            f"• Paises: {total_paises} paises atendidos"
        )
        st.metric(
            "Territorios Atendidos",
            f"{total_estados + total_paises} regioes",
            help=help_text
        )
    
    with col2:
        help_text = (
            f"Composicao do Faturamento:\n"
            f"• Interno: {format_tooltip_currency(faturamento_interno)}\n"
            f"• Exportacao: {format_tooltip_currency(faturamento_externo)}"
        )
        st.metric(
            "Faturamento Total",
            format_currency(total_faturamento),
            help=help_text
        )
    
    with col3:
        help_text = (
            f"Crescimento por Mercado:\n"
            f"• Interno: {format_tooltip_currency(faturamento_interno)}\n"
            f"• Exportacao: {format_tooltip_currency(faturamento_externo)}\n\n"
            f"Total: {format_tooltip_currency(total_faturamento)}"
        )
        st.metric(
            "Crescimento Anual",
            format_percentage(faturamento_externo/total_faturamento),
            "vs Mercado Total",
            help=help_text
        )
    
    with col4:
        proporcao_interno = faturamento_interno/total_faturamento
        help_text = (
            f"Distribuicao do Faturamento:\n"
            f"• Mercado Interno: {format_tooltip_currency(faturamento_interno)} ({format_percentage(proporcao_interno)})\n"
            f"• Exportacao: {format_tooltip_currency(faturamento_externo)} ({format_percentage(1-proporcao_interno)})\n\n"
            f"Exportacao representa {format_percentage(faturamento_externo/faturamento_interno)} do mercado interno"
        )
        st.metric(
            "Mercado Interno",
            format_percentage(proporcao_interno),
            help=help_text
        )

def render_analise_territorial():
    """Renderiza a página de análise territorial"""
    
    st.title("Análise Territorial")
    
    try:
        # Obtém os dados
        df = ComercialAPIService.get_vendas_mapa()
        
        # Adiciona a seção de métricas antes do mapa
        create_metrics_section(df)
        
        # Cria o layout com duas colunas
        col1, col2 = st.columns([2, 1])  # Proporção 2:1
        
        with col1:
            # Renderiza o mapa
            territory_map = TerritoryMap.create_scatter_mapbox(df)
            st.plotly_chart(
                territory_map,
                use_container_width=True,
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToAdd': ['fullscreen']
                }
            )
            
        with col2:
            # Renderiza o ranking
            region_ranking = RegionRanking.create_ranking_chart(df)
            st.plotly_chart(
                region_ranking,
                use_container_width=True,
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToAdd': ['fullscreen']
                }
            )
            
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}") 