"""
Testes unitários para o serviço comercial
"""
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from modules.comercial.services.api_service import ComercialAPIService
from shared.exceptions.api_exceptions import *

class TestComercialService(unittest.TestCase):
    """Testes para o serviço comercial"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.service = ComercialAPIService()
        
    @patch('requests.get')
    def test_successful_request(self, mock_get):
        """Testa uma requisição bem-sucedida"""
        # Mock da resposta
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': [{'valor': 100}]}
        mock_get.return_value = mock_response
        
        # Teste
        result = self.service.get_data(use_cache=False)
        self.assertIsInstance(result, pd.DataFrame)
        
    @patch('requests.get')
    def test_api_timeout(self, mock_get):
        """Testa timeout na API"""
        mock_get.side_effect = requests.exceptions.Timeout
        
        with self.assertRaises(APITimeoutError):
            self.service.get_data(use_cache=False)
    
    def test_cache_functionality(self):
        """Testa funcionalidade de cache"""
        # Primeiro acesso (sem cache)
        data1 = self.service.get_data()
        
        # Segundo acesso (deve usar cache)
        data2 = self.service.get_data()
        
        self.assertTrue(data1.equals(data2)) 