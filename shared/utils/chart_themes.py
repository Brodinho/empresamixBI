from typing import Dict, Any

class ChartThemes:
    # Cores padrão para gráficos
    COLORS = {
        'primary': '#4A90E2',
        'secondary': '#E2844A',
        'success': '#4AE28D',
        'danger': '#E24A4A',
        'warning': '#E2C84A',
        'info': '#4AE2E2'
    }
    
    # Configurações padrão para gráficos
    CHART_CONFIG = {
        'template': 'plotly_dark',
        'font': {
            'family': 'Arial, sans-serif',
            'size': 12,
            'color': '#CCCCCC'
        },
        'paper_bgcolor': '#1E1E1E',
        'plot_bgcolor': '#1E1E1E',
        'showlegend': True
    }
    
    # Estilos para cards
    CARD_STYLES = {
        'padding': '20px',
        'border-radius': '10px',
        'background-color': '#1E1E1E',
        'margin': '10px 0'
    } 