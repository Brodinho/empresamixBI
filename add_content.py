import os

file_path = r'C:\empresamixBI\docs\guidelines\chart_development.md'

content = '''# Diretrizes para Desenvolvimento de Gráficos

## 1. Estrutura de Arquivos
### 1.1 Localização
- Todos os gráficos devem ser criados em `modules/comercial/components/`
- Um arquivo por gráfico
- Nome do arquivo em snake_case (ex: `vendas_por_regiao.py`)
...
'''  # Todo o conteúdo que mostrei anteriormente

# Escrever o conteúdo no arquivo
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Conteúdo adicionado com sucesso ao arquivo: {file_path}") 