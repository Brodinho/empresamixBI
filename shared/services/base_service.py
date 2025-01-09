"""
Classe base para serviços de API
"""
import requests
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class BaseAPIService(ABC):
    """Classe base para todos os serviços de API"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BaseAPIService, cls).__new__(cls)
        return cls._instance
    
    @abstractmethod
    def _build_url(self) -> str:
        """Método abstrato para construção da URL"""
        pass
    
    def _make_request(self) -> Optional[Dict[str, Any]]:
        """Faz a requisição HTTP e trata erros comuns"""
        try:
            url = self._build_url()
            logger.debug(f"Fazendo requisição para: {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Erro na requisição: {str(e)}")
            return None 