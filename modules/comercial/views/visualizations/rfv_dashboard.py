import dash_bootstrap_components as dbc
from dash import html
import streamlit as st
import pandas as pd
from ...services.api_service import ComercialAPIService
from ...components.rfv_analysis import RFVAnalysis
from shared.utils.formatters import format_number, format_currency
from shared.utils.visualizations.insights_cards import render_metrics_section

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

def render_rfv():
    """Renderiza a visualização de análise RFV"""
    try:
        # Obtém os dados
        api_service = ComercialAPIService()
        df = api_service.get_rfv_data()
        
        # Título da seção
        st.markdown("## 💎 Análise RFV")
        
        # Expander explicativo
        with st.expander("ℹ️ O que é análise RFV?", expanded=False):
            st.markdown("""
                A **Análise RFV** (Recência, Frequência e Valor) é uma técnica que avalia o comportamento 
                dos clientes com base em três métricas principais:
                
                - **Recência**: Há quanto tempo foi a última compra
                - **Frequência**: Quantas compras foram realizadas
                - **Valor**: Qual o ticket médio das compras
            """)
        
        # Calcula métricas
        media_recencia = df['ultima_compra_dias'].mean()
        media_frequencia = df['quantidade_compras'].mean()
        ticket_medio = df['valor_total_compras'].mean()
        
        # Configuração das métricas para os cards
        metrics = {
            'media_recencia': {
                'title': '📅 Média de Recência',
                'value': media_recencia,
                'formatter': 'number',
                'suffix': ' dias',
                'decimals': 0,
                'help_text': 'Média de dias desde a última compra dos clientes',
                'positive_is_good': False
            },
            'media_frequencia': {
                'title': '🔄 Média de Frequência',
                'value': media_frequencia,
                'formatter': 'number',
                'suffix': ' compras',
                'decimals': 1,
                'help_text': 'Média de compras por cliente no período',
                'positive_is_good': True
            },
            'ticket_medio': {
                'title': '💰 Ticket Médio',
                'value': ticket_medio,
                'formatter': 'currency',
                'help_text': 'Valor médio das compras por cliente',
                'positive_is_good': True
            }
        }
        
        # Renderiza os cards de métricas
        render_metrics_section('', metrics, columns=3)
        
        # Separador
        st.markdown("---")
        
        # Gráficos RFV
        st.subheader("📊 Distribuição da Recência")
        fig_recencia = criar_grafico_recencia(df)
        if fig_recencia:
            st.plotly_chart(fig_recencia, use_container_width=True)
        
        # Layout em duas colunas para os outros gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Distribuição da Frequência")
            fig_frequencia = criar_grafico_frequencia(df)
            if fig_frequencia:
                st.plotly_chart(fig_frequencia, use_container_width=True)
        
        with col2:
            st.subheader("💰 Distribuição do Valor")
            fig_valor = criar_grafico_valor(df)
            if fig_valor:
                st.plotly_chart(fig_valor, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro ao renderizar análise RFV: {str(e)}") 