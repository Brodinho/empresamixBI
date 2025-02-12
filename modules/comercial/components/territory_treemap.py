import plotly.graph_objects as go
import pandas as pd
from shared.utils.formatters import format_currency
import logging

logger = logging.getLogger(__name__)

def criar_treemap_territorial(df: pd.DataFrame, metrica: str = "Valor Faturado", nivel_detalhe: str = "Região > Estado > Cidade") -> go.Figure:
    """
    Cria gráfico treemap da distribuição territorial
    
    Expander HTML:
    ℹ️ Como interpretar este gráfico?
    
    Este gráfico mostra a distribuição geográfica das vendas:
    
    📂 Níveis: Região > Estado > Cidade
    🎨 Cores: Quanto mais escuro, maior o valor
    📊 Tamanho: Proporcional ao valor faturado
    
    % do Total representa:
    • Região: % do faturamento total
    • Estado: % do total da região
    • Cidade: % do total do estado
    
    💡 Dica: Identifique regiões com maior potencial e oportunidades de expansão territorial.
    
    Args:
        df: DataFrame com os dados
        metrica: Métrica a ser analisada ("Valor Faturado", "Quantidade", "Número de Clientes")
        nivel_detalhe: Nível de detalhe ("Região > Estado", "Estado > Cidade", "Região > Estado > Cidade")
    """
    try:
        # Debug prints
        print(f"Recebido - Métrica: {metrica}, Nível: {nivel_detalhe}")
        
        # Mapeia a métrica para a coluna correspondente
        colunas = {
            "Valor Faturado": "valorfaturado",
            "Quantidade": "quant",
            "Número de Clientes": "codcli"
        }
        
        coluna_valor = colunas.get(metrica)
        if not coluna_valor:
            raise ValueError(f"Métrica não reconhecida: {metrica}")
            
        print(f"Coluna valor mapeada: {coluna_valor}")  # Debug
        
        # Define os níveis baseado na seleção
        niveis = {
            "Região > Estado": ['regiao', 'uf'],
            "Estado > Cidade": ['uf', 'cidade'],
            "Região > Estado > Cidade": ['regiao', 'uf', 'cidade']
        }[nivel_detalhe]
        
        print(f"Níveis selecionados: {niveis}")  # Debug
        
        # Verifica se as colunas existem no DataFrame
        colunas_necessarias = niveis + [coluna_valor]
        colunas_faltantes = [col for col in colunas_necessarias if col not in df.columns]
        if colunas_faltantes:
            raise ValueError(f"Colunas faltantes no DataFrame: {colunas_faltantes}")
            
        # Mostra as colunas disponíveis para debug
        print(f"Colunas disponíveis no DataFrame: {df.columns.tolist()}")
        
        # Limpeza e preparação dos dados
        df_clean = df.dropna(subset=niveis + [coluna_valor])
        
        # Agrupamento dos dados
        df_geo = (df_clean.groupby(niveis)
                 .agg({coluna_valor: 'nunique' if coluna_valor == 'codcli' else 'sum'})
                 .round(2)
                 .reset_index())
        
        # Prepara as listas para o Treemap
        ids = []
        labels = []
        parents = []
        values = []
        
        # Função para formatar o valor baseado na métrica
        def format_value(value):
            if coluna_valor == 'valorfaturado':
                return format_currency(value)
            elif coluna_valor == 'codcli':
                return f"{int(value)} clientes"
            else:
                return f"{int(value)} un"
        
        # Adiciona níveis conforme selecionado
        if nivel_detalhe == "Estado > Cidade":
            # Começa pelo estado
            for uf in df_geo['uf'].unique():
                valor_uf = df_geo[df_geo['uf'] == uf][coluna_valor].sum()
                ids.append(f"u_{uf}")
                labels.append(f"{uf}<br>{format_value(valor_uf)}")
                parents.append("")
                values.append(valor_uf)
                
                # Adiciona cidades
                for _, row in df_geo[df_geo['uf'] == uf].iterrows():
                    ids.append(f"c_{uf}_{row['cidade']}")
                    labels.append(f"{row['cidade']}<br>{format_value(row[coluna_valor])}")
                    parents.append(f"u_{uf}")
                    values.append(row[coluna_valor])
        else:
            # Adiciona regiões (se aplicável)
            if 'regiao' in niveis:
                for regiao in df_geo['regiao'].unique():
                    valor_regiao = df_geo[df_geo['regiao'] == regiao][coluna_valor].sum()
                    ids.append(f"r_{regiao}")
                    labels.append(f"{regiao}<br>{format_value(valor_regiao)}")
                    parents.append("")
                    values.append(valor_regiao)
                    
                    # Adiciona estados
                    for uf in df_geo[df_geo['regiao'] == regiao]['uf'].unique():
                        valor_uf = df_geo[
                            (df_geo['regiao'] == regiao) & 
                            (df_geo['uf'] == uf)
                        ][coluna_valor].sum()
                        ids.append(f"u_{regiao}_{uf}")
                        labels.append(f"{uf}<br>{format_value(valor_uf)}")
                        parents.append(f"r_{regiao}")
                        values.append(valor_uf)
                        
                        # Adiciona cidades se necessário
                        if 'cidade' in niveis:
                            cidades = df_geo[
                                (df_geo['regiao'] == regiao) & 
                                (df_geo['uf'] == uf)
                            ]
                            for _, row in cidades.iterrows():
                                ids.append(f"c_{regiao}_{uf}_{row['cidade']}")
                                labels.append(f"{row['cidade']}<br>{format_value(row[coluna_valor])}")
                                parents.append(f"u_{regiao}_{uf}")
                                values.append(row[coluna_valor])
        
        # Limpa qualquer figura anterior
        go.Figure().data = []
        
        # Cria o Treemap
        fig = go.Figure(go.Treemap(
            ids=ids,
            labels=labels,
            parents=parents,
            values=values,
            branchvalues='total',
            textinfo='label',
            hovertemplate=(
                "<b>%{label}</b><br>" +
                "% do Total: %{percentParent:.1f}%<br>" +
                "<extra></extra>"
            ),
            marker=dict(
                colors=values,
                colorscale='Teal',
                showscale=False
            ),
        ))
        
        # Atualiza o layout
        fig.update_layout(
            title=dict(
                text=f"Distribuição Territorial - {metrica}",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font=dict(size=20)
            ),
            width=1200,
            height=800,
            margin=dict(t=100, l=25, r=25, b=25),
            paper_bgcolor="#111111",
            plot_bgcolor="#111111",
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Erro ao criar treemap territorial: {str(e)}")
        return None 