import locale
from typing import Union, Optional, Tuple
from datetime import datetime

# Configurar locale para formatação de moeda
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def format_currency(value: Union[float, int]) -> str:
    """Formata valor para moeda brasileira"""
    try:
        # Primeiro formata o número com pontos de milhar e vírgula decimal
        numero = f"{value:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", ".")
        return f"R$ {numero}"
    except:
        return f"R$ 0,00"

def format_percentage(value: float, decimals: int = 1) -> str:
    """Formata valor para percentual"""
    if value is None:
        return "0%"
    # Formata o número e substitui ponto por vírgula
    return f"{value:,.{decimals}f}%".replace(".", ",")

def format_date(date: Union[str, datetime], format_str: str = "%d/%m/%Y") -> str:
    """Formata data"""
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
    return date.strftime(format_str)

def format_number(value: Union[float, int], 
                 decimals: int = 0, 
                 prefix: str = "", 
                 suffix: str = "") -> str:
    """Formata número com prefixo/sufixo opcional no padrão brasileiro"""
    if value is None:
        return "0"
    # Formata o número com separador de milhar e substitui por ponto
    numero = f"{value:,.{decimals}f}".replace(",", ".")
    if decimals > 0:
        # Se tiver decimais, substitui o último ponto por vírgula
        numero = numero.replace(".", ",", -1)
    return f"{prefix}{numero}{suffix}"

def format_kpi_delta(value: float, positive_is_good: bool = True) -> Tuple[str, str]:
    """Formata delta de KPI com indicador de direção"""
    if value is None:
        return "0%", "off"
    
    formatted = format_percentage(abs(value))
    
    if value > 0:
        direction = "up" if positive_is_good else "down"
        return f"↑ {formatted}", direction
    elif value < 0:
        direction = "down" if positive_is_good else "up"
        return f"↓ {formatted}", direction
    else:
        return formatted, "off"

def format_tooltip_currency(value: Union[float, int]) -> str:
    """Formata valor para moeda brasileira sem caracteres especiais (para tooltips)"""
    try:
        # Primeiro formata o número com pontos de milhar e vírgula decimal
        numero = f"{value:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", ".")
        # Retorna com R sem $ e mantém o espaço
        return f"R {numero}"
    except:
        return f"R 0,00"
