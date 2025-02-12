"""
Exceções personalizadas para tratamento de erros da API
"""

class APIError(Exception):
    """Classe base para exceções da API"""
    pass

class APIConnectionError(APIError):
    """Erro de conexão com a API"""
    pass

class APIDataError(APIError):
    """Erro nos dados retornados pela API"""
    pass

class APITimeoutError(APIError):
    """Erro de timeout na requisição"""
    pass

class APICacheError(APIError):
    """Erro relacionado ao cache"""
    pass 