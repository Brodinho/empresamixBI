import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import requests
import sys
from pathlib import Path
import locale

# Configurar locale para formatação de moeda
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def format_currency(value):
    """Formata valor para moeda brasileira"""
    try:
        return locale.currency(value, grouping=True, symbol=True)
    except:
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def load_data():
    """Carrega dados da API"""
    try:
        # Configuração da API
        api_url = "http://tecnolife.empresamix.info:8077/POWERBI"
        params = {
            "CLIENTE": "TECNOLIFE",
            "ID": "XIOPMANA",
            "VIEW": "CUBO_FATURAMENTO"
        }
        
        response = requests.get(api_url, params=params)
        
        if response.status_code != 200:
            st.error(f"Erro na API. Status code: {response.status_code}")
            return None
            
        data = response.json()
        df = pd.DataFrame(data)
        
        # Converter datas com tratamento de erros
        df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d', errors='coerce')
        
        # Remover registros com datas inválidas
        df = df.dropna(subset=['data'])
        
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar dados da API: {str(e)}")
        return None

def create_timeline(df, selected_years):
    """Cria o gráfico de timeline com os anos selecionados"""
    try:
        # Extrair ano e mês se ainda não existirem
        if 'ano' not in df.columns:
            df['ano'] = df['data'].dt.year
        if 'mes' not in df.columns:
            df['mes'] = df['data'].dt.month
        
        # Filtra dados pelos anos selecionados
        df_filtered = df[df['ano'].isin(selected_years)]
        
        # Calcula o valor máximo mensal
        df_mensal = df_filtered.groupby(['ano', 'mes'])['valorfaturado'].sum().reset_index()
        max_value = df_mensal['valorfaturado'].max()
        
        # Arredonda para o próximo milhão
        y_max = ((max_value // 1000000) + 1) * 1000000
        
        # Calcula os valores intermediários (de 1 em 1 milhão)
        y_ticks = []
        current_value = 0
        while current_value <= y_max:
            y_ticks.append(current_value)
            current_value += 1000000  # Incremento de 1 milhão
        
        # Cores para cada ano
        year_colors = {
            2021: '#1f77b4',  # Azul
            2022: '#ff7f0e',  # Laranja
            2023: '#2ca02c',  # Verde
            2024: '#d62728',  # Vermelho
            2025: '#9467bd',  # Roxo
        }
        
        # Cria o gráfico
        fig = go.Figure()
        
        # Para cada ano selecionado
        for year in selected_years:
            df_year = df_filtered[df_filtered['ano'] == year]
            
            # Agrupa por mês (soma todo faturamento)
            df_mensal = df_year.groupby('mes')['valorfaturado'].sum().reindex(range(1,13), fill_value=0)
            
            # Formata os valores para o hover
            hover_text = [f"Mês: {mes}<br>Faturamento: {format_currency(valor)}" 
                         for mes, valor in zip(range(1, 13), df_mensal.values)]
            
            # Adiciona linha ao gráfico
            fig.add_trace(go.Scatter(
                x=list(range(1, 13)),
                y=df_mensal.values,
                name=str(year),
                line=dict(
                    color=year_colors.get(year),
                    dash='solid'
                ),
                hovertext=hover_text,
                hoverinfo='text'
            ))
        
        # Configura o layout
        fig.update_layout(
            title='Evolução do Faturamento por Ano',
            xaxis=dict(
                title='Mês',
                tickmode='array',
                ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                tickvals=list(range(1, 13))
            ),
            yaxis=dict(
                title='Faturamento',
                range=[0, y_max],
                tickmode='array',
                tickvals=y_ticks,
                ticktext=[f'R$ {int(val/1000000)} Milhões' if val > 0 else 'R$ 0' for val in y_ticks],
                tickfont=dict(
                    color='white',
                    size=12
                ),
                showgrid=True,
                gridcolor='rgba(128,128,128,0.2)',
                showline=True,
                linecolor='rgba(128,128,128,0.2)',
                zeroline=True,
                zerolinecolor='rgba(128,128,128,0.2)'
            ),
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99,
                bgcolor="rgba(0,0,0,0.8)",
                font=dict(color="white")
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erro ao criar gráfico: {str(e)}")
        return None

if __name__ == "__main__":
    df = load_data()
    
    if df is not None:
        # Para teste, usando todos os anos disponíveis
        available_years = sorted(df['data'].dt.year.unique(), reverse=True)[-5:]
        
        fig = create_timeline(df, available_years)
        
        if fig:
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToAdd': ['fullscreen']
                }
            ) 