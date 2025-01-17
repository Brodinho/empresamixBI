"""
Serviço para API do módulo comercial
"""
import os
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
from typing import List

logger = logging.getLogger(__name__)

class ComercialAPIService:
    def __init__(self):
        self.base_url = os.getenv('API_BASE_URL', 'http://tecnolife.empresamix.info:8077')
        self.client = os.getenv('VITE_API_CLIENTE', 'TECNOLIFE')
        self.api_id = os.getenv('VITE_API_ID', 'XIOPMANA')
        self.view = os.getenv('VITE_API_VIEW')
        
        # Configuração de retry
        self.session = requests.Session()
        retries = Retry(
            total=3,  # número total de tentativas
            backoff_factor=0.5,  # tempo de espera entre tentativas
            status_forcelist=[500, 502, 503, 504]  # códigos HTTP para retry
        )
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
    
    def get_data(self, cube: str = None) -> pd.DataFrame:
        """
        Obtém dados do cubo especificado
        
        Args:
            cube: Nome do cubo a ser consultado (ex: "CUBO_FATURAMENTO")
        """
        try:
            # Define o cubo a ser consultado
            self.view = cube or self.view
            
            # Monta a URL
            url = f"{self.base_url}/POWERBI/?CLIENTE={self.client}&ID={self.api_id}&VIEW={self.view}"
            
            logger.debug(f"Consultando API: {url}")
            
            # Faz a requisição com timeout
            response = self.session.get(url, timeout=30)
            response.raise_for_status()  # Levanta exceção para status codes de erro
            
            data = response.json()
            
            if not data:
                logger.error("API retornou dados vazios")
                return pd.DataFrame()
            
            logger.debug(f"Dados recebidos com sucesso: {len(data)} registros")
            return pd.DataFrame(data)
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Erro de conexão com a API: {str(e)}")
            st.error("Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.")
            return pd.DataFrame()
            
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout na requisição: {str(e)}")
            st.error("A requisição excedeu o tempo limite. Tente novamente.")
            return pd.DataFrame()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {str(e)}")
            st.error("Erro ao acessar a API. Tente novamente mais tarde.")
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            st.error("Ocorreu um erro inesperado. Tente novamente mais tarde.")
            return pd.DataFrame() 

    def get_dados_rfv(self, anos_selecionados: List[int]) -> pd.DataFrame:
        """
        Obtém os dados para análise RFV
        """
        try:
            # Usa o método get_data() que já está funcionando
            df = self.get_data("CUBO_FATURAMENTO")
            
            if df.empty:
                logger.warning("Nenhum dado retornado da API")
                return pd.DataFrame()
            
            # Converte datas com tratamento de erros
            df['data'] = pd.to_datetime(df['data'], errors='coerce')
            df = df.dropna(subset=['data'])  # Remove linhas com datas inválidas
            
            # Filtra por anos selecionados
            df['ano'] = df['data'].dt.year
            df = df[df['ano'].isin(anos_selecionados)]
            
            # Calcula métricas RFV
            if not df.empty:
                df = df.groupby('codcli').agg({
                    'data': lambda x: (pd.Timestamp.now() - x.max()).days,  # Recência
                    'nota': 'count',  # Frequência (contagem de notas fiscais)
                    'valorfaturado': 'sum'  # Valor total
                }).reset_index()
                
                # Renomeia as colunas
                df.columns = ['cliente_id', 'recencia', 'frequencia', 'valor']
            
            logger.info(f"Dados RFV processados: {len(df)} registros")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao processar dados RFV: {str(e)}")
            return pd.DataFrame() 