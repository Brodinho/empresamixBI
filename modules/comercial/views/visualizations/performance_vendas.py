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
from modules.comercial.components import TendenciaVendas

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

def prepare_data_for_chart(df: pd.DataFrame, meta_percentual: float) -> pd.DataFrame:
    """
    Prepara dados para o gráfico de vendas vs meta
    """
    try:
        df = df.copy()
        ano_atual = datetime.now().year
        
        if 'emissao' not in df.columns:
            return pd.DataFrame()
            
        df['emissao'] = pd.to_datetime(df['emissao'])
        df['ano'] = df['emissao'].dt.year
        df['mes'] = df['emissao'].dt.month
        
        # Cria DataFrame base com todos os meses de 2025
        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        
        df_mensal = pd.DataFrame({'mes': range(1, 13)})
        df_mensal['Mês'] = df_mensal['mes'].map(meses)
        
        # Pega vendas de 2025 (se houver)
        vendas_2025 = df[df['ano'] == ano_atual].groupby('mes')['valorfaturado'].sum().reset_index()
        
        # Merge com vendas (preenchendo zeros onde não há vendas)
        df_mensal = df_mensal.merge(vendas_2025, on='mes', how='left')
        df_mensal['Vendas'] = df_mensal['valorfaturado'].fillna(0)
        
        # Calcula meta baseada em 2024
        ano_anterior = ano_atual - 1
        faturamento_ano_anterior = df[df['ano'] == ano_anterior]['valorfaturado'].sum()
        
        if faturamento_ano_anterior > 0:
            meta_mensal = (faturamento_ano_anterior * (1 + meta_percentual/100)) / 12
        else:
            meta_mensal = 0
            
        df_mensal['Meta'] = meta_mensal
        
        return df_mensal[['Mês', 'Vendas', 'Meta']]
            
    except Exception as e:
        return pd.DataFrame()

def render_performance():
    """Renderiza o dashboard de Performance de Vendas"""
    try:
        # Título com ano dinâmico
        st.header(f"📈 Performance de Vendas")
        st.subheader(f"Meta para {datetime.now().year}")
        
        # Slider para definir meta
        meta_percentual = st.slider(
            "Percentual de aumento para Meta",
            min_value=0,
            max_value=100,
            value=10,
            step=10,
            help="Define o percentual de aumento sobre o faturamento do ano anterior"
        )
        
        # Carrega dados
        api_service = ComercialAPIService()
        df_vendas = api_service.get_data()
        
        if df_vendas is None or df_vendas.empty:
            st.error('Não foi possível carregar os dados.')
            return
            
        # Prepara dados para o gráfico
        df_graficos = prepare_data_for_chart(df_vendas, meta_percentual)
        
        if df_graficos.empty:
            st.error('Erro ao preparar dados para visualização.')
            return
            
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            fig_vendas = create_sales_vs_target_chart(df_graficos)
            if fig_vendas:
                st.plotly_chart(fig_vendas, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de vendas vs meta')
                
        # Adicionar o gráfico
        st.markdown("---")
        try:
            tendencia = TendenciaVendas.create_trend_chart(df_vendas)
            if tendencia:
                st.plotly_chart(tendencia, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de tendência')
        except Exception as e:
            st.error('Erro ao criar gráfico')
            logger.error(f'Erro: {str(e)}')
            
    except Exception as e:
        st.error(f"Erro ao renderizar dashboard: {str(e)}")