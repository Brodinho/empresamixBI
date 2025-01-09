"""
Componentes reutilizáveis de filtros
"""
import streamlit as st
import logging
from typing import List
from datetime import datetime

logger = logging.getLogger(__name__)

class DateFilters:
    """Classe para gerenciar filtros de data"""
    
    @staticmethod
    def year_filter(key_suffix: str = "") -> List[int]:
        """
        Cria um filtro de seleção de anos
        
        Args:
            key_suffix (str): Sufixo para a chave do componente
            
        Returns:
            List[int]: Lista de anos selecionados
        """
        try:
            # Gera lista de anos (últimos 5 anos)
            current_year = datetime.now().year
            anos_disponiveis = list(range(current_year - 4, current_year + 1))
            
            # Adiciona opção "Todos"
            opcoes = ['Todos'] + [str(ano) for ano in anos_disponiveis]
            
            # Cria o multiselect
            anos_selecionados = st.multiselect(
                'Selecione o(s) período(s):',
                opcoes,
                default=['Todos'],
                key=f"year_filter_{key_suffix}"
            )
            
            logger.debug(f"Anos selecionados: {anos_selecionados}")
            
            # Se "Todos" está selecionado ou nenhuma seleção, retorna todos os anos
            if 'Todos' in anos_selecionados or not anos_selecionados:
                return anos_disponiveis
                
            # Converte anos selecionados para inteiros
            return [int(ano) for ano in anos_selecionados if ano != 'Todos']
            
        except Exception as e:
            logger.error(f"Erro no filtro de anos: {str(e)}")
            return anos_disponiveis  # Retorna todos os anos em caso de erro 