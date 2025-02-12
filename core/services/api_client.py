import requests
from typing import Dict, Any
from config.settings import API_BASE_URL, API_TIMEOUT

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Faz requisição à API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Erro na requisição: {str(e)}")
    
    def get_sales_data(self, **params):
        """Obtém dados de vendas"""
        return self._make_request("GET", "/vendas", params=params)
    
    def get_leads_data(self, **params):
        """Obtém dados de leads"""
        return self._make_request("GET", "/leads", params=params)
    
    # Adicione mais métodos conforme necessário

class APIError(Exception):
    pass

api_client = APIClient()
