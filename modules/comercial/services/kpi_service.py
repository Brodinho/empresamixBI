import pandas as pd
from typing import Dict, Any
from datetime import datetime, timedelta
from shared.utils.formatters import format_date

class KPIService:
    def __init__(self, dataframes: Dict[str, pd.DataFrame]):
        # Define o período de 5 anos
        hoje = datetime.now()
        inicio_ano_atual = datetime(hoje.year, 1, 1)
        self.data_inicial = inicio_ano_atual - timedelta(days=365*4)  # 5 anos (4 anos anteriores + ano atual)
        
        # Converte e filtra os dataframes pelo período
        self.df_faturamento = self._filtrar_periodo(dataframes['faturamento'])
        self.df_orcamento = self._filtrar_periodo(dataframes['orcamento'])
        self.df_os = self._filtrar_periodo(dataframes['os'])
        
        print(f"Período de análise: {self.data_inicial.strftime('%d/%m/%Y')} até hoje")
        
    def _filtrar_periodo(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filtra o dataframe pelo período de 5 anos"""
        df = df.copy()
        df['data'] = pd.to_datetime(df['data'], errors='coerce')
        return df[df['data'] >= self.data_inicial]
        
    def calcular_kpis_producao(self) -> Dict[str, Any]:
        """Calcula KPIs para o dashboard de Análise de Produção"""
        try:
            print(f"Total registros após filtro - Faturamento: {len(self.df_faturamento)}")
            print(f"Total registros após filtro - Orçamento: {len(self.df_orcamento)}")
            print(f"Total registros após filtro - OS: {len(self.df_os)}")
            
            # 1. Taxa de aprovação de orçamentos
            # Total de orçamentos excluindo os que ainda estão em análise (status 0)
            orcamentos_finalizados = self.df_orcamento[self.df_orcamento['status'] != 0]
            total_orcamentos = len(orcamentos_finalizados)
            
            # Orçamentos não cancelados (todos exceto status 5)
            orcamentos_aprovados = len(orcamentos_finalizados[orcamentos_finalizados['status'] != 5])
            
            print(f"Total orçamentos finalizados: {total_orcamentos}")
            print(f"Orçamentos aprovados (não cancelados): {orcamentos_aprovados}")
            
            taxa_conversao = (orcamentos_aprovados / total_orcamentos * 100) if total_orcamentos > 0 else 0
            
            # 2. Tempo médio entre orçamento e OS
            df_orc_com_os = self.df_orcamento[self.df_orcamento['os'] != 0].copy()
            print(f"Orçamentos com OS: {len(df_orc_com_os)}")
            
            if not df_orc_com_os.empty:
                df_os_merge = self.df_os[['os', 'data']].copy()
                
                df_merge = pd.merge(
                    df_orc_com_os[['os', 'data']],
                    df_os_merge,
                    on='os',
                    suffixes=('_orc', '_os')
                )
                
                df_merge = df_merge.dropna()
                tempo_medio_orc_os = (df_merge['data_os'] - df_merge['data_orc']).dt.days.mean()
            else:
                tempo_medio_orc_os = 0
            
            # 3. Tempo médio entre OS e faturamento
            df_os_fat = self.df_os[self.df_os['status'] == 4].copy()
            print(f"OS Faturadas: {len(df_os_fat)}")
            if not df_os_fat.empty:
                df_merge = pd.merge(
                    df_os_fat[['os', 'data']],
                    self.df_faturamento[['os', 'data']],
                    on='os',
                    suffixes=('_os', '_fat')
                )
                tempo_medio_os_fat = (df_merge['data_fat'] - df_merge['data_os']).dt.days.mean()
            else:
                tempo_medio_os_fat = 0
            
            # 4. Valor médio de orçamentos aprovados
            df_orc_aprov = self.df_orcamento[self.df_orcamento['os'] != 0]
            print(f"Orçamentos aprovados para média: {len(df_orc_aprov)}")
            valor_medio_aprovados = df_orc_aprov['valor'].mean() if not df_orc_aprov.empty else 0
            
            # 5. Percentual de faturamento via OS
            faturamento_total = self.df_faturamento['valorfaturado'].sum()
            faturamento_os = self.df_faturamento[
                self.df_faturamento['os'] != 0
            ]['valorfaturado'].sum()
            
            print(f"Faturamento total: {faturamento_total}")
            print(f"Faturamento via OS: {faturamento_os}")
            perc_faturamento_os = (faturamento_os / faturamento_total * 100) if faturamento_total > 0 else 0
            
            result = {
                'taxa_conversao': taxa_conversao,
                'tempo_medio_orc_os': tempo_medio_orc_os if not pd.isna(tempo_medio_orc_os) else 0,
                'tempo_medio_os_fat': tempo_medio_os_fat if not pd.isna(tempo_medio_os_fat) else 0,
                'valor_medio_aprovados': valor_medio_aprovados if not pd.isna(valor_medio_aprovados) else 0,
                'perc_faturamento_os': perc_faturamento_os
            }
            print("Valores finais:", result)
            return result
            
        except Exception as e:
            print(f"Erro no cálculo dos KPIs: {str(e)}")
            return {
                'taxa_conversao': 0,
                'tempo_medio_orc_os': 0,
                'tempo_medio_os_fat': 0,
                'valor_medio_aprovados': 0,
                'perc_faturamento_os': 0
            } 