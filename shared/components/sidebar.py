import streamlit as st
from typing import List, Callable

def create_sidebar(
    title: str,
    menu_items: List[str],
    on_home_click: Callable = None
) -> str:
    """Cria sidebar com menu de navegação"""
    
    with st.sidebar:
        # Botão Home
        if st.button("🏠 Home"):
            if on_home_click:
                on_home_click()
            else:
                st.switch_page("Home.py")
        
        st.title(title)
        st.markdown("---")
        
        # Menu de navegação
        selected = None
        for item in menu_items:
            if st.button(item, use_container_width=True):
                selected = item
                
        return selected 