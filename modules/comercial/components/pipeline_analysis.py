import plotly.graph_objects as go
import pandas as pd
from shared.utils.formatters import format_currency, format_number, format_percentage
from datetime import datetime, timedelta

class PipelineAnalysis:
    @staticmethod
    def create_funnel_chart(df: pd.DataFrame) -> go.Figure:
        """
        Cria o gráfico de funil do pipeline de vendas
        Mostra a quantidade de oportunidades em cada etapa
        """
        try:
            # Agrupa por status e conta as ocorrências
            status_counts = df.groupby('status').size().reset_index(name='count')
            total = status_counts['count'].sum()
            
            # Calcula os percentuais
            status_counts['percentage'] = status_counts['count'] / total * 100
            
            # Ordena conforme a sequência do funil
            status_order = ['Prospecção', 'Proposta', 'Negociação', 'Fechamento']
            status_counts = status_counts.set_index('status').reindex(status_order).reset_index()
            
            # Prepara os dados formatados para customdata
            customdata = [
                [format_number(count), format_percentage(perc)]
                for count, perc in zip(status_counts['count'], status_counts['percentage'])
            ]
            
            # Cria o gráfico de funil
            fig = go.Figure(go.Funnel(
                y=status_counts['status'],
                x=status_counts['count'],
                textposition="inside",
                textinfo="value+percent initial",
                opacity=0.65,
                marker={
                    "color": ["#2E5EAA", "#4373B9", "#5B8BC9", "#7AA3D9"],
                    "line": {"width": [2, 2, 2, 2], "color": ["white", "white", "white", "white"]}
                },
                connector={"line": {"color": "white", "dash": "solid", "width": 2}},
                customdata=customdata,
                hovertemplate="<b>%{y}</b><br>" +
                            "Quantidade: %{customdata[0]}<br>" +
                            "Percentual: %{customdata[1]}<extra></extra>"
            ))
            
            # Atualiza o layout
            fig.update_layout(
                title_text="Funil de Vendas",
                showlegend=False,
                template='plotly_dark',
                height=400,
                margin=dict(t=30, l=0, r=0, b=0)
            )
            
            return fig
            
        except Exception as e:
            print(f"Erro ao criar gráfico de funil: {str(e)}")
            return None 

    @staticmethod
    def create_value_by_status_chart(df: pd.DataFrame) -> go.Figure:
        """
        Cria o gráfico de valor total por status do pipeline
        Mostra o valor monetário das oportunidades em cada etapa
        """
        try:
            # Agrupa por status e soma os valores
            status_values = df.groupby('status')['valor'].sum().reset_index()
            
            # Ordena conforme a sequência do pipeline
            status_order = ['Prospecção', 'Proposta', 'Negociação', 'Fechamento']
            status_values = status_values.set_index('status').reindex(status_order).reset_index()
            
            # Prepara os dados formatados para o hover
            hover_text = [
                f"Status: {status}<br>" +
                f"Valor Total: {format_currency(valor)}"
                for status, valor in zip(status_values['status'], status_values['valor'])
            ]
            
            # Cria o gráfico de barras horizontais
            fig = go.Figure(go.Bar(
                x=status_values['valor'],
                y=status_values['status'],
                orientation='h',
                text=[format_currency(v) for v in status_values['valor']],
                textposition='auto',
                hovertext=hover_text,
                hoverinfo='text',
                marker=dict(
                    color=['#2E5EAA', '#4373B9', '#5B8BC9', '#7AA3D9'],
                    line=dict(color='white', width=1)
                )
            ))
            
            # Atualiza o layout
            fig.update_layout(
                title_text="Valor Total por Status",
                showlegend=False,
                template='plotly_dark',
                height=400,
                xaxis_title="Valor Total",
                yaxis_title="Status",
                margin=dict(t=30, l=0, r=0, b=0),
                # Formata o eixo X para mostrar valores em reais
                xaxis=dict(
                    tickformat=",.0f",
                    tickprefix="R$ "
                )
            )
            
            return fig
            
        except Exception as e:
            print(f"Erro ao criar gráfico de valor por status: {str(e)}")
            return None 

    @staticmethod
    def create_conversion_trend_chart(df: pd.DataFrame) -> go.Figure:
        """
        Cria o gráfico de tendência de conversão ao longo do tempo
        Mostra a evolução das conversões por status
        """
        try:
            # Converte a coluna de data para datetime se necessário
            df['data_criacao'] = pd.to_datetime(df['data_criacao'])
            
            # Agrupa por data e status, conta as ocorrências
            daily_status = df.groupby([
                pd.Grouper(key='data_criacao', freq='D'),
                'status'
            ]).size().reset_index(name='count')
            
            # Cria o gráfico de linha
            fig = go.Figure()
            
            # Cores para cada status
            colors = {
                'Prospecção': '#2E5EAA',
                'Proposta': '#4373B9',
                'Negociação': '#5B8BC9',
                'Fechamento': '#7AA3D9'
            }
            
            # Adiciona uma linha para cada status
            for status in colors.keys():
                status_data = daily_status[daily_status['status'] == status]
                
                # Calcula média móvel de 7 dias
                status_data['moving_avg'] = status_data['count'].rolling(
                    window=7, min_periods=1).mean()
                
                fig.add_trace(go.Scatter(
                    x=status_data['data_criacao'],
                    y=status_data['moving_avg'],
                    name=status,
                    mode='lines',
                    line=dict(color=colors[status], width=2),
                    hovertemplate="Data: %{x|%d/%m/%Y}<br>" +
                                f"Status: {status}<br>" +
                                "Quantidade: %{y:.0f}<extra></extra>"
                ))
            
            # Atualiza o layout
            fig.update_layout(
                title_text="Tendência de Conversão (Média Móvel 7 dias)",
                showlegend=True,
                template='plotly_dark',
                height=400,
                xaxis_title="Data",
                yaxis_title="Quantidade de Oportunidades",
                margin=dict(t=30, l=0, r=0, b=0),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                # Formata datas no eixo X
                xaxis=dict(
                    tickformat="%d/%m/%Y",
                    tickangle=-45
                )
            )
            
            return fig
            
        except Exception as e:
            print(f"Erro ao criar gráfico de tendência de conversão: {str(e)}")
            return None 

    @staticmethod
    def create_sales_by_rep_chart(df: pd.DataFrame) -> go.Figure:
        """
        Cria o gráfico de distribuição de oportunidades por vendedor
        Mostra quantidade e valor total por vendedor
        """
        try:
            # Agrupa por vendedor e status
            vendedor_status = df.groupby(['vendedor', 'status']).agg({
                'valor': 'sum',
                'status': 'size'
            }).rename(columns={'status': 'count'}).reset_index()
            
            # Ordena vendedores por valor total
            ordem_vendedores = df.groupby('vendedor')['valor'].sum().sort_values(ascending=True).index
            
            # Cores para cada status
            colors = {
                'Prospecção': '#2E5EAA',
                'Proposta': '#4373B9',
                'Negociação': '#5B8BC9',
                'Fechamento': '#7AA3D9'
            }
            
            # Cria o gráfico de barras empilhadas
            fig = go.Figure()
            
            for status in ['Prospecção', 'Proposta', 'Negociação', 'Fechamento']:
                status_data = vendedor_status[vendedor_status['status'] == status]
                
                # Prepara os dados para hover
                hover_text = [
                    f"Vendedor: {vendedor}<br>" +
                    f"Status: {status}<br>" +
                    f"Quantidade: {format_number(count)}<br>" +
                    f"Valor Total: {format_currency(valor)}"
                    for vendedor, count, valor in zip(status_data['vendedor'], 
                                                    status_data['count'], 
                                                    status_data['valor'])
                ]
                
                fig.add_trace(go.Bar(
                    name=status,
                    x=status_data['vendedor'],
                    y=status_data['valor'],
                    text=[format_currency(v) for v in status_data['valor']],
                    textposition='auto',
                    hovertext=hover_text,
                    hoverinfo='text',
                    marker_color=colors[status]
                ))
            
            # Atualiza o layout
            fig.update_layout(
                title_text="Distribuição por Vendedor",
                barmode='stack',
                showlegend=True,
                template='plotly_dark',
                height=400,
                xaxis_title="Vendedor",
                yaxis_title="Valor Total (R$)",
                margin=dict(t=30, l=0, r=0, b=0),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                # Formata o eixo Y para mostrar valores em reais
                yaxis=dict(
                    tickformat=",.0f",
                    tickprefix="R$ "
                )
            )
            
            return fig
            
        except Exception as e:
            print(f"Erro ao criar gráfico de distribuição por vendedor: {str(e)}")
            return None 

    @staticmethod
    def create_time_in_stage_chart(df: pd.DataFrame) -> go.Figure:
        """
        Cria o gráfico de tempo médio em cada etapa do pipeline
        Mostra quanto tempo as oportunidades permanecem em cada status
        """
        try:
            # Calcula o tempo médio em cada status
            tempo_medio = df.groupby('status')['tempo_etapa'].mean().reset_index()
            
            # Ordena conforme a sequência do pipeline
            status_order = ['Prospecção', 'Proposta', 'Negociação', 'Fechamento']
            tempo_medio = tempo_medio.set_index('status').reindex(status_order).reset_index()
            
            # Prepara os dados para hover
            hover_text = [
                f"Status: {status}<br>" +
                f"Tempo Médio: {format_number(tempo, decimals=1)} dias"
                for status, tempo in zip(tempo_medio['status'], tempo_medio['tempo_etapa'])
            ]
            
            # Cria o gráfico de barras horizontais
            fig = go.Figure(go.Bar(
                x=tempo_medio['tempo_etapa'],
                y=tempo_medio['status'],
                orientation='h',
                text=[f"{format_number(v, decimals=1)} dias" for v in tempo_medio['tempo_etapa']],
                textposition='auto',
                hovertext=hover_text,
                hoverinfo='text',
                marker=dict(
                    color=['#2E5EAA', '#4373B9', '#5B8BC9', '#7AA3D9'],
                    line=dict(color='white', width=1)
                )
            ))
            
            # Atualiza o layout
            fig.update_layout(
                title_text="Tempo Médio por Etapa",
                showlegend=False,
                template='plotly_dark',
                height=400,
                xaxis_title="Tempo (dias)",
                yaxis_title="Status",
                margin=dict(t=30, l=0, r=0, b=0),
                # Formata o eixo X para mostrar dias
                xaxis=dict(
                    ticksuffix=" dias"
                )
            )
            
            return fig
            
        except Exception as e:
            print(f"Erro ao criar gráfico de tempo médio por etapa: {str(e)}")
            return None 