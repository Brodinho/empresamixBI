import os
import shutil
from pathlib import Path

def setup_module_pages():
    """Copia os arquivos main.py dos módulos para a pasta pages/"""
    # Cria pasta pages se não existir
    pages_dir = Path("pages")
    pages_dir.mkdir(exist_ok=True)
    
    # Para cada módulo, copia o arquivo main.py
    modules_dir = Path("modules")
    for module in modules_dir.iterdir():
        if module.is_dir():
            source = module / "views" / "pages" / "main.py"
            target = pages_dir / f"{module.name}_main.py"
            
            if source.exists():
                # Copia o arquivo
                shutil.copy2(source, target)
                
                # Modifica o conteúdo para adicionar redirecionamento
                with open(target, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Adiciona import e chamada da função no início do arquivo
                if "load_comercial_module()" not in content:
                    with open(target, 'w', encoding='utf-8') as f:
                        f.write(content)
                        f.write("\n\n# Carrega o módulo automaticamente\nload_comercial_module()")

# Executar ao iniciar a aplicação
if __name__ == "__main__":
    setup_module_pages() 