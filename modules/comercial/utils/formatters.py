import locale
from typing import Union, Dict, Any

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class ValueFormatter:
    @staticmethod
    def format_currency(value: float) -> str:
        """Formata valor para moeda brasileira"""
        return locale.currency(value, grouping=True, symbol=True)

    @staticmethod
    def prepare_hover_data(location: str, value: float) -> list:
        """Prepara dados para o hover do mapa"""
        return [
            location,
            locale.currency(value, grouping=True, symbol=True)
        ] 