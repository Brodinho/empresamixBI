import os
import shutil
from pathlib import Path

def disable_pages():
    """Desabilita o sistema de páginas do Streamlit"""
    # Remove a pasta .streamlit/pages se existir
    pages_dir = Path(".streamlit/pages")
    if pages_dir.exists():
        shutil.rmtree(pages_dir)
    
    # Cria arquivo de configuração que desabilita páginas
    config = """
[server]
enableStaticServing = false
runOnSave = false

[browser]
gatherUsageStats = false

[client]
toolbarMode = "minimal"
showErrorDetails = false

[runner]
fastRerunEnabled = true
magicEnabled = false

[theme]
base = "dark"

[logger]
level = "error"
    """
    
    Path(".streamlit/config.toml").write_text(config)
    
    # Força variáveis de ambiente
    os.environ["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "false"
    os.environ["STREAMLIT_SERVER_RUN_ON_SAVE"] = "false"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

def setup_module_pages():
    """Configura as páginas do módulo"""
    disable_pages()

# Executar ao iniciar a aplicação
if __name__ == "__main__":
    setup_module_pages() 