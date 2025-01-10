"""
Dashboard de Performance de Vendas
"""
import streamlit as st
import pandas as pd
import logging
from datetime import datetime
from shared.utils.cursor_rules import CursorRules
from shared.components.layouts import DashboardLayout
from shared.components.filters import DateFilters
from modules.comercial.services.api_service import ComercialAPIService
from .sales_vs_target import create_sales_vs_target_chart
from .monthly_growth import create_monthly_growth_chart
import locale
import calendar

logger = logging.getLogger(__name__)

# Configura locale para português brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def calcular_meta_anual(df: pd.DataFrame, percentual_aumento: float) -> float:
    """Calcula meta anual baseada no faturamento total do ano anterior + percentual"""
    ano_atual = datetime.now().year
    
    # Extrai ano da data de emissão
    df = df.copy()
    df['ano'] = pd.to_datetime(df['emissao']).dt.year
    
    # Filtra ano anterior
    df_ano_anterior = df[df['ano'] == ano_atual - 1]
    
    if df_ano_anterior.empty:
        return 0
        
    faturamento_total = df_ano_anterior['valorfaturado'].sum()
    meta_anual = faturamento_total * (1 + percentual_aumento/100)
    return meta_anual / 12  # Divide por 12 para distribuir igualmente entre os meses

def formatar_valor_br(valor: float) -> str:
    """Formata valor monetário no padrão brasileiro"""
    return locale.currency(valor, grouping=True, symbol='R$')

def render_performance():
    """Renderiza o dashboard de Performance de Vendas"""
    ano_atual = datetime.now().year
    
    # Título com ano dinâmico
    st.header(f"📈 Performance de Vendas")
    st.subheader(f"Meta para {ano_atual}")
    
    # Botão Voltar
    st.markdown("[← Voltar para Home](Home)")
    
    # Slider para definir meta
    meta_percentual = st.slider(
        "Percentual de aumento para Meta",
        min_value=0,
        max_value=100,
        value=10,
        step=10,
        help="Define o percentual de aumento sobre o faturamento do ano anterior"
    )
    
    try:
        # Carrega dados
        api_service = ComercialAPIService()
        df_vendas = api_service.get_data()
        
        if df_vendas is None or df_vendas.empty:
            st.error('Não foi possível carregar os dados.')
            return
            
        # Extrai ano e mês da data de emissão
        df_vendas['emissao'] = pd.to_datetime(df_vendas['emissao'])
        df_vendas['ano'] = df_vendas['emissao'].dt.year
        df_vendas['mes'] = df_vendas['emissao'].dt.month
        
        # Calcula meta mensal (valor fixo para todos os meses)
        meta_mensal = calcular_meta_anual(df_vendas, meta_percentual)
        
        # Cria DataFrame base com todos os meses
        meses_completos = pd.DataFrame({
            'mes': range(1, 13),
            'nome_mes': [calendar.month_name[i].capitalize() for i in range(1, 13)]
        })
        
        # Prepara dados do ano atual
        df_atual = df_vendas[df_vendas['ano'] == ano_atual].copy()
        
        if df_atual.empty:
            df_mensal = meses_completos.copy()
            df_mensal['valorfaturado'] = 0.0
        else:
            df_temp = df_atual.groupby('mes')['valorfaturado'].sum().reset_index()
            df_mensal = pd.merge(meses_completos, df_temp, on='mes', how='left')
            df_mensal['valorfaturado'] = df_mensal['valorfaturado'].fillna(0.0)
        
        # Adiciona meta fixa para todos os meses
        df_mensal['meta'] = meta_mensal
        
        # Prepara DataFrame para os gráficos
        df_graficos = pd.DataFrame({
            'Mês': df_mensal['nome_mes'],  # Usa nome do mês em vez do número
            'Vendas': df_mensal['valorfaturado'],
            'Meta': df_mensal['meta'],
            'Crescimento': df_mensal['valorfaturado'].pct_change().fillna(0) * 100
        })
        
        # KPIs (mesmo com valores zerados)
        total_vendas = df_mensal['valorfaturado'].sum()
        media_vendas = df_mensal['valorfaturado'].mean()
        crescimento_total = 0  # Quando não há vendas, crescimento é zero
        
        # Layout de métricas
        metrics = [
            {
                'label': 'Total de Vendas',
                'value': CursorRules.format_currency(total_vendas)
            },
            {
                'label': 'Média Mensal',
                'value': CursorRules.format_currency(media_vendas)
            },
            {
                'label': 'Crescimento',
                'value': CursorRules.format_percentage(crescimento_total/100)
            }
        ]
        DashboardLayout.create_metric_row(metrics)
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            fig_vendas = create_sales_vs_target_chart(df_graficos)
            if fig_vendas:
                st.plotly_chart(fig_vendas, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de vendas vs meta')
        
        with col2:
            fig_crescimento = create_monthly_growth_chart(df_graficos)
            if fig_crescimento:
                st.plotly_chart(fig_crescimento, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de crescimento')
                
    except Exception as e:
        logger.error(f'Erro detalhado: {str(e)}', exc_info=True)
        st.error('Erro ao processar os dados. Verifique os logs para mais detalhes.')