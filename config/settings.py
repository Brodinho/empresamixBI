import os
from dotenv import load_dotenv

load_dotenv()

# Configurações da Aplicação
APP_NAME = "Empresamix BI"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Configurações da API
API_BASE_URL = os.getenv("API_BASE_URL", "http://tecnolife.empresamix.info:8077/POWERBI")
API_TIMEOUT = 30

# Configurações de Tema
THEME = {
    "primaryColor": "#FF4B4B",
    "backgroundColor": "#FFFFFF",
    "secondaryBackgroundColor": "#F0F2F6",
    "textColor": "#262730",
    "font": "sans serif"
}

# Configurações de Módulos
MODULES = {
    "comercial": {
        "name": "Comercial",
        "icon": "📊",
        "color": "#1f77b4",
        "dashboards": ["Performance de Vendas", "Análise de Pipeline", 
                      "Gestão de Leads/Oportunidades", "Análise de Território"]
    },
    "cliente": {
        "name": "Cliente",
        "icon": "👥",
        "color": "#ff7f0e",
        "dashboards": ["Satisfação do Cliente", "Análise de Churn", 
                      "Segmentação de Clientes", "Jornada do Cliente"]
    },
    # ... outros módulos
}
