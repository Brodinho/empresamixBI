import streamlit as st
import traceback
from functools import wraps
from typing import Callable, Any

def handle_error(show_traceback: bool = False) -> Callable:
    """Decorator para tratamento de erros"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = str(e)
                st.error(f"Erro: {error_msg}")
                
                if show_traceback:
                    st.code(traceback.format_exc())
                    
                # Log do erro (pode ser implementado posteriormente)
                print(f"Error in {func.__name__}: {error_msg}")
                print(traceback.format_exc())
                
        return wrapper
    return decorator 