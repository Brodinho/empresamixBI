"""
Serviço para API do módulo comercial
"""
import os
import pandas as pd
from typing import Optional
from shared.services.base_service import BaseAPIService
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ComercialAPIService(BaseAPIService):
    """Serviço responsável por gerenciar todas as chamadas à API comercial"""
    
    def __init__(self):
        """Inicializa o serviço com as configurações da API"""
        super().__init__()
        self.base_url = os.getenv('API_BASE_URL')
        self.client = os.getenv('VITE_API_CLIENTE')
        self.api_id = os.getenv('VITE_API_ID')
        self.view = os.getenv('VITE_API_VIEW')
    
    def _build_url(self) -> str:
        """Constrói a URL da API com os parâmetros necessários"""
        return f"{self.base_url}/?CLIENTE={self.client}&ID={self.api_id}&VIEW={self.view}"
    
    def _validate_date(self, date_str: str) -> bool:
        """
        Valida se a data está em um intervalo aceitável
        
        Args:
            date_str (str): Data em formato string
            
        Returns:
            bool: True se a data é válida, False caso contrário
        """
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            # Aceita datas entre 2000 e o ano atual + 1
            return 2000 <= date.year <= datetime.now().year + 1
        except:
            return False
    
    def _process_data(self, data: list) -> pd.DataFrame:
        """
        Processa os dados brutos da API
        
        Args:
            data (list): Lista de dicionários com dados da API
            
        Returns:
            pd.DataFrame: DataFrame processado
        """
        try:
            # Converte para DataFrame
            df = pd.DataFrame(data)
            
            # Filtra datas inválidas
            df = df[df['data'].apply(self._validate_date)]
            
            # Converte data usando formato ISO
            df['data'] = pd.to_datetime(df['data'])
            df['ano'] = df['data'].dt.year
            
            # Identifica vendas internas/externas
            df['tipo_venda'] = df.apply(
                lambda x: 'EXTERNO' if x['pais'] != 'BRASIL' else 'INTERNO',
                axis=1
            )
            
            # Remove registros com valores nulos ou inválidos
            df = df.dropna(subset=['valorfaturado', 'uf', 'cidade', 'pais'])
            
            logger.debug(f"Dados processados: {len(df)} registros válidos")
            logger.debug(f"Colunas disponíveis: {df.columns.tolist()}")
            logger.debug(f"Amostra dos dados:\n{df.head()}")
            
            if df.empty:
                logger.error("Nenhum registro válido após processamento")
                return None
                
            return df
            
        except Exception as e:
            logger.error(f"Erro no processamento dos dados: {str(e)}")
            logger.error(f"Exemplo dos dados recebidos: {data[0] if data else 'Sem dados'}")
            return None
    
    def get_data(self) -> Optional[pd.DataFrame]:
        """
        Obtém dados da API comercial
        
        Returns:
            Optional[pd.DataFrame]: DataFrame com os dados ou None em caso de erro
        """
        try:
            data = self._make_request()
            if data is None:
                logger.error("Nenhum dado retornado pela API")
                return None
                
            df = self._process_data(data)
            if df is None or df.empty:
                logger.error("Nenhum dado válido após processamento")
                return None
                
            return df
            
        except Exception as e:
            logger.error(f"Erro ao processar dados: {str(e)}")
            return None 