import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

API_CONFIG = {
    'BASE_URL': os.getenv('VITE_API_URL', 'http://tecnolife.empresamix.info:8077/POWERBI'),
    'TIMEOUT': int(os.getenv('API_TIMEOUT', '30')),
    'PARAMS': {
        'CLIENTE': os.getenv('VITE_API_CLIENTE', 'TECNOLIFE'),
        'ID': os.getenv('VITE_API_ID', 'XIOPMANA'),
        'VIEW': os.getenv('VITE_API_VIEW', 'CUBO_FATURAMENTO')
    }
} 