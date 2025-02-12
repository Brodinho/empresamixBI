import plotly.express as px
import streamlit as st

def criar_grafico_valor(df):
    """
    Cria o gráfico de Valor do modelo RFV
    """
    fig = px.box(
        df,
        y='valor',
        title='Distribuição do Valor Total de Compras por Cliente',
        labels={'valor': 'Valor Total (R$)'},
        color_discrete_sequence=['#E67E22']
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        height=400
    )

    # Expander com explicação
    with st.expander("ℹ️ Como interpretar o Valor?"):
        st.markdown("""
            💰 O boxplot mostra a distribuição dos valores gastos por cliente:
            - 📦 A caixa central representa 50% dos clientes
            - ⚡ Pontos acima são clientes com alto valor
            - 💎 Identifique e cuide especialmente dos clientes premium
        """)

    # Renderiza o gráfico
    st.plotly_chart(fig, use_container_width=True) 