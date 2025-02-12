# Cores para o mapa
MAP_COLORS = {
    'INTERNO': '#1a237e',  # Azul escuro
    'EXTERNO': '#1b5e20'   # Verde escuro
}

# Configuração do mapa base
MAPBOX_CONFIG = {
    'style': 'carto-positron',
    'zoom': 3.5,
    'center': {'lat': -15.7801, 'lon': -47.9292}
}

# Template do hover
HOVER_TEMPLATE = "<b>%{hovertext}</b><br>Faturamento: %{customdata[0]}<extra></extra>" 