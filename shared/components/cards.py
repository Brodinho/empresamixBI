import streamlit as st

def create_module_card(title, icon, color, dashboards, module_id):
    """Cria um card usando botão estilizado."""
    
    # Estilo do botão/card
    st.markdown(f"""
        <style>
            /* Estilo do botão como card */
            div[data-testid="stButton"] button {{
                width: 100%;
                background-color: {color}15 !important;
                border: 1px solid {color} !important;
                border-radius: 10px !important;
                padding: 1.5rem !important;
                cursor: pointer;
                transition: all 0.3s ease;
                color: white !important;
                text-align: left !important;
                height: auto !important;
            }}
            
            div[data-testid="stButton"] button:hover {{
                transform: translateY(-5px);
                box-shadow: 0 5px 15px {color}30;
            }}
            
            /* Conteúdo do card */
            .card-content-{module_id} {{
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }}
            
            /* Título */
            .card-title-{module_id} {{
                font-size: 1.2rem;
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 0.5rem;
            }}
            
            /* Lista de dashboards */
            .dashboard-list-{module_id} {{
                list-style-type: none;
                padding: 0;
                margin: 0;
                color: #94A3B8;
            }}
            
            .dashboard-item-{module_id} {{
                margin: 0.5rem 0;
                padding-left: 1rem;
                position: relative;
                font-size: 0.9rem;
            }}
            
            .dashboard-item-{module_id}:before {{
                content: "•";
                position: absolute;
                left: 0;
                color: {color};
            }}
        </style>
    """, unsafe_allow_html=True)
    
    # Lista de dashboards formatada
    dashboard_items = "".join([
        f'<li class="dashboard-item-{module_id}">{dashboard}</li>'
        for dashboard in dashboards
    ])
    
    # Criar o botão com o conteúdo
    if st.button(
        f"{icon} {title}",  # Simplificando o conteúdo do botão
        key=f"btn_{module_id}",
        use_container_width=True
    ):
        try:
            # Tenta navegar para o módulo
            st.switch_page(f"pages/{module_id}_main.py")
        except Exception as e:
            st.error(f"Erro ao carregar o módulo {module_id}: {str(e)}")
            st.error("Verifique se o arquivo existe em: pages/{module_id}_main.py") 

def create_info_card(title, icon, color, dashboards):
    """Cria um card informativo (não clicável)."""
    
    st.markdown(f"""
        <style>
            /* Container principal */
            .stColumns {{
                gap: 1rem;  /* Espaço entre colunas */
            }}
            
            /* Card informativo */
            .info-card {{
                background-color: {color}15;
                border: 1px solid {color};
                border-radius: 10px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                width: 100%;  /* Ocupa toda a largura da coluna */
                max-width: 600px;  /* Largura máxima */
                margin-left: auto;  /* Centraliza horizontalmente */
                margin-right: auto;
            }}
            
            /* Título mais compacto */
            .info-card-title {{
                color: white;
                font-size: 1.2rem;
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 0.8rem;
            }}
            
            /* Lista mais compacta */
            .info-dashboard-list {{
                list-style-type: none;
                padding: 0;
                margin: 0;
                color: #94A3B8;
            }}
            
            .info-dashboard-item {{
                margin: 0.3rem 0;
                padding-left: 1rem;
                position: relative;
                font-size: 0.9rem;
            }}
            
            .info-dashboard-item:before {{
                content: "•";
                position: absolute;
                left: 0;
                color: {color};
            }}
        </style>
        
        <div class="info-card">
            <div class="info-card-title">
                {icon} {title}
            </div>
            <ul class="info-dashboard-list">
                {"".join([f'<li class="info-dashboard-item">{dashboard}</li>' for dashboard in dashboards])}
            </ul>
        </div>
    """, unsafe_allow_html=True)

def create_nav_button(title, icon, module_id):
    """Cria um botão de navegação estilizado."""
    
    st.markdown(f"""
        <style>
            /* Estilo do botão de navegação */
            div[data-testid="stButton"] button {{
                width: 100%;
                background-color: rgba(255, 255, 255, 0.1) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 10px !important;
                padding: 1rem !important;
                cursor: pointer;
                transition: all 0.3s ease;
                color: white !important;
                text-align: left !important;
                font-size: 1.1rem !important;
            }}
            
            div[data-testid="stButton"] button:hover {{
                background-color: rgba(255, 255, 255, 0.2) !important;
                border-color: rgba(255, 255, 255, 0.3) !important;
                transform: translateX(5px);
            }}
        </style>
    """, unsafe_allow_html=True)
    
    if st.button(f"{icon} {title}", key=f"btn_{module_id}", use_container_width=True):
        try:
            st.switch_page(f"pages/{module_id}_main.py")
        except Exception as e:
            st.error(f"Erro ao carregar o módulo {module_id}: {str(e)}") 

def create_module_container(title, icon, color, dashboards, module_id):
    """Cria um container que agrupa o card informativo e o botão."""
    
    st.markdown(f"""
        <style>
            /* Reset para containers do Streamlit */
            div.element-container,
            div.stButton,
            div[data-testid="stButton"] {{
                width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
            
            /* Container principal */
            .module-container-{module_id} {{
                width: 100%;
                display: flex;
                flex-direction: column;
                align-items: stretch;
                gap: 1rem;  /* Espaçamento entre card e botão */
                margin-bottom: 2rem;
            }}
            
            /* Card informativo */
            .info-card {{
                background-color: {color}15;
                border: 1px solid {color};
                border-radius: 10px;
                padding: 1.5rem;
                width: 100%;
                margin-bottom: 0.75rem;  /* Espaçamento adicional após o card */
            }}
            
            /* Botão de navegação */
            div[data-testid="stButton"] button {{
                width: 100% !important;
                background-color: rgba(255, 255, 255, 0.1) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 10px !important;
                padding: 1rem !important;
                cursor: pointer;
                transition: all 0.3s ease;
                color: white !important;
                text-align: left !important;
                font-size: 1.1rem !important;
                box-sizing: border-box !important;
            }}
            
            /* Forçar largura igual em todos os navegadores */
            div.row-widget.stButton,
            div[data-testid="stButton"] {{
                display: block !important;
                width: 100% !important;
            }}
            
            /* Resto dos estilos permanece igual */
            .info-card-title {{
                color: white;
                font-size: 1.2rem;
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 0.8rem;
            }}
            
            .info-dashboard-list {{
                list-style-type: none;
                padding: 0;
                margin: 0;
                color: #94A3B8;
            }}
            
            .info-dashboard-item {{
                margin: 0.3rem 0;
                padding-left: 1rem;
                position: relative;
                font-size: 0.9rem;
            }}
            
            .info-dashboard-item:before {{
                content: "•";
                position: absolute;
                left: 0;
                color: {color};
            }}
        </style>
    """, unsafe_allow_html=True)
    
    # Container principal
    st.markdown(f'<div class="module-container-{module_id}">', unsafe_allow_html=True)
    
    # Card informativo
    st.markdown(f"""
        <div class="info-card">
            <div class="info-card-title">
                {icon} {title}
            </div>
            <ul class="info-dashboard-list">
                {"".join([f'<li class="info-dashboard-item">{dashboard}</li>' for dashboard in dashboards])}
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Botão de navegação
    if st.button(f"{icon} {title}", key=f"btn_{module_id}", use_container_width=True):
        try:
            st.switch_page(f"pages/{module_id}_main.py")
        except Exception as e:
            st.error(f"Erro ao carregar o módulo {module_id}: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True) 