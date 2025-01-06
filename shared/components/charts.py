import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional, Union
from shared.utils.cursor_rules import CursorRules

class ChartComponents:
    @staticmethod
    def create_kpi_card(
        title: str,
        value: float,
        prefix: str = "",
        suffix: str = "",
        comparison_value: Optional[float] = None,
        is_currency: bool = False,
        is_percentage: bool = False
    ):
        """Cria um card de KPI padronizado"""
        if is_currency:
            formatted_value = CursorRules.format_currency(value)
            if comparison_value:
                formatted_comparison = CursorRules.format_currency(comparison_value)
        elif is_percentage:
            formatted_value = CursorRules.format_percentage(value)
            if comparison_value:
                formatted_comparison = CursorRules.format_percentage(comparison_value)
        else:
            formatted_value = f"{prefix}{value}{suffix}"
            if comparison_value:
                formatted_comparison = f"{prefix}{comparison_value}{suffix}"
        
        st.markdown(
            f"""
            <div style="
                padding: 20px;
                border-radius: 10px;
                background-color: #1E1E1E;
                margin: 10px 0;
            ">
                <h3 style="margin: 0; color: #CCC;">{title}</h3>
                <p style="
                    font-size: 24px;
                    margin: 10px 0;
                    color: white;
                ">{formatted_value}</p>
                {f'<p style="margin: 0; color: {"green" if value > comparison_value else "red"};">vs {formatted_comparison}</p>' if comparison_value else ''}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def create_bar_chart(
        df: pd.DataFrame,
        x: str,
        y: Union[str, List[str]],
        title: str,
        horizontal: bool = False
    ) -> go.Figure:
        """Cria um gráfico de barras"""
        if isinstance(y, list):
            fig = go.Figure()
            for col in y:
                fig.add_trace(
                    go.Bar(
                        x=df[x] if not horizontal else df[col],
                        y=df[col] if not horizontal else df[x],
                        name=col,
                        orientation='h' if horizontal else 'v'
                    )
                )
        else:
            fig = go.Figure(
                go.Bar(
                    x=df[x] if not horizontal else df[y],
                    y=df[y] if not horizontal else df[x],
                    orientation='h' if horizontal else 'v'
                )
            )
        
        fig.update_layout(
            title=title,
            showlegend=True if isinstance(y, list) else False
        )
        return fig
    
    @staticmethod
    def create_line_chart(
        df: pd.DataFrame,
        x: str,
        y: Union[str, List[str]],
        title: str
    ) -> go.Figure:
        """Cria um gráfico de linha"""
        if isinstance(y, list):
            fig = go.Figure()
            for col in y:
                fig.add_trace(
                    go.Scatter(
                        x=df[x],
                        y=df[col],
                        name=col,
                        mode='lines+markers'
                    )
                )
        else:
            fig = go.Figure(
                go.Scatter(
                    x=df[x],
                    y=df[y],
                    mode='lines+markers'
                )
            )
        
        fig.update_layout(
            title=title,
            showlegend=True if isinstance(y, list) else False
        )
        return fig
    
    @staticmethod
    def create_pie_chart(
        df: pd.DataFrame,
        values: str,
        names: str,
        title: str
    ) -> go.Figure:
        """Cria um gráfico de pizza"""
        fig = go.Figure(
            go.Pie(
                values=df[values],
                labels=df[names],
                hole=0.3
            )
        )
        
        fig.update_layout(title=title)
        return fig 