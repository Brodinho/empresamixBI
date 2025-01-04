import streamlit as st

def create_module_card(title, icon, color, dashboards, module_id):
    """Cria um card clicável para um módulo."""
    
    # Estilo do card clicável
    st.markdown(f"""
        <style>
        .module-card-{module_id} {{
            background-color: {color}15;
            border: 1px solid {color};
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            position: relative;  /* Importante para o botão */
        }}
        
        .module-card-{module_id}:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px {color}30;
            transition: all 0.3s ease;
        }}
        
        /* Título do módulo */
        .module-title {{
            color: white;
            font-size: 1.2rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        /* Lista de dashboards */
        .dashboard-list {{
            list-style-type: none;
            padding: 0;
            margin: 0;
            color: #94A3B8;
        }}
        
        .dashboard-item {{
            margin: 0.5rem 0;
            padding-left: 1rem;
            position: relative;
        }}
        
        .dashboard-item:before {{
            content: "•";
            position: absolute;
            left: 0;
            color: {color};
        }}

        /* Botão que cobre todo o card */
        div[data-testid="stButton"] {{
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 100% !important;
            opacity: 0 !important;
            cursor: pointer !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Container do card com botão
    with st.container():
        col1, col2 = st.columns([1, 0.001])  # Hack para posicionamento do botão
        
        with col1:
            # Conteúdo do card
            st.markdown(f"""
                <div class="module-card-{module_id}">
                    <div class="module-title">
                        {icon} {title}
                    </div>
                    <ul class="dashboard-list">
                        {"".join([f'<li class="dashboard-item">{dashboard}</li>' for dashboard in dashboards])}
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Botão invisível que cobre o card
            if st.button("", key=f"btn_{module_id}", help=f"Ir para {title}"):
                try:
                    # Usa o novo caminho do arquivo copiado
                    st.switch_page(f"pages/{module_id}_main.py")
                except Exception as e:
                    st.error(f"Erro ao acessar o módulo: {str(e)}") 