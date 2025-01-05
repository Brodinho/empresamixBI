import pandas as pd
import numpy as np

def get_cashflow_data():
    """Dados de fluxo de caixa."""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    return pd.DataFrame({
        'date': dates,
        'receitas': np.random.uniform(10000, 50000, size=len(dates)),
        'despesas': np.random.uniform(8000, 40000, size=len(dates))
    })

def get_dre_data():
    """Dados do DRE."""
    return pd.DataFrame({
        'conta': ['Receita Bruta', 'Deduções', 'Receita Líquida', 'CMV', 'Lucro Bruto'],
        'valor': np.random.uniform(100000, 500000, size=5)
    })

def get_indicators_data():
    """Dados de indicadores financeiros."""
    return {
        'liquidez_corrente': np.random.uniform(1.0, 2.0),
        'margem_ebitda': np.random.uniform(0.1, 0.3),
        'roi': np.random.uniform(0.15, 0.25)
    }

def get_budget_data():
    """Dados de orçamento."""
    departments = ['Comercial', 'Marketing', 'RH', 'TI', 'Operações']
    return pd.DataFrame({
        'departamento': departments,
        'orcado': np.random.uniform(50000, 200000, size=len(departments)),
        'realizado': np.random.uniform(45000, 180000, size=len(departments))
    }) 