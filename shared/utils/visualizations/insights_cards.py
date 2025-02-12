import streamlit as st
from typing import Optional, Union, Dict, Any
from shared.utils.formatters import format_currency, format_percentage, format_number, format_kpi_delta

def render_metric_card(
    title: str,
    value: Union[str, float, int],
    delta: Optional[float] = None,
    delta_description: Optional[str] = None,
    help_text: Optional[str] = None,
    prefix: str = "",
    suffix: str = "",
    positive_is_good: bool = True,
    formatter: str = "number",  # "number", "currency", "percentage"
    decimals: int = 0
) -> None:
    """
    Renderiza um card de métrica padronizado com efeito de profundidade
    
    Args:
        title: Título do card
        value: Valor principal
        delta: Variação percentual
        delta_description: Descrição da variação (ex: "vs mês anterior")
        help_text: Texto de ajuda que aparece ao passar o mouse
        prefix: Prefixo do valor (ex: "R$")
        suffix: Sufixo do valor (ex: "%")
        positive_is_good: Se True, valores positivos são verdes
        formatter: Tipo de formatação do valor
        decimals: Número de casas decimais
    """
    
    # Formata o valor principal
    if formatter == "currency":
        formatted_value = format_currency(value)
    elif formatter == "percentage":
        formatted_value = format_percentage(value, decimals)
    else:
        formatted_value = format_number(value, decimals, prefix, suffix)
    
    # Formata o delta se existir
    if delta is not None:
        delta_value, direction = format_kpi_delta(delta, positive_is_good)
        
        # Adiciona descrição se existir
        if delta_description:
            delta_value = f"{delta_value} {delta_description}"
    else:
        delta_value = None

    # HTML personalizado para o card
    html = f"""
    <div style="
        background-color: #1E2A3A;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin: 0.5rem 0;
        border: 1px solid #2E3A4A;
        transition: all 0.3s ease;
        &:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4);
        }}
    ">
        <div style="color: #9BA1A6; font-size: 0.8em; margin-bottom: 0.5rem;">
            {title}
            {f'<span title="{help_text}"> ℹ️</span>' if help_text else ''}
        </div>
        <div style="color: white; font-size: 1.5em; font-weight: bold;">
            {formatted_value}
        </div>
        {f'<div style="color: #9BA1A6; font-size: 0.8em; margin-top: 0.5rem;">{delta_value}</div>' if delta_value else ''}
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def render_metrics_section(
    title: str,
    metrics: Dict[str, Dict[str, Any]],
    columns: int = 5
) -> None:
    """
    Renderiza uma seção de métricas com múltiplos cards
    
    Args:
        title: Título da seção
        metrics: Dicionário com configurações das métricas
        columns: Número de colunas para distribuir os cards
    """
    st.subheader(title)
    
    # Cria as colunas
    cols = st.columns(columns)
    
    # Distribui os cards nas colunas
    for idx, (metric_id, metric_config) in enumerate(metrics.items()):
        with cols[idx % columns]:
            render_metric_card(**metric_config) 