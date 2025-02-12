import pandas as pd
import numpy as np

def get_sales_data():
    """
    Função temporária para gerar dados de exemplo.
    Substitua por sua lógica real de dados.
    """
    # Dados de exemplo
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    data = {
        'date': dates,
        'sales': np.random.randint(1000, 5000, size=len(dates)),
        'revenue': np.random.uniform(10000, 50000, size=len(dates)),
        'customers': np.random.randint(10, 100, size=len(dates))
    }
    return pd.DataFrame(data)

def get_pipeline_data():
    """Dados do pipeline de vendas."""
    stages = ['Lead', 'Qualificação', 'Proposta', 'Negociação', 'Fechado']
    data = {
        'stage': stages,
        'count': np.random.randint(10, 100, size=len(stages)),
        'value': np.random.uniform(10000, 100000, size=len(stages))
    }
    return pd.DataFrame(data)

def get_leads_data():
    """Dados de leads/oportunidades."""
    return pd.DataFrame({
        'lead': np.random.choice(['A', 'B', 'C'], 100),
        'status': np.random.choice(['Novo', 'Em Progresso', 'Convertido'], 100),
        'value': np.random.uniform(1000, 10000, 100)
    })

def get_territory_data():
    """Dados de território de vendas."""
    regions = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
    return pd.DataFrame({
        'region': regions,
        'sales': np.random.randint(10000, 50000, size=len(regions)),
        'market_share': np.random.uniform(0.1, 0.3, size=len(regions))
    }) 