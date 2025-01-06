import requests
import pandas as pd
from datetime import datetime
from ..config import API_CONFIG
from .geo_service import GeoService

class ComercialAPIService:
    @staticmethod
    def _make_request(params: dict = None) -> dict:
        """Faz uma requisição à API"""
        try:
            url = API_CONFIG['BASE_URL']
            default_params = API_CONFIG['PARAMS'].copy()  # Faz uma cópia para não modificar o original
            
            # Combina os parâmetros default com os parâmetros passados
            if params:
                default_params.update(params)
            
            response = requests.get(
                url,
                params=default_params,
                timeout=API_CONFIG['TIMEOUT']
            )
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao acessar a API: {str(e)}")

    @classmethod
    def get_vendas_por_regiao(cls) -> pd.DataFrame:
        """Obtém dados de vendas por região"""
        data = cls._make_request(API_CONFIG['ENDPOINTS']['TERRITORIO']['vendas_regiao'])
        return pd.DataFrame(data)

    @classmethod
    def get_metas_por_regiao(cls) -> pd.DataFrame:
        """Obtém dados de metas por região"""
        data = cls._make_request(API_CONFIG['ENDPOINTS']['TERRITORIO']['metas_regiao'])
        return pd.DataFrame(data)

    @classmethod
    def get_detalhamento_territorio(cls, page: int = 1, items_per_page: int = 10) -> dict:
        """Obtém detalhamento do território com paginação"""
        params = {
            'page': page,
            'items_per_page': items_per_page
        }
        return cls._make_request(
            API_CONFIG['ENDPOINTS']['TERRITORIO']['detalhamento'],
            params=params
        )

    @classmethod
    def get_vendas_mapa(cls) -> pd.DataFrame:
        """Obtém e processa dados de vendas para o mapa"""
        try:
            # Faz a requisição à API
            data = cls._make_request()
            df = pd.DataFrame(data)
            
            # Converte a coluna de emissão para datetime
            df['emissao'] = pd.to_datetime(df['emissao'])
            
            # Filtra os últimos 5 anos
            data_inicial = datetime(datetime.now().year - 5, 1, 1)
            df = df[df['emissao'] >= data_inicial]
            
            # Agrupa por nota fiscal
            df_notas = df.groupby(['sequencial', 'uf', 'codPais', 'pais'])['valorfaturado'].sum().reset_index()
            
            # Agrupa por localização
            df_mapa = df_notas.groupby(['uf', 'codPais', 'pais'], as_index=False).agg({
                'valorfaturado': 'sum'
            })
            
            # Processa dados internos e externos
            def get_coordinates(row):
                if row['uf'] == 'EX':
                    # Para exportações, usa o nome do país
                    coords = GeoService.get_location_coordinates('EX', row['pais'])
                    location_name = row['pais']
                else:
                    # Para vendas internas, usa o nome completo do estado
                    coords = GeoService.get_location_coordinates(row['uf'])
                    location_name = GeoService.get_location_name(row['uf'])
                
                return pd.Series({
                    'latitude': coords.get('lat'),
                    'longitude': coords.get('lon'),
                    'location_name': location_name,
                    'tipo_venda': 'INTERNO' if row['uf'] != 'EX' else 'EXTERNO',
                    'faturamento': row['valorfaturado']
                })
            
            # Aplica as coordenadas e formatação
            return df_mapa.apply(get_coordinates, axis=1)
            
        except Exception as e:
            raise Exception(f"Erro ao processar dados do mapa: {str(e)}") 