import subprocess
import os

def init_git():
    """Inicializa o repositório Git e faz o primeiro commit."""
    try:
        # Inicializar repositório
        subprocess.run(["git", "init"])
        
        # Criar .gitignore
        gitignore_content = """
        __pycache__/
        *.py[cod]
        *$py.class
        .env
        .venv
        venv/
        ENV/
        .idea/
        .vscode/
        *.log
        """
        
        with open(".gitignore", "w") as f:
            f.write(gitignore_content.strip())
        
        # Adicionar todos os arquivos
        subprocess.run(["git", "add", "."])
        
        # Primeiro commit
        subprocess.run(["git", "commit", "-m", "Inicialização do projeto"])
        
        print("Repositório Git inicializado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao inicializar repositório Git: {str(e)}")

if __name__ == "__main__":
    init_git()
