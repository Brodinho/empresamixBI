import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils

def render():
    st.title("Planejamento da Produção")
    
    df = pd.DataFrame({
        'Ordem': ['OP001', 'OP002'],
        'Valor': [25000.00, 35000.00],
        'Progresso': [0.65, 0.80]
    })
    
    df = CursorUtils.format_df_currency(df, ['Valor'])
    df = CursorUtils.format_df_percentage(df, ['Progresso'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df, page)
    
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 