import streamlit as st
from functools import wraps
from datetime import datetime, timedelta

def cache_data(ttl_seconds=3600):
    """Decorator para cache de dados com TTL"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Criar chave única para o cache
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            
            # Verificar se dados estão em cache e ainda são válidos
            if cache_key in st.session_state:
                data, timestamp = st.session_state[cache_key]
                if datetime.now() - timestamp < timedelta(seconds=ttl_seconds):
                    return data
            
            # Se não estiver em cache ou expirou, executar função
            result = func(*args, **kwargs)
            st.session_state[cache_key] = (result, datetime.now())
            return result
        return wrapper
    return decorator

def clear_cache():
    """Limpa todo o cache"""
    for key in list(st.session_state.keys()):
        del st.session_state[key] 