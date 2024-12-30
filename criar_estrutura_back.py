import os

def criar_estrutura():
    # Diretórios principais
    diretorios = [
        '.streamlit',
        'assets',
        'config',
        'dashboards_comercial',
        'dashboards_financeiro',
        'dashboards_rh',
        'pages',
        'src',
        'styles',
        'utils',
        'utils/common',
        'src/analysis',
        'src/api',
        'src/database',
        'src/etl',
        'src/reports',
        'src/utils'
    ]

    # Criar diretórios
    for dir in diretorios:
        os.makedirs(dir, exist_ok=True)
        # Criar __init__.py em cada diretório
        if dir not in ['.streamlit', 'assets', 'styles']:
            with open(os.path.join(dir, '__init__.py'), 'w') as f:
                pass

    # Criar arquivos principais
    arquivos = {
        '.gitignore': '',
        'ComandosImportantes.txt': '',
        'Home.py': '',
        'README.md': '# Empresa Mix BI\n\nDescrição do projeto aqui.',
        'requirements.txt': '',
        'test_api.py': '',
        '.streamlit/config.toml': '',
        'config/settings.py': '',
        'pages/1_comercial.py': '',
        'pages/2_financeiro.py': '',
        'src/main.py': '',
        'styles/login.css': '',
        'utils/api_connector.py': '',
        'utils/auth.py': '',
        'utils/constants.py': '',
        'utils/data_handlers.py': '',
        'utils/data_processing.py': '',
        'utils/filters.py': '',
        'utils/formatters.py': '',
        'utils/layout.py': '',
        'utils/menu.py': '',
        'utils/theme_config.py': '',
        'utils/trends.py': '',
        'utils/visualizations.py': '',
        'utils/common/data_processing.py': '',
        'utils/common/imports.py': ''
    }

    # Criar arquivos
    for arquivo, conteudo in arquivos.items():
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)

    print("Estrutura de diretórios e arquivos criada com sucesso!")

if __name__ == "__main__":
    criar_estrutura() 