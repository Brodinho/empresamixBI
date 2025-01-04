import streamlit as st

def create_module_card(title, icon, color, dashboards, module_id):
    """Cria um card clicável para um módulo."""
    
    card_style = f"""
    <style>
        .module-card {{
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .module-card:hover {{
            transform: translateY(-5px);
        }}
        .module-title {{
            color: {color};
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        .dashboard-item {{
            padding: 5px 0;
            color: #333;
        }}
    </style>
    """
    
    st.markdown(card_style, unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f"""
        <div class="module-card">
            <div class="module-title">{icon} {title}</div>
            {''.join([f'<div class="dashboard-item">• {dashboard}</div>' for dashboard in dashboards])}
        </div>
        """, unsafe_allow_html=True)
        
        # Botão invisível para navegação
        if st.button("", key=f"btn_{module_id}", help=f"Ir para {title}"):
            st.switch_page(f"pages/{module_id}/main.py") 