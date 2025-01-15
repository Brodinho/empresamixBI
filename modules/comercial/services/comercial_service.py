from typing import List
import pandas as pd
from shared.services.database import DatabaseService
import logging

logger = logging.getLogger(__name__)

class ComercialAPIService:
    def __init__(self):
        self.db = DatabaseService()

    def get_dados_rfv(self, anos_selecionados: List[int]) -> pd.DataFrame:
        """
        Obtém os dados para análise RFV
        
        Args:
            anos_selecionados (List[int]): Lista de anos para filtrar os dados
            
        Returns:
            pd.DataFrame: DataFrame com os dados de RFV
        """
        try:
            query = """
            WITH ultima_compra AS (
                SELECT 
                    cliente_id,
                    MAX(data_venda) as data_ultima_compra
                FROM vendas
                WHERE YEAR(data_venda) IN :anos
                GROUP BY cliente_id
            ),
            metricas_cliente AS (
                SELECT 
                    v.cliente_id,
                    COUNT(DISTINCT v.venda_id) as frequencia,
                    SUM(v.valor_total) as valor
                FROM vendas v
                WHERE YEAR(v.data_venda) IN :anos
                GROUP BY v.cliente_id
            )
            SELECT 
                mc.cliente_id,
                DATEDIFF(day, uc.data_ultima_compra, GETDATE()) as recencia,
                mc.frequencia,
                mc.valor
            FROM metricas_cliente mc
            JOIN ultima_compra uc ON mc.cliente_id = uc.cliente_id
            """
            
            params = {
                'anos': tuple(anos_selecionados)
            }
            
            df = self.db.query_df(query, params)
            return df
            
        except Exception as e:
            logger.error(f"Erro ao buscar dados RFV: {str(e)}")
            raise 