from dash import Input, Output, State

def register_rfv_callbacks(app):
    """
    Registra os callbacks para os gráficos RFV
    """
    
    # Callback para Recência
    @app.callback(
        Output("collapse-recencia", "is_open"),
        [Input("btn-recencia", "n_clicks")],
        [State("collapse-recencia", "is_open")],
    )
    def toggle_collapse_recencia(n, is_open):
        if n:
            return not is_open
        return is_open

    # Callback para Frequência
    @app.callback(
        Output("collapse-frequencia", "is_open"),
        [Input("btn-frequencia", "n_clicks")],
        [State("collapse-frequencia", "is_open")],
    )
    def toggle_collapse_frequencia(n, is_open):
        if n:
            return not is_open
        return is_open

    # Callback para Valor
    @app.callback(
        Output("collapse-valor", "is_open"),
        [Input("btn-valor", "n_clicks")],
        [State("collapse-valor", "is_open")],
    )
    def toggle_collapse_valor(n, is_open):
        if n:
            return not is_open
        return is_open 