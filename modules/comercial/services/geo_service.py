import pandas as pd
from typing import Dict, Any

class GeoService:
    # Dicionário com coordenadas e nomes completos das capitais
    CAPITALS = {
        'AC': {'lat': -9.975377, 'lon': -67.824897, 'name': 'Acre'},
        'AL': {'lat': -9.665979, 'lon': -35.735137, 'name': 'Alagoas'},
        'AM': {'lat': -3.119028, 'lon': -60.021731, 'name': 'Amazonas'},
        'AP': {'lat': 0.034934, 'lon': -51.050033, 'name': 'Amapá'},
        'BA': {'lat': -12.971598, 'lon': -38.501799, 'name': 'Bahia'},
        'CE': {'lat': -3.731862, 'lon': -38.526669, 'name': 'Ceará'},
        'DF': {'lat': -15.779972, 'lon': -47.864195, 'name': 'Distrito Federal'},
        'ES': {'lat': -20.319972, 'lon': -40.338226, 'name': 'Espírito Santo'},
        'GO': {'lat': -16.686882, 'lon': -49.264789, 'name': 'Goiás'},
        'MA': {'lat': -2.531970, 'lon': -44.303458, 'name': 'Maranhão'},
        'MG': {'lat': -19.916681, 'lon': -43.934493, 'name': 'Minas Gerais'},
        'MS': {'lat': -20.469722, 'lon': -54.620166, 'name': 'Mato Grosso do Sul'},
        'MT': {'lat': -15.601411, 'lon': -56.097892, 'name': 'Mato Grosso'},
        'PA': {'lat': -1.455833, 'lon': -48.490277, 'name': 'Pará'},
        'PB': {'lat': -7.119496, 'lon': -34.845011, 'name': 'Paraíba'},
        'PE': {'lat': -8.054277, 'lon': -34.881256, 'name': 'Pernambuco'},
        'PI': {'lat': -5.089967, 'lon': -42.809588, 'name': 'Piauí'},
        'PR': {'lat': -25.428954, 'lon': -49.271230, 'name': 'Paraná'},
        'RJ': {'lat': -22.906847, 'lon': -43.172897, 'name': 'Rio de Janeiro'},
        'RN': {'lat': -5.779257, 'lon': -35.200916, 'name': 'Rio Grande do Norte'},
        'RO': {'lat': -8.761160, 'lon': -63.901089, 'name': 'Rondônia'},
        'RR': {'lat': 2.819725, 'lon': -60.672458, 'name': 'Roraima'},
        'RS': {'lat': -30.034647, 'lon': -51.217658, 'name': 'Rio Grande do Sul'},
        'SC': {'lat': -27.596910, 'lon': -48.549580, 'name': 'Santa Catarina'},
        'SE': {'lat': -10.916206, 'lon': -37.077466, 'name': 'Sergipe'},
        'SP': {'lat': -23.550520, 'lon': -46.633308, 'name': 'São Paulo'},
        'TO': {'lat': -10.249091, 'lon': -48.324286, 'name': 'Tocantins'}
    }
    
    # Dicionário com coordenadas das capitais dos países
    COUNTRY_CAPITALS = {
        'ESTADOS UNIDOS': {'lat': 38.8951, 'lon': -77.0364},
        'URUGUAY': {'lat': -34.9011, 'lon': -56.1645},
        'EL SALVADOR': {'lat': 13.6929, 'lon': -89.2182},
        'COLOMBIA': {'lat': 4.7110, 'lon': -74.0721},
        'MEXICO': {'lat': 19.4326, 'lon': -99.1332},
        'GUATEMALA': {'lat': 14.6349, 'lon': -90.5069},
        'PARAGUAI': {'lat': -25.2867, 'lon': -57.3333},
        'COSTA RICA': {'lat': 9.9281, 'lon': -84.0907},
        'HONDURAS': {'lat': 14.0723, 'lon': -87.1921},
        'ARGENTINA': {'lat': -34.6037, 'lon': -58.3816},
        'PERU': {'lat': -12.0464, 'lon': -77.0428},
        'NICARAGUA': {'lat': 12.1149, 'lon': -86.2362},
        'PANAMA': {'lat': 8.9824, 'lon': -79.5199},
        'BELIZE': {'lat': 17.2514, 'lon': -88.7705},
        'ZIMBABWE': {'lat': -17.8292, 'lon': 31.0522}
    }
    
    @classmethod
    def get_location_coordinates(cls, uf: str, cod_pais: str = None) -> dict:
        """Retorna coordenadas baseado na UF ou país"""
        if uf == 'EX':
            # Para exportações, procura pelo nome do país
            return cls.COUNTRY_CAPITALS.get(cod_pais, {})
        return cls.CAPITALS.get(uf, {})

    @classmethod
    def get_location_name(cls, uf: str, cod_pais: str = None) -> str:
        """Retorna o nome formatado da localização"""
        if uf == 'EX':
            return cod_pais
        return cls.CAPITALS.get(uf, {}).get('name', uf) 