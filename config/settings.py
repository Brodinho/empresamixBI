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
MODULES = [
    {
        "id": "comercial",
        "title": "Comercial",
        "description": "Gestão de vendas e pipeline comercial",
        "icon": "💼"
    },
    {
        "id": "financeiro",
        "title": "Financeiro",
        "description": "Controle financeiro e indicadores",
        "icon": "💰"
    },
    {
        "id": "marketing",
        "title": "Marketing",
        "description": "Campanhas e análise de marketing",
        "icon": "📢"
    },
    {
        "id": "operacional",
        "title": "Operacional",
        "description": "Gestão de operações e produção",
        "icon": "⚙️"
    },
    {
        "id": "pcp",
        "title": "PCP",
        "description": "Planejamento e controle da produção",
        "icon": "📋"
    },
    {
        "id": "rh",
        "title": "Recursos Humanos",
        "description": "Gestão de pessoas e desenvolvimento",
        "icon": "👥"
    }
]
