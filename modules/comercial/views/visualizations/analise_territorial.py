import streamlit as st
from ...components import TerritoryMap, RegionRanking
from ...services.api_service import ComercialAPIService

def render_analise_territorial():
    """Renderiza a página de análise territorial"""
    
    st.title("Análise Territorial")
    
    try:
        # Obtém os dados
        df = ComercialAPIService.get_vendas_mapa()
        
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