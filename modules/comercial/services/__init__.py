"""
Inicialização dos serviços do módulo comercial
"""
from .api_service import ComercialAPIService

# Instância global única do serviço
comercial_service = ComercialAPIService()

__all__ = ['comercial_service']
