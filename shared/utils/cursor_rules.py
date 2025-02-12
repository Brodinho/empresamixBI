from typing import Tuple, List, Union, Dict

class CursorRules:
    # Constantes
    DEFAULT_CHART_HEIGHT = 400
    DEFAULT_PAGE_SIZE = 10
    
    @staticmethod
    def format_currency(value: float) -> str:
        """Formata um valor para moeda (R$)"""
        return f"R$ {value:,.2f}"
    
    @staticmethod
    def format_percentage(value: float) -> str:
        """Formata um valor para porcentagem"""
        return f"{value*100:.1f}%"
    
    @staticmethod
    def format_number(value: float) -> str:
        """Formata um número com separadores de milhar"""
        return f"{value:,.0f}"
    
    @staticmethod
    def get_page_slice(
        page: int,
        page_size: int,
        total_items: int
    ) -> Tuple[int, int]:
        """
        Calcula o slice de início e fim para paginação
        Retorna uma tupla com (start_idx, end_idx)
        """
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, total_items)
        return (start_idx, end_idx) 