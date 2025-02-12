"""
Serviço para API do módulo comercial
"""
import os
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
from typing import List, Dict, Any
import plotly.graph_objects as go
from shared.utils.formatters import format_number, format_percentage
from datetime import datetime, timedelta
import random
from config import settings
import streamlit as st  # Adicionar importação do streamlit
import time

logger = logging.getLogger(__name__)

class APIService:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.cliente = settings.API_CLIENTE
        self.id = settings.API_ID
        
    def get_data(self, view: str) -> pd.DataFrame:
        try:
            url = f"{self.base_url}/POWERBI/?CLIENTE={self.cliente}&ID={self.id}&VIEW={view}"
            response = requests.get(url, timeout=settings.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Erro ao obter dados da API {view}: {str(e)}")
            return pd.DataFrame()

    def get_all_data(self) -> Dict[str, pd.DataFrame]:
        """Obtém dados de todas as APIs necessárias"""
        views = {
            'faturamento': 'CUBO_FATURAMENTO',
            'orcamento': 'ORCAMENTO',
            'os': 'OS'
        }
        
        dataframes = {}
        for key, view in views.items():
            try:
                dataframes[key] = self.get_data(view)
            except Exception as e:
                raise Exception(f"Erro ao carregar {key}: {str(e)}")
                
        return dataframes

class ComercialAPIService:
    def __init__(self):
        logger.debug("=== Iniciando ComercialAPIService ===")
        
        # URL base correta
        self.base_url = 'http://tecnolife.empresamix.info:8077'
        self.client = 'TECNOLIFE'
        self.api_id = 'XIOPMANA'
        self.view = None
        
        # Configuração de session com headers específicos
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive'
        })
    
    def get_data(self, cube: str = None) -> pd.DataFrame:
        max_attempts = 3
        attempt = 0
        
        while attempt < max_attempts:
            try:
                attempt += 1
                self.view = cube or self.view
                
                # Primeiro, tenta limpar a sessão existente
                clear_url = f"{self.base_url}/POWERBI/clear-session"
                try:
                    self.session.get(clear_url, timeout=5)
                except:
                    pass  # Ignora erros na limpeza
                
                # Aguarda um pouco antes da próxima requisição
                time.sleep(2)
                
                # URL principal
                url = f"{self.base_url}/POWERBI/?CLIENTE={self.client}&ID={self.api_id}&VIEW={self.view}"
                logger.info(f"Tentativa {attempt} de {max_attempts} para {self.view}")
                
                # Adiciona um parâmetro timestamp para evitar cache
                timestamp = int(time.time())
                url = f"{url}&_={timestamp}"
                
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 500:
                    error_text = response.text
                    logger.error(f"Erro 500 recebido. Conteúdo: {error_text}")
                    
                    if "A component named DM already exists" in error_text:
                        logger.warning("Erro do PowerBI detectado, aguardando...")
                        # Aguarda mais tempo entre tentativas
                        time.sleep(10)  # Aumentado para 10 segundos
                        
                        # Tenta limpar o cache do PowerBI
                        try:
                            clear_cache_url = f"{self.base_url}/POWERBI/refresh"
                            self.session.get(clear_cache_url, timeout=5)
                        except:
                            pass
                        
                        continue
                    
                    if attempt < max_attempts:
                        time.sleep(5 * attempt)
                        continue
                    else:
                        return pd.DataFrame()
                
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    logger.warning("Dados vazios recebidos")
                    if attempt < max_attempts:
                        time.sleep(5)
                        continue
                    return pd.DataFrame()
                
                df = pd.DataFrame(data)
                logger.info(f"Dados recebidos com sucesso: {len(df)} registros")
                return df
                
            except Exception as e:
                logger.error(f"Erro na tentativa {attempt}: {str(e)}")
                if attempt == max_attempts:
                    return pd.DataFrame()
                time.sleep(5 * attempt)
        
        return pd.DataFrame()

    def get_dados_rfv(self, anos_selecionados: List[int]) -> pd.DataFrame:
        """
        Obtém os dados para análise RFV
        """
        try:
            # Usa o método get_data() que já está funcionando
            df = self.get_data("CUBO_FATURAMENTO")
            
            if df.empty:
                logger.warning("Nenhum dado retornado da API")
                return pd.DataFrame()
            
            # Converte datas com tratamento de erros
            df['data'] = pd.to_datetime(df['data'], errors='coerce')
            df = df.dropna(subset=['data'])  # Remove linhas com datas inválidas
            
            # Filtra por anos selecionados
            df['ano'] = df['data'].dt.year
            df = df[df['ano'].isin(anos_selecionados)]
            
            # Calcula métricas RFV
            if not df.empty:
                df = df.groupby('codcli').agg({
                    'data': lambda x: (pd.Timestamp.now() - x.max()).days,  # Recência
                    'nota': 'count',  # Frequência (contagem de notas fiscais)
                    'valorfaturado': 'sum'  # Valor total
                }).reset_index()
                
                # Renomeia as colunas
                df.columns = ['cliente_id', 'recencia', 'frequencia', 'valor']
            
            logger.info(f"Dados RFV processados: {len(df)} registros")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao processar dados RFV: {str(e)}")
            return pd.DataFrame() 

    def get_leads_data(self):
        """Obtém dados combinados de leads e faturamento"""
        try:
            # Busca dados do faturamento
            df_faturamento = self.get_data("CUBO_FATURAMENTO")
            
            # Busca dados de clientes
            df_clientes = self.get_data("CLIENTE")
            
            # Merge dos dataframes
            df_combined = pd.merge(
                df_clientes,
                df_faturamento,
                on='codcli',
                how='left'
            )
            
            # Garante que as colunas numéricas estão no formato correto
            numeric_columns = df_combined.select_dtypes(include=['int64', 'float64']).columns
            for col in numeric_columns:
                df_combined[col] = pd.to_numeric(df_combined[col], errors='coerce')
            
            # Define o locale para formatação brasileira
            import locale
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            
            return df_combined
            
        except Exception as e:
            logger.error(f"Erro ao buscar dados de leads: {str(e)}")
            return pd.DataFrame() 

    def get_pipeline_data(self) -> pd.DataFrame:
        """
        Obtém os dados do pipeline de vendas
        Simulação de dados para desenvolvimento
        """
        try:
            # Lista de status possíveis
            status_list = ['Prospecção', 'Proposta', 'Negociação', 'Fechamento']
            vendedores = ['João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa']
            
            # Gera dados simulados
            data = []
            for _ in range(100):  # 100 oportunidades
                status = random.choice(status_list)
                vendedor = random.choice(vendedores)
                
                # Data de criação entre 90 dias atrás e hoje
                dias_atras = random.randint(0, 90)
                data_criacao = datetime.now() - timedelta(days=dias_atras)
                
                # Valor entre 10k e 500k
                valor = random.uniform(10000, 500000)
                
                # Tempo na etapa atual (dias)
                tempo_etapa = random.randint(1, 30)
                
                data.append({
                    'status': status,
                    'vendedor': vendedor,
                    'data_criacao': data_criacao,
                    'valor': valor,
                    'tempo_etapa': tempo_etapa
                })
            
            # Cria DataFrame
            df = pd.DataFrame(data)
            
            return df
            
        except Exception as e:
            print(f"Erro ao obter dados do pipeline: {str(e)}")
            return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro 