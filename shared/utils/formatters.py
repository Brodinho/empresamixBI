import locale
from typing import Union, Optional, Tuple
from datetime import datetime

# Configurar locale para formatação de moeda
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def format_currency(value: Union[float, int]) -> str:
    """Formata valor para moeda brasileira"""
    try:
        # Formata o número manualmente para garantir consistência
        valor_formatado = f"{value:_.2f}".replace("_", ".").replace(".", ",", 1).replace("_", ".")
        return f"R$ {valor_formatado}"
    except:
        return f"R$ 0,00"

def format_percentage(value: float, decimals: int = 1) -> str:
    """Formata valor para percentual"""
    if value is None:
        return "0%"
    return f"{value:,.{decimals}f}%"

def format_date(date: Union[str, datetime], format_str: str = "%d/%m/%Y") -> str:
    """Formata data"""
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
    return date.strftime(format_str)

def format_number(value: Union[float, int], 
                 decimals: int = 0, 
                 prefix: str = "", 
                 suffix: str = "") -> str:
    """Formata número com prefixo/sufixo opcional"""
    if value is None:
        return "0"
    return f"{prefix}{value:,.{decimals}f}{suffix}"

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
