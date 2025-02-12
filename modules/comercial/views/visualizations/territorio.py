import streamlit as st
from ...services.api_service import ComercialAPIService
from ...components.maps import TerritoryMap

def render_territorio():
    """Renderiza o dashboard de Análise Territorial"""
    try:
        # Carrega dados para o mapa
        df_mapa = ComercialAPIService.get_vendas_mapa()
        
        # Cria o mapa
        fig_mapa = TerritoryMap.create_scatter_mapbox(df_mapa)
        
        # Renderiza o mapa
        st.plotly_chart(fig_mapa, use_container_width=True)
        
        # ... resto do código ...
        
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        st.error("Por favor, verifique a conexão com a API.") 