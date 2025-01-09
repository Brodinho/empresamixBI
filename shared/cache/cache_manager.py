"""
Gerenciador de cache para otimização de requisições
"""
import os
import json
from datetime import datetime, timedelta
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """Gerencia o cache de dados da aplicação"""
    
    def __init__(self):
        self.cache_dir = os.getenv('CACHE_DIR', '.cache')
        self.cache_duration = timedelta(minutes=30)  # Cache de 30 minutos
        
        # Cria diretório de cache se não existir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera dados do cache"""
        try:
            cache_file = os.path.join(self.cache_dir, f"{key}.json")
            
            if not os.path.exists(cache_file):
                return None
                
            with open(cache_file, 'r') as f:
                data = json.load(f)
                
            # Verifica se o cache expirou
            cached_time = datetime.fromisoformat(data['timestamp'])
            if datetime.now() - cached_time > self.cache_duration:
                return None
                
            return data['content']
            
        except Exception as e:
            logger.error(f"Erro ao ler cache: {str(e)}")
            return None
    
    def set(self, key: str, content: Any) -> bool:
        """Salva dados no cache"""
        try:
            cache_file = os.path.join(self.cache_dir, f"{key}.json")
            
            data = {
                'timestamp': datetime.now().isoformat(),
                'content': content
            }
            
            with open(cache_file, 'w') as f:
                json.dump(data, f)
                
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar cache: {str(e)}")
            return False

# Instância global do cache
cache_manager = CacheManager() 