import dash_bootstrap_components as dbc
from dash import html

from modules.comercial.components.grafico_recencia import criar_grafico_recencia
from modules.comercial.components.grafico_frequencia import criar_grafico_frequencia
from modules.comercial.components.grafico_valor import criar_grafico_valor

def criar_layout_rfv(df):
    """
    Cria o layout da página de análise RFV
    """
    return html.Div([
        dbc.Row([
            html.H2("Análise RFV - Recência, Frequência e Valor", 
                   className="text-primary mb-4")
        ]),
        
        # Linha com cards informativos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📅 Recência Média", className="card-title"),
                        html.H3(f"{df['ultima_compra_dias'].mean():.0f} dias")
                    ])
                ])
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🔄 Frequência Média", className="card-title"),
                        html.H3(f"{df['quantidade_compras'].mean():.1f} compras")
                    ])
                ])
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("💰 Ticket Médio", className="card-title"),
                        html.H3(f"R$ {df['valor_total_compras'].mean():.2f}")
                    ])
                ])
            ], width=4),
        ], className="mb-4"),
        
        # Linha com os gráficos
        dbc.Row([
            dbc.Col([
                criar_grafico_recencia(df)
            ], width=12, className="mb-4"),
        ]),
        
        dbc.Row([
            dbc.Col([
                criar_grafico_frequencia(df)
            ], width=6),
            dbc.Col([
                criar_grafico_valor(df)
            ], width=6),
        ]),
    ], className="p-4") 