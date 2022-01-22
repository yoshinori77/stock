import dash
from dash.dependencies import Input, Output
from dash import dcc, html
from yahoofinancials import YahooFinancials
import shellinford

import flask
import pandas as pd
import os


def create_dash_app(requests_pathname_prefix: str = None) -> dash.Dash:
    """
    Sample Dash application from Plotly: https://github.com/plotly/dash-hello-world/blob/master/app.py
    """
    server = flask.Flask(__name__)

    # server.secret_key = os.environ.get('secret_key', 'secret')

    df = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/hello-world-stock.csv')

    app = dash.Dash(
        __name__,
        server=server,
        requests_pathname_prefix=requests_pathname_prefix)

    app.scripts.config.serve_locally = False
    dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

    ALLOWED_TYPES = (
        "text", "number", "password", "email", "search",
        "tel", "url", "range", "hidden",
    )

    app.layout = html.Div(
        # [
        #     dcc.Input(
        #         id="input_{}".format(_),
        #         type=_,
        #         placeholder="input type {}".format(_),
        #     )
        #     for _ in ALLOWED_TYPES
        # ]
        # + [html.Div(id="out-all-types")],
        [
            html.H1('Stock Tickers'),
            dcc.Input(
                id="input_brand",
                type="text",
                placeholder="input stock brand name",
            ),
            html.Div(id="out-all-types"),
            dcc.Dropdown(
                id='my-dropdown',
                options=[
                    {'label': 'Tesla', 'value': 'TSLA'},
                    {'label': 'Apple', 'value': 'AAPL'},
                    {'label': 'Coke', 'value': 'COKE'},
                    {'label': 'DeNA', 'value': '2432.T'}
                ],
                # multi=True,
                value='TSLA'
            ),
            dcc.Graph(id='my-graph')
        ], className="container"
    )

    @app.callback(Output('my-graph', 'figure'),
                  [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):
        yahoo_financials = YahooFinancials(selected_dropdown_value)
        daily_stock_info = yahoo_financials.get_historical_price_data(
            '2017-01-22', '2022-01-22', 'daily')
        daily_stock_prices = daily_stock_info[selected_dropdown_value]['prices']
        daily_close_prices = list(map(lambda x: x['close'], daily_stock_prices))
        daily_formatted_date = list(map(lambda x: x['formatted_date'], daily_stock_prices))

        # dff = df[df['Stock'] == selected_dropdown_value]
        return {
            'data': [{
                'x': daily_formatted_date,
                'y': daily_close_prices,
                'line': {
                    'width': 3,
                    'shape': 'spline'
                }
            }],
            'layout': {
                'margin': {
                    'l': 30,
                    'r': 20,
                    'b': 30,
                    't': 20
                }
            }
        }

    @app.callback(
        Output("out-all-types", "children"),
        [Input("input_brand", "value")],
    )
    def cb_render(*vals):
        print(vals)
        fm = shellinford.FMIndex()
        fm.read('brand.fm')
        docs = fm.search(vals)
        print(docs)
        if docs is not None:
            for doc in fm.search(vals):
                return doc.text

                # return [filter(str.isalnum, text)for text in doc.text.split('\t')].join()


        # return " | ".join((str(val) for val in vals if val))

    return app
