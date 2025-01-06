import streamlit as st
from typing import List, Dict, Any, Callable

class DashboardLayout:
    @staticmethod
    def create_metric_row(metrics: List[Dict[str, Any]]):
        """Cria uma linha de métricas"""
        cols = st.columns(len(metrics))
        for col, metric in zip(cols, metrics):
            with col:
                st.metric(
                    label=metric['label'],
                    value=metric['value'],
                    delta=metric.get('delta')
                )
    
    @staticmethod
    def create_chart_grid(
        charts: List[Callable],
        cols: int = 2
    ):
        """Cria um grid de gráficos"""
        for i in range(0, len(charts), cols):
            row_charts = charts[i:i+cols]
            row = st.columns(cols)
            for col, chart_func in zip(row, row_charts):
                with col:
                    chart_func() 