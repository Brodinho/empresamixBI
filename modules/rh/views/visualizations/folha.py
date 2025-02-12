import streamlit as st
import pandas as pd
from shared.utils.cursor_rules import CursorRules
from shared.utils.cursor_utils import CursorUtils

def render():
    st.title("Folha de Pagamento")
    
    df = pd.DataFrame({
        'Funcionário': ['João', 'Maria'],
        'Salário': [4500.00, 5500.00],
        'Benefícios': [0.30, 0.30]
    })
    
    df = CursorUtils.format_df_currency(df, ['Salário'])
    df = CursorUtils.format_df_percentage(df, ['Benefícios'])
    
    page = st.number_input('Página', min_value=1, value=1)
    df_paged = CursorUtils.paginate_dataframe(df, page)
    
    st.dataframe(df_paged, height=CursorRules.DEFAULT_CHART_HEIGHT) 