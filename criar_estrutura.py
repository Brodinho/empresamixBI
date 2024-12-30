import os
import shutil

def criar_estrutura():
    # Diretório raiz
    root_dir = "EMPRESAMIXBI"
    
    # Criar diretório raiz se não existir
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    # Estrutura de diretórios
    diretorios = [
        ".streamlit",
        "assets",
        "config",
        "dashboards_comercial",
        "dashboards_financeiro", 
        "dashboards_rh",
        "pages",
        "src",
        "src/analysis",
        "src/api",
        "src/database",
        "src/etl",
        "src/reports",
        "src/utils",
        "styles",
        "utils",
        "utils/common"
    ]

    # Criar diretórios
    for dir in diretorios:
        path = os.path.join(root_dir, dir)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Diretório criado: {path}")

    # Criar arquivos básicos
    arquivos = {
        ".streamlit/config.toml": """[theme]
base="dark"
primaryColor="#FF4B4B"
backgroundColor="#0E1117"
secondaryBackgroundColor="#1B1B1B"
textColor="#FAFAFA"
font="sans serif"
""",
        "config/settings.py": """import os
from dotenv import load_dotenv

load_dotenv()

APP_CONFIG = {
    'debug': True,
    'api_url': os.getenv('API_URL'),
    'api_key': os.getenv('API_KEY')
}

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}
""",
        "config/__init__.py": "",
        "dashboards_comercial/__init__.py": "",
        "dashboards_financeiro/__init__.py": "",
        "dashboards_rh/__init__.py": "",
        "src/main.py": """import streamlit as st
from config.settings import APP_CONFIG
from utils.auth import check_authentication

def main():
    if check_authentication():
        st.success("Autenticado com sucesso!")
    else:
        st.error("Falha na autenticação")

if __name__ == "__main__":
    main()
""",
        "src/__init__.py": "",
        "src/analysis/__init__.py": "",
        "src/api/__init__.py": "",
        "src/database/__init__.py": "",
        "src/etl/__init__.py": "",
        "src/reports/__init__.py": "",
        "src/utils/__init__.py": "",
        "utils/__init__.py": "",
        "utils/common/__init__.py": "",
        "Home.py": """import streamlit as st

st.set_page_config(
    page_title="EmpresaMix BI",
    page_icon="📊",
    layout="wide"
)

st.title("EmpresaMix BI - Dashboard")
""",
        "requirements.txt": """pandas==2.0.3
numpy==1.24.4
matplotlib==3.7.5
plotly==5.24.1
streamlit==1.29.0
python-dotenv==1.0.0
""",
        ".gitignore": """venv/
__pycache__/
.env
.idea/
*.pyc
.DS_Store
"""
    }

    # Criar arquivos
    for file_path, content in arquivos.items():
        full_path = os.path.join(root_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        if not os.path.exists(full_path):
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Arquivo criado: {full_path}")

    print("\nEstrutura do projeto criada com sucesso!")

if __name__ == "__main__":
    criar_estrutura()