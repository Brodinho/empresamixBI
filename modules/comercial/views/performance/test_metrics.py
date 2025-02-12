import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = Path(__file__).parent.parent.parent.parent.parent
sys.path.append(str(root_dir))

from shared.utils.formatters import format_currency, format_percentage

def create_metrics_card():
    """Cria um card de métricas com layout personalizado"""
    
    # Dados de exemplo - Simulando dados territoriais
    df_metricas = pd.DataFrame({
        'Período': ['2023', '2024'],
        'Estados_Atendidos': [18, 22],
        'Paises_Atendidos': [3, 5],
        'Faturamento_Interno': [15000000.00, 18500000.00],
        'Faturamento_Exportacao': [2500000.00, 4000000.00]
    })
    
    # Cálculos das métricas
    ano_atual = df_metricas.iloc[-1]
    ano_anterior = df_metricas.iloc[-2]
    
    # Cálculos específicos
    total_territorios = ano_atual['Estados_Atendidos'] + ano_atual['Paises_Atendidos']
    faturamento_total = ano_atual['Faturamento_Interno'] + ano_atual['Faturamento_Exportacao']
    faturamento_anterior = ano_anterior['Faturamento_Interno'] + ano_anterior['Faturamento_Exportacao']
    
    # Variações e proporções
    var_faturamento = (faturamento_total / faturamento_anterior - 1)
    proporcao_interno = ano_atual['Faturamento_Interno'] / faturamento_total
    proporcao_exportacao = ano_atual['Faturamento_Exportacao'] / faturamento_total
    
    # Layout de métricas
    st.subheader("📍 Análise Territorial")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Detalhamento dos territórios
        var_estados = ano_atual['Estados_Atendidos'] - ano_anterior['Estados_Atendidos']
        var_paises = ano_atual['Paises_Atendidos'] - ano_anterior['Paises_Atendidos']
        help_text = (
            f"Detalhamento:\n"
            f"• Estados: {ano_atual['Estados_Atendidos']} de 27 estados brasileiros\n"
            f"• Países: {ano_atual['Paises_Atendidos']} países atendidos\n\n"
            f"Variação vs 2023:\n"
            f"• +{var_estados} estados\n"
            f"• +{var_paises} países"
        )
        st.metric(
            "Territórios Atendidos",
            f"{total_territorios} regiões",
            f"+{var_estados + var_paises} vs 2023",
            help=help_text
        )
    
    with col2:
        # Detalhamento do faturamento total
        help_text = (
            f"Composição do Faturamento:\n"
            f"• Interno: {format_currency(ano_atual['Faturamento_Interno'])}\n"
            f"• Exportação: {format_currency(ano_atual['Faturamento_Exportacao'])}\n\n"
            f"Variação vs 2023:\n"
            f"• Interno: {format_percentage((ano_atual['Faturamento_Interno']/ano_anterior['Faturamento_Interno'])-1)}\n"
            f"• Exportação: {format_percentage((ano_atual['Faturamento_Exportacao']/ano_anterior['Faturamento_Exportacao'])-1)}"
        )
        st.metric(
            "Faturamento Total",
            format_currency(faturamento_total),
            format_percentage(var_faturamento),
            help=help_text
        )
    
    with col3:
        # Detalhamento do crescimento
        crescimento_interno = ano_atual['Faturamento_Interno'] - ano_anterior['Faturamento_Interno']
        crescimento_exportacao = ano_atual['Faturamento_Exportacao'] - ano_anterior['Faturamento_Exportacao']
        crescimento_total = faturamento_total - faturamento_anterior
        
        help_text = (
            f"Crescimento por Mercado:\n"
            f"• Interno: {format_currency(crescimento_interno)}\n"
            f"• Exportação: {format_currency(crescimento_exportacao)}\n\n"
            f"Total: {format_currency(crescimento_total)}"
        )
        st.metric(
            "Crescimento Anual",
            format_percentage(var_faturamento),
            "vs 2023",
            help=help_text
        )
    
    with col4:
        # Detalhamento da distribuição de mercado
        help_text = (
            f"Distribuição do Faturamento:\n"
            f"• Mercado Interno: {format_currency(ano_atual['Faturamento_Interno'])} ({format_percentage(proporcao_interno)})\n"
            f"• Exportação: {format_currency(ano_atual['Faturamento_Exportacao'])} ({format_percentage(proporcao_exportacao)})\n\n"
            f"Exportação representa {format_percentage(ano_atual['Faturamento_Exportacao']/ano_atual['Faturamento_Interno'])} do mercado interno"
        )
        st.metric(
            "Mercado Interno",
            format_percentage(proporcao_interno),
            format_percentage(proporcao_interno - (ano_anterior['Faturamento_Interno'] / (ano_anterior['Faturamento_Interno'] + ano_anterior['Faturamento_Exportacao']))),
            help=help_text
        )

def main():
    st.set_page_config(page_title="Teste de Métricas", layout="wide")
    create_metrics_card()

if __name__ == "__main__":
    main() 