"""
Dashboard de Performance de Vendedores
"""
import streamlit as st
import pandas as pd
import logging
from modules.comercial.services import comercial_service
from shared.components.filters import DateFilters
from modules.comercial.components.evolucao_individual import criar_evolucao_individual
from modules.comercial.components.mix_produtos_vendedor import criar_mix_produtos_vendedor
from modules.comercial.components.analise_conversao_vendedor import criar_analise_conversao_vendedor
from shared.utils.formatters import format_currency, format_percentage
from shared.utils.visualizations.insights_cards import render_metrics_section

logger = logging.getLogger(__name__)

def render_performance_vendedores():
    """Renderiza o dashboard de performance dos vendedores"""
    try:
        st.title("🎯 Performance de Vendedores")
        
        # Carrega dados primeiro
        df = comercial_service.get_data()
        if df is None or df.empty:
            logger.error("Dados não carregados em Performance de Vendedores")
            st.error('Não foi possível carregar os dados.')
            return
        
        # Configuração das métricas para os cards
        metrics = {
            'faturamento_total': {
                'title': '💰 Faturamento Total',
                'value': df['valorfaturado'].sum(),
                'formatter': 'currency',
                'help_text': 'Valor total faturado no período',
                'positive_is_good': True
            },
            'total_vendedores': {
                'title': '👥 Total de Vendedores',
                'value': len(df['vendedor'].unique()),
                'formatter': 'number',
                'help_text': 'Número de vendedores ativos no período'
            },
            'ticket_medio': {
                'title': '🎫 Ticket Médio',
                'value': df['valorfaturado'].sum() / len(df['nota'].unique()),
                'formatter': 'currency',
                'help_text': 'Valor médio por venda no período',
                'positive_is_good': True
            }
        }
        
        # Renderiza os cards de métricas
        render_metrics_section('', metrics, columns=3)
        
        # Filtros após as métricas
        with st.expander("🔍 Filtros de Análise"):
            if 'emissao' in df.columns:
                df['emissao'] = pd.to_datetime(df['emissao'])
                df['ano'] = df['emissao'].dt.year
                
                anos_disponiveis = sorted(df['ano'].unique())
                if anos_disponiveis:
                    anos_selecionados = DateFilters.year_filter("performance_vendedores")
                    
                    if anos_selecionados and len(anos_selecionados) > 0:
                        df = df[df['ano'].isin(anos_selecionados)]
        
        if not df.empty:
            # Debug: Verifica se chegou na renderização dos cards
            logger.debug("Iniciando renderização dos cards em Performance de Vendedores")
            
            # Separador
            st.markdown("---")
            
            # Gráfico de Análise de Conversão
            st.subheader("📊 Análise de Conversão por Vendedor")
            with st.expander("ℹ️ Como interpretar este gráfico?"):
                st.markdown("""
                    Este gráfico mostra três métricas importantes por vendedor:
                    - 🔵 **Valor Médio por Venda**: Indica o ticket médio de cada vendedor
                    - 🟢 **Vendas por Cliente**: Mostra a capacidade de gerar vendas recorrentes
                    - 🟡 **Total de Clientes**: Representa a base de clientes atendida
                    
                    💡 **Dica**: Vendedores com alta taxa de vendas por cliente e valor médio 
                    elevado tendem a ser mais eficientes em relacionamento e negociação.
                """)
            
            fig_conversao = criar_analise_conversao_vendedor(df)
            if fig_conversao:
                st.plotly_chart(fig_conversao, use_container_width=True)
            else:
                st.error('Erro ao criar gráfico de análise de conversão')
            
            # Demais gráficos (a serem implementados)
            st.markdown("---")
            
            # Layout em duas colunas para os outros gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Evolução de Vendas")
                with st.expander("ℹ️ Como interpretar este gráfico?"):
                    st.markdown("""
                        Este gráfico mostra a evolução das vendas de cada vendedor ao longo do tempo:
                        - 📊 **Linhas**: Representam o desempenho individual
                        - 📅 **Eixo X**: Mostra a evolução temporal (mês/ano)
                        - 💰 **Eixo Y**: Apresenta o valor faturado
                        
                        💡 **Dica**: Observe tendências de crescimento e sazonalidade nas vendas 
                        de cada vendedor.
                    """)
                
                fig_evolucao = criar_evolucao_individual(df)
                if fig_evolucao:
                    st.plotly_chart(fig_evolucao, use_container_width=True)
                else:
                    st.error('Erro ao criar gráfico de evolução de vendas')
                
            with col2:
                st.subheader("🎯 Mix de Produtos")
                with st.expander("ℹ️ Como interpretar este gráfico?"):
                    st.markdown("""
                        Este gráfico mostra a distribuição das vendas por categoria de produtos:
                        
                        📂 **Níveis:**
                        • Vendedor > Grupo > Subgrupo
                        
                        🎨 **Cores:**
                        • Quanto mais escuro, maior o valor
                        
                        📊 **Tamanho:**
                        • Proporcional ao valor faturado
                        
                        **% do Total representa:**
                        • Vendedor: % do faturamento total do período
                        • Grupo: % do total do vendedor
                        • Subgrupo: % do total do grupo
                        
                        💡 **Dica:**
                        • Identifique a especialidade de cada vendedor
                        • Analise oportunidades de diversificação do mix de produtos
                        • Compare a distribuição entre diferentes vendedores
                    """)
                
                fig_mix = criar_mix_produtos_vendedor(df)
                if fig_mix:
                    st.plotly_chart(fig_mix, use_container_width=True)
                else:
                    st.error('Erro ao criar gráfico de mix de produtos')
                
        else:
            st.warning("Nenhum dado encontrado para o período selecionado.")
            
    except Exception as e:
        logger.error(f"Erro na renderização de Performance de Vendedores: {str(e)}")
        st.error('Erro ao renderizar dashboard') 