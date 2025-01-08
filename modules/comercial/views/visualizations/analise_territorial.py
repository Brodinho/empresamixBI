import streamlit as st
from ...components import TerritoryMap, RegionRanking
from ...services.api_service import ComercialAPIService
from shared.utils.formatters import format_currency, format_percentage

def create_metrics_section(df):
    """Cria seção de métricas no topo do dashboard"""
    
    # Adiciona o CSS personalizado
    st.markdown("""
        <style>
        div.stMetrics-container {
            background: #1E1E1E;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            margin: 10px 0;
        }
        
        div.stMetrics-row {
            display: flex;
            justify-content: space-between;
            gap: 20px;
        }
        
        div.stMetric-card {
            background: linear-gradient(145deg, #2A2A2A, #1E1E1E);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.2),
                       -5px -5px 15px rgba(255,255,255,0.05);
            flex: 1;
        }
        
        div.stMetric-title {
            color: #7DD87D;
            font-size: 0.9em;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        div.stMetric-value {
            color: white;
            font-size: 1.5em;
            margin-bottom: 5px;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        div.stMetric-value span.currency {
            font-size: 1em;
        }
        
        div.stMetric-delta {
            color: #7DD87D;
            font-size: 0.8em;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Cálculos das métricas
    total_faturamento = df['faturamento'].sum()
    df_interno = df[df['tipo_venda'] == 'INTERNO']
    df_externo = df[df['tipo_venda'] == 'EXTERNO']
    faturamento_interno = df_interno['faturamento'].sum()
    faturamento_externo = df_externo['faturamento'].sum()
    total_estados = len(df_interno['location_name'].unique())
    total_paises = len(df_externo['location_name'].unique())
    
    # Cria o HTML dos cards
    metrics_html = f"""
    <div class="stMetrics-container">
        <div class="stMetrics-row">
            <div class="stMetric-card">
                <div class="stMetric-title">Territórios Atendidos</div>
                <div class="stMetric-value">{total_estados + total_paises} regiões</div>
            </div>
            <div class="stMetric-card">
                <div class="stMetric-title">Faturamento Total</div>
                <div class="stMetric-value">{format_currency(total_faturamento)}</div>
            </div>
            <div class="stMetric-card">
                <div class="stMetric-title">Crescimento Anual</div>
                <div class="stMetric-value">{format_percentage(faturamento_externo/total_faturamento)}</div>
                <div class="stMetric-delta">↑ vs Mercado Total</div>
            </div>
            <div class="stMetric-card">
                <div class="stMetric-title">Mercado Interno</div>
                <div class="stMetric-value">{format_percentage(faturamento_interno/total_faturamento)}</div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(metrics_html, unsafe_allow_html=True)

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
            # Cria o mapa
            territory_map = TerritoryMap.create_scatter_mapbox(df)
            st.plotly_chart(territory_map, use_container_width=True)
        
        with col2:
            # Cria o ranking
            region_ranking = RegionRanking.create_ranking_chart(df)
            st.plotly_chart(region_ranking, use_container_width=True)
            
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}") 