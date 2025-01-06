from typing import List, Any, Optional
import pandas as pd
from .cursor_rules import CursorRules

class CursorUtils:
    """Utilitários para manipulação de cursores com as regras definidas"""
    
    @staticmethod
    def paginate_dataframe(
        df: pd.DataFrame,
        page: int,
        page_size: Optional[int] = None
    ) -> pd.DataFrame:
        """Pagina um DataFrame seguindo as regras definidas"""
        if page_size is None:
            page_size = CursorRules.DEFAULT_PAGE_SIZE
        else:
            page_size = CursorRules.validate_page_size(page_size)
            
        start, end = CursorRules.get_page_slice(page, page_size)
        return df.iloc[start:end]
    
    @staticmethod
    def format_df_currency(
        df: pd.DataFrame,
        columns: List[str]
    ) -> pd.DataFrame:
        """Formata colunas monetárias do DataFrame"""
        df = df.copy()
        for col in columns:
            if col in df.columns:
                df[col] = df[col].apply(CursorRules.format_currency)
        return df
    
    @staticmethod
    def format_df_percentage(
        df: pd.DataFrame,
        columns: List[str]
    ) -> pd.DataFrame:
        """Formata colunas de porcentagem do DataFrame"""
        df = df.copy()
        for col in columns:
            if col in df.columns:
                df[col] = df[col].apply(CursorRules.format_percentage)
        return df
    
    @staticmethod
    def prepare_chart_data(
        df: pd.DataFrame,
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """Prepara dados para visualização em gráficos"""
        if limit is None:
            limit = CursorRules.MAX_ITEMS_PER_CHART
        return df.head(limit) 