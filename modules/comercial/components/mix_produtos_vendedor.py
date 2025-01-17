import plotly.graph_objects as go
import pandas as pd
from shared.utils.formatters import format_currency
import logging

logger = logging.getLogger(__name__)

def criar_mix_produtos_vendedor(df: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico treemap do mix de produtos por vendedor
    
    Expander HTML:
    ℹ️ Como interpretar este gráfico?
    
    Este gráfico mostra a distribuição das vendas por categoria de produtos:
    
    📂 Níveis: Vendedor > Grupo > Subgrupo
    🎨 Cores: Quanto mais escuro, maior o valor
    📊 Tamanho: Proporcional ao valor faturado
    
    % do Total representa:
    • Vendedor: % do faturamento total do período
    • Grupo: % do total do vendedor
    • Subgrupo: % do total do grupo
    
    💡 Dica: Identifique a especialidade de cada vendedor e oportunidades de diversificação do mix de produtos.
    """
    try:
        print("\n=== DEBUG MIX PRODUTOS ===")
        print(f"1. DataFrame original: {df.shape} registros")
        print(f"Colunas disponíveis: {df.columns.tolist()}")
        print(f"Amostra dos dados originais:")
        print(df[['vendedor', 'grupo', 'subGrupo', 'valorfaturado']].head())
        
        # Limpeza dos dados
        df_clean = df.dropna(subset=['vendedor', 'grupo', 'subGrupo', 'valorfaturado'])
        print(f"\n2. Após limpeza: {df_clean.shape} registros")
        
        # Agrupamento dos dados
        df_mix = (df_clean.groupby(['vendedor', 'grupo', 'subGrupo'])
                 .agg({'valorfaturado': 'sum'})
                 .round(2)
                 .reset_index())
        
        print(f"\n3. Após agrupamento: {df_mix.shape} registros")
        print("Amostra dos dados agrupados:")
        print(df_mix.head())
        
        # Prepara as listas para o Treemap
        ids = []
        labels = []
        parents = []
        values = []
        
        # Adiciona vendedores (nível 1)
        for vendedor in df_mix['vendedor'].unique():
            valor_vendedor = df_mix[df_mix['vendedor'] == vendedor]['valorfaturado'].sum()
            ids.append(f"v_{vendedor}")
            labels.append(f"{vendedor}<br>{format_currency(valor_vendedor)}")
            parents.append("")
            values.append(valor_vendedor)
            
            # Adiciona grupos (nível 2)
            for grupo in df_mix[df_mix['vendedor'] == vendedor]['grupo'].unique():
                valor_grupo = df_mix[(df_mix['vendedor'] == vendedor) & 
                                   (df_mix['grupo'] == grupo)]['valorfaturado'].sum()
                ids.append(f"g_{vendedor}_{grupo}")
                labels.append(f"{grupo}<br>{format_currency(valor_grupo)}")
                parents.append(f"v_{vendedor}")
                values.append(valor_grupo)
                
                # Adiciona subgrupos (nível 3)
                subgrupos = df_mix[(df_mix['vendedor'] == vendedor) & 
                                 (df_mix['grupo'] == grupo)]
                for _, row in subgrupos.iterrows():
                    ids.append(f"s_{vendedor}_{grupo}_{row['subGrupo']}")
                    labels.append(f"{row['subGrupo']}<br>{format_currency(row['valorfaturado'])}")
                    parents.append(f"g_{vendedor}_{grupo}")
                    values.append(row['valorfaturado'])
        
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
                colorscale=[
                    [0, '#e3f2fd'],      # Azul muito claro
                    [0.3, '#90caf9'],    # Azul claro
                    [0.6, '#2196f3'],    # Azul médio
                    [0.9, '#1976d2'],    # Azul escuro
                    [1, '#0d47a1']       # Azul muito escuro
                ],
                showscale=False
            ),
        ))
        
        print("\n5. Figura criada com sucesso")
        
        # Atualiza o layout
        fig.update_layout(
            title=dict(
                text="Mix de Produtos por Vendedor",
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
        
        print("6. Layout atualizado")
        print("=== FIM DEBUG ===\n")
        
        return fig
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        logger.error(f"Erro ao criar gráfico de mix de produtos: {str(e)}")
        return None 