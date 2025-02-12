import streamlit as st
from config.settings import MODULES

def create_module_card(title: str, description: str, icon: str) -> None:
    """Cria um card para um módulo com funcionalidade de clique"""
    
    # Criar um ID único para o botão baseado no título
    button_id = f"btn_{title.lower().replace(' ', '_')}"
    
    # HTML do card com wrapper de botão e classe específica para esconder o botão
    card_html = f"""
        <div class="module-card clickable hidden-button" onclick="document.getElementById('{button_id}').click()">
            <div class="icon">{icon}</div>
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
    """
    
    # Renderiza o card
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Botão invisível que será acionado pelo clique no card
    if st.button("Acessar", key=button_id, help=f"Acessar módulo {title}"):
        # Atualiza o estado da sessão com o módulo selecionado
        module_route = title.lower().replace(" ", "_")
        st.session_state.current_module = module_route
        st.rerun()

def create_info_card(title: str, value: str, delta: str = None) -> None:
    """Cria um card informativo"""
    if delta:
        st.metric(label=title, value=value, delta=delta)
    else:
        st.metric(label=title, value=value)

def create_nav_button(label: str, key: str) -> bool:
    """Cria um botão de navegação"""
    return st.button(label, key=key)

def create_module_container(title: str) -> None:
    """Cria um container para um módulo"""
    st.markdown(f"## {title}") 