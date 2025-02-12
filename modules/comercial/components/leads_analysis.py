import plotly.graph_objects as go
import pandas as pd
import logging
from shared.utils.formatters import format_number, format_percentage

logger = logging.getLogger(__name__)

class LeadsAnalysis:
    @staticmethod
    def create_conversion_funnel(df: pd.DataFrame) -> go.Figure:
        """Cria funil de conversão de leads"""
        try:
            # Calcula métricas do funil
            total_leads = int(len(df))
            leads_ativos = int(len(df[df['ativo'] == 1]))
            leads_convertidos = int(len(df[df['valorfaturado'].notna()]))
            
            # Calcula percentuais
            perc_ativos = (leads_ativos/total_leads*100)
            perc_convertidos = (leads_convertidos/total_leads*100)
            perc_convertidos_ativos = (leads_convertidos/leads_ativos*100) if leads_ativos > 0 else 0.0
            
            # Prepara os dados formatados para customdata
            customdata = [
                [format_number(total_leads), 100, 100],
                [format_number(leads_ativos), perc_ativos, 100],
                [format_number(leads_convertidos), perc_convertidos, perc_convertidos_ativos]
            ]
            
            fig = go.Figure(go.Funnel(
                y=['Total Leads', 'Leads Ativos', 'Leads Convertidos'],
                x=[total_leads, leads_ativos, leads_convertidos],
                textinfo="value+percent previous",
                customdata=customdata,
                hovertemplate="<b>%{y}</b><br>" +
                            "Quantidade: %{customdata[0]}<br>" +
                            "%{customdata[1]:.1f}% do total inicial<br>" +
                            "%{customdata[2]:.1f}% do nível anterior<br>" +
                            "<extra></extra>"
            ))
            
            fig.update_layout(
                title="Funil de Conversão de Leads",
                template='plotly_dark'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Erro ao criar funil de conversão: {str(e)}")
            return None

    @staticmethod
    def create_leads_by_region(df: pd.DataFrame) -> go.Figure:
        """Cria gráfico de distribuição de leads por UF"""
        try:
            # Usa uf_x que vem da tabela CLIENTE
            leads_by_uf = df.groupby('uf_x').size().reset_index(name='total')
            leads_by_uf = leads_by_uf.sort_values('total', ascending=True)  # Ordena por quantidade
            
            fig = go.Figure(data=[
                go.Bar(
                    x=leads_by_uf['total'],  # Quantidade no eixo X
                    y=leads_by_uf['uf_x'],   # Estados no eixo Y
                    orientation='h',          # Barras horizontais
                    text=leads_by_uf['total'],
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title="Distribuição de Leads por Estado",
                xaxis_title="Quantidade de Leads",
                yaxis_title="Estado",
                template='plotly_dark',
                height=400,  # Altura fixa para melhor visualização
                margin=dict(l=0, r=0, t=30, b=0)  # Ajuste das margens
            )
            
            return fig
            
        except Exception as e:
            print(f"Erro ao criar gráfico de leads por região: {str(e)}")
            return None 