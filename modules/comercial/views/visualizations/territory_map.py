"""
Visualização do Mapa Territorial
"""
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import logging
from shared.utils.formatters import format_currency

logger = logging.getLogger(__name__)

# Dicionário de coordenadas das UFs e países
COORDENADAS = {
    # Estados do Brasil
    'AC': {'lat': -9.0238, 'lon': -70.812},
    'AL': {'lat': -9.5713, 'lon': -36.782},
    'AM': {'lat': -3.4168, 'lon': -65.8561},
    'AP': {'lat': 1.4099, 'lon': -51.7695},
    'BA': {'lat': -12.2846, 'lon': -41.6809},
    'CE': {'lat': -5.4984, 'lon': -39.3206},
    'DF': {'lat': -15.7801, 'lon': -47.9292},
    'ES': {'lat': -19.1834, 'lon': -40.3089},
    'GO': {'lat': -15.827, 'lon': -49.8362},
    'MA': {'lat': -4.9609, 'lon': -45.2744},
    'MG': {'lat': -18.5122, 'lon': -44.555},
    'MS': {'lat': -20.7722, 'lon': -54.7852},
    'MT': {'lat': -12.6819, 'lon': -56.9211},
    'PA': {'lat': -5.5305, 'lon': -52.2907},
    'PB': {'lat': -7.24, 'lon': -36.782},
    'PE': {'lat': -8.8137, 'lon': -36.9541},
    'PI': {'lat': -7.7183, 'lon': -42.7289},
    'PR': {'lat': -25.2521, 'lon': -52.0215},
    'RJ': {'lat': -22.9099, 'lon': -43.2095},
    'RN': {'lat': -5.4026, 'lon': -36.9541},
    'RO': {'lat': -11.5057, 'lon': -63.5806},
    'RR': {'lat': 2.7376, 'lon': -62.0751},
    'RS': {'lat': -30.0346, 'lon': -51.2177},
    'SC': {'lat': -27.2423, 'lon': -50.2189},
    'SE': {'lat': -10.9091, 'lon': -37.0677},
    'SP': {'lat': -23.5505, 'lon': -46.6333},
    'TO': {'lat': -10.1753, 'lon': -48.2982},
}

def calculate_marker_size(value, min_val, max_val, min_size=8, max_size=40):
    """
    Calcula o tamanho do marcador usando escala logarítmica para melhor visualização
    das diferenças de faturamento
    """
    try:
        if pd.isna(value) or value <= 0:
            return min_size
            
        # Usa log para melhor distribuição dos tamanhos
        log_value = np.log10(value)
        log_min = np.log10(min_val) if min_val > 0 else 0
        log_max = np.log10(max_val)
        
        # Normaliza na escala logarítmica
        normalized = (log_value - log_min) / (log_max - log_min)
        
        # Aplica a escala de tamanho com uma curva mais acentuada
        size = min_size + (normalized ** 0.7) * (max_size - min_size)
        
        return size
        
    except Exception as e:
        logger.error(f"Erro ao calcular tamanho do marcador: {str(e)}")
        return min_size

def create_territory_map(df: pd.DataFrame) -> go.Figure:
    """Cria o mapa territorial"""
    try:
        # Separa vendas internas e externas
        df_interno = df[df['uf'] != 'EX'].groupby('uf')['valorfaturado'].sum().reset_index()
        df_externo = df[df['uf'] == 'EX'].groupby(['pais'])['valorfaturado'].sum().reset_index()
        
        # Encontra os valores mínimos e máximos globais para manter a escala consistente
        min_fat = min(df_interno['valorfaturado'].min(), df_externo['valorfaturado'].min())
        max_fat = max(df_interno['valorfaturado'].max(), df_externo['valorfaturado'].max())
        
        # Adiciona coordenadas e calcula tamanhos para vendas internas
        df_interno['lat'] = df_interno['uf'].map(lambda x: COORDENADAS.get(x, {}).get('lat', 0))
        df_interno['lon'] = df_interno['uf'].map(lambda x: COORDENADAS.get(x, {}).get('lon', 0))
        df_interno['size'] = df_interno['valorfaturado'].apply(
            lambda x: calculate_marker_size(x, min_fat, max_fat)
        )
        
        # Cria o mapa
        fig = go.Figure()
        
        # Adiciona marcadores para vendas internas
        fig.add_trace(go.Scattergeo(
            lon=df_interno['lon'],
            lat=df_interno['lat'],
            mode='markers',
            marker=dict(
                size=df_interno['size'],
                color='blue',
                opacity=0.7,
                line=dict(color='white', width=1)
            ),
            text=df_interno.apply(
                lambda x: f"Estado: {x['uf']}<br>Faturamento: {format_currency(x['valorfaturado'])}",
                axis=1
            ),
            name='Vendas Internas',
            hoverinfo='text',
            showlegend=True
        ))
        
        # Lista para armazenar todas as coordenadas externas
        lats_ext = []
        lons_ext = []
        sizes_ext = []
        texts_ext = []
        
        # Prepara dados de vendas externas
        for _, row in df_externo.iterrows():
            coords = get_country_coordinates(row['pais'])
            if coords:
                lats_ext.append(coords['lat'])
                lons_ext.append(coords['lon'])
                sizes_ext.append(calculate_marker_size(row['valorfaturado'], min_fat, max_fat))
                texts_ext.append(f"País: {row['pais']}<br>Faturamento: {format_currency(row['valorfaturado'])}")
        
        # Adiciona todos os marcadores externos em uma única trace
        if lats_ext:
            fig.add_trace(go.Scattergeo(
                lon=lons_ext,
                lat=lats_ext,
                mode='markers',
                marker=dict(
                    size=sizes_ext,
                    color='green',
                    opacity=0.7,
                    line=dict(color='white', width=1)
                ),
                text=texts_ext,
                name='Vendas Externas',
                hoverinfo='text',
                showlegend=True  # Mostra na legenda
            ))
        
        # Layout do mapa
        fig.update_layout(
            showlegend=True,
            legend=dict(
                itemsizing='constant',
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            geo=dict(
                scope='world',
                projection_type='equirectangular',
                showland=True,
                showocean=True,
                showcoastlines=True,
                showcountries=True,
                showsubunits=True,  # Mostra subdivisões (estados)
                subunitcolor='rgb(204, 204, 204)',  # Cor das linhas dos estados
                landcolor='rgb(243, 243, 243)',
                oceancolor='rgb(204, 229, 255)',
                countrycolor='rgb(150, 150, 150)',  # Cor mais escura para países
                coastlinecolor='rgb(150, 150, 150)',
                center=dict(lat=-15, lon=-47),
                lataxis=dict(range=[-60, 20]),
                lonaxis=dict(range=[-90, 50]),
            ),
            # Alterando para usar o mapa base com mais detalhes
            mapbox=dict(
                style='carto-positron',
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Erro ao criar mapa: {str(e)}")
        return None

def get_country_coordinates(country_name: str) -> dict:
    """
    Obtém as coordenadas de um país usando a API do OpenStreetMap
    """
    import requests
    import time
    
    try:
        # Cache para coordenadas já consultadas
        if not hasattr(get_country_coordinates, 'cache'):
            get_country_coordinates.cache = {}
            
        # Verifica se já está no cache
        if country_name in get_country_coordinates.cache:
            return get_country_coordinates.cache[country_name]
            
        # Consulta a API do Nominatim (OpenStreetMap)
        url = f"https://nominatim.openstreetmap.org/search?country={country_name}&format=json"
        response = requests.get(url, headers={'User-Agent': 'MixBI/1.0'})
        time.sleep(1)  # Respeita o limite de requisições
        
        if response.status_code == 200:
            data = response.json()
            if data:
                coords = {
                    'lat': float(data[0]['lat']),
                    'lon': float(data[0]['lon'])
                }
                get_country_coordinates.cache[country_name] = coords
                return coords
                
        return None
        
    except Exception as e:
        logger.error(f"Erro ao obter coordenadas do país {country_name}: {str(e)}")
        return None 