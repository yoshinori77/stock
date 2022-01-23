import dash
from dash import dcc, html
from dash import dash_table as dt
from dash.dependencies import Input, Output, State
import flask
from stockstats import StockDataFrame as Sdf
import dash_bootstrap_components as dbc
import yahoo_fin.stock_info as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta
import pickle
import random
import plotly.subplots as sub


# defining style color
colors = {"background": "#000000", "text": "#ffFFFF"}


def line(df):
    # Line plot
    figs = [
        go.Scatter(
            x=list(
                df.index),
            y=list(
                df.close),
            fill="tozeroy",
            name="close"
        )
    ]
    return figs


def candlestick(df):
    # Candelstick
    figs = [
        go.Candlestick(
            x=list(df.index),
            open=list(df.open),
            high=list(df.high),
            low=list(df.low),
            close=list(df.close),
            name="Candlestick",
        )
    ]
    return figs


def ohlc(df):
    # Open_high_low_close
    figs = [
        go.Ohlc(
            x=df.index,
            open=df.open,
            high=df.high,
            low=df.low,
            close=df.close,
        )
    ]
    return figs


def sma(df):
    # Simple moving average
    close_ma_10 = df.close.rolling(10).mean()
    close_ma_30 = df.close.rolling(30).mean()
    close_ma_100 = df.close.rolling(100).mean()
    figs = [
        go.Scatter(
            x=list(
                close_ma_10.index),
            y=list(close_ma_10),
            name="10 Days"),
        go.Scatter(
            x=list(
                close_ma_30.index),
            y=list(close_ma_30),
            name="30 Days"),
        go.Scatter(
            x=list(
                close_ma_100.index),
            y=list(close_ma_100),
            name="100 Days"),
    ]
    return figs


def ema(df):
    # Exponential moving average
    close_ema_10 = df.close.ewm(span=10).mean()
    close_ema_15 = df.close.ewm(span=15).mean()
    close_ema_30 = df.close.ewm(span=30).mean()
    close_ema_100 = df.close.ewm(span=100).mean()
    figs = [
        go.Scatter(
            x=list(
                close_ema_10.index),
            y=list(close_ema_10),
            name="10 Days"),
        go.Scatter(
            x=list(
                close_ema_15.index),
            y=list(close_ema_15),
            name="15 Days"),
        go.Scatter(
            x=list(
                close_ema_30.index),
            y=list(close_ema_30),
            name="30 Days"),
        go.Scatter(
            x=list(
                close_ema_100.index),
            y=list(close_ema_100),
            name="100 Days",
        )
    ]
    return figs


def macd(df, stock):
    # Moving average convergence divergence
    df["MACD"], df["signal"], df["hist"] = (
        stock["macd"],
        stock["macds"],
        stock["macdh"],
    )
    figs = [
        go.Scatter(x=list(df.index), y=list(df.MACD), name="MACD"),
        go.Scatter(x=list(df.index), y=list(
            df.signal), name="Signal"),
        go.Scatter(
            x=list(df.index),
            y=list(df["hist"]),
            line=dict(color="royalblue", width=2, dash="dot"),
            name="Hitogram",
        ),
    ]
    return figs


def rsi(df, stock):
    # Relative strength index
    rsi_6 = stock["rsi_6"]
    rsi_12 = stock["rsi_12"]
    rsi_figs = [
        go.Scatter(x=list(df.index), y=list(
                    rsi_6), name="RSI 6 Day"),
        go.Scatter(x=list(df.index), y=list(
                    rsi_12), name="RSI 12 Day"),
    ]
    return rsi_figs


def beatify_subplots(main_fig, second_fig):
    subplots = sub.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, horizontal_spacing=0.1)
    subplots['layout']['margin'] = {'l': 30, 'r': 10, 'b': 100, 't': 50}
    subplots.add_traces(
        main_fig,
        rows=1, cols=1
    )
    subplots.add_traces(
        second_fig,
        rows=2, cols=1
    )
    subplots.update_layout(
        height=1000,
        showlegend=True,
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font={
            "color": colors["text"]
        },
    )
    subplots.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            activecolor="blue",
            bgcolor=colors["background"],
            buttons=list(
                [
                    dict(count=7, label="10D",
                            step="day", stepmode="backward"),
                    dict(
                        count=15, label="15D", step="day", stepmode="backward"
                    ),
                    dict(
                        count=1, label="1m", step="month", stepmode="backward"
                    ),
                    dict(
                        count=3, label="3m", step="month", stepmode="backward"
                    ),
                    dict(
                        count=6, label="6m", step="month", stepmode="backward"
                    ),
                    dict(count=1, label="1y", step="year",
                            stepmode="backward"),
                    dict(count=5, label="5y", step="year",
                            stepmode="backward"),
                    dict(count=1, label="YTD",
                            step="year", stepmode="todate"),
                    dict(step="all"),
                ]
            ),
        ),
    )
    return subplots


def create_dash2_app(requests_pathname_prefix: str = None) -> dash.Dash:
    with open("app/tickers.pickle", "rb") as f:
        ticker_list = pickle.load(f)

    external_stylesheets = [dbc.themes.SLATE]

    server = flask.Flask(__name__)

    # adding css
    app = dash.Dash(
        __name__,
        server=server,
        requests_pathname_prefix=requests_pathname_prefix,
        external_stylesheets=external_stylesheets)

    app.layout = html.Div(
        style={"backgroundColor": colors["background"]},
        children=[
            html.Div(
                [  # header Div
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Header(
                                    [
                                        html.H1(
                                            "Stock Dashboard",
                                            style={
                                                "textAlign": "center",
                                                "color": colors["text"],
                                            },
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                ]
            ),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Div(
                [  # Dropdown Div
                    dbc.Row(
                        [
                            dbc.Col(  # Tickers
                                dcc.Dropdown(
                                    id="stock_name",
                                    options=[
                                        {
                                            "label": str(ticker_list[i]),
                                            "value": str(ticker_list[i]),
                                        }
                                        for i in range(len(ticker_list))
                                    ],
                                    searchable=True,
                                    value=str(
                                        random.choice(
                                            [
                                                "TSLA",
                                                "GOOGL",
                                                "F",
                                                "GE",
                                                "AAL",
                                                "DIS",
                                                "DAL",
                                                "AAPL",
                                                "MSFT",
                                                "CCL",
                                                "GPRO",
                                                "ACB",
                                                "PLUG",
                                                "AMZN",
                                            ]
                                        )
                                    ),
                                    placeholder="enter stock name",
                                ),
                                width={"size": 3, "offset": 3},
                            ),
                            dbc.Col(  # Graph type
                                dcc.Dropdown(
                                    id="chart",
                                    options=[
                                        {"label": "line", "value": "Line"},
                                        {"label": "candlestick",
                                            "value": "Candlestick"},
                                        {
                                            "label": "Exponential moving average",
                                            "value": "EMA",
                                        },
                                        {"label": "MACD", "value": "MACD"},
                                        {"label": "OHLC", "value": "OHLC"},
                                    ],
                                    value="Line",
                                    style={"color": "#000000"},
                                ),
                                width={"size": 3},
                            ),
                            dbc.Col(  # button
                                dbc.Button(
                                    "Plot",
                                    id="submit-button-state",
                                    className="mr-1",
                                    n_clicks=1,
                                ),
                                width={"size": 2},
                            ),
                        ]
                    )
                ]
            ),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="live price",
                                    config={
                                        "displaylogo": False,
                                        "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                                    },
                                )
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="graph",
                                    config={
                                        "displaylogo": False,
                                        "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                                    },
                                ),
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dt.DataTable(
                                    id="info",
                                    style_table={"height": "auto"},
                                    style_cell={
                                        "white_space": "normal",
                                        "height": "auto",
                                        "backgroundColor": colors["background"],
                                        "color": "white",
                                        "font_size": "16px",
                                    },
                                    style_data={"border": "#4d4d4d"},
                                    style_header={
                                        "backgroundColor": colors["background"],
                                        "fontWeight": "bold",
                                        "border": "#4d4d4d",
                                    },
                                    style_cell_conditional=[
                                        {"if": {"column_id": c},
                                            "textAlign": "center"}
                                        for c in ["attribute", "value"]
                                    ],
                                ),
                                width={"size": 6, "offset": 3},
                            )
                        ]
                    ),
                ]
            ),
        ],
    )

    # Callback main graph

    @app.callback(
        # output
        [Output("graph", "figure"), Output("live price", "figure")],
        # input
        [Input("submit-button-state", "n_clicks")],
        # state
        [State("stock_name", "value"), State("chart", "value")],
    )
    def graph_genrator(n_clicks, ticker, chart_name):

        if n_clicks >= 1:  # Checking for user to click submit button

            # loading data
            start_date = datetime.now().date() - timedelta(days=5 * 365)
            end_data = datetime.now().date()
            df = yf.get_data(
                ticker, start_date=start_date, end_date=end_data, interval="1d"
            )
            stock = Sdf(df)

            # selecting graph type

            # line plot
            if chart_name == "Line":
                figs = line(df)

            # Candelstick
            if chart_name == "Candlestick":
                figs = candlestick(df)

            # Open_high_low_close
            if chart_name == "OHLC":
                figs = ohlc(df)

            # Exponential moving average
            if chart_name == "EMA":
                figs = ema(df)

            # Moving average convergence divergence
            if chart_name == "MACD":
                figs = macd(df, stock)

            figs += sma(df)
            rsi_figs = rsi(df, stock)
            subplots = beatify_subplots(figs, rsi_figs)

        end_data = datetime.now().date()
        start_date = datetime.now().date() - timedelta(days=30)
        res_df = yf.get_data(
            ticker, start_date=start_date, end_date=end_data, interval="1d"
        )
        price = yf.get_live_price(ticker)
        prev_close = res_df.close.iloc[0]

        live_price = go.Figure(
            data=[
                go.Indicator(
                    domain={"x": [0, 1], "y": [0, 1]},
                    value=price,
                    mode="number+delta",
                    title={"text": "Price"},
                    delta={"reference": prev_close},
                )
            ],
            layout={
                "height": 300,
                "showlegend": True,
                "plot_bgcolor": colors["background"],
                "paper_bgcolor": colors["background"],
                "font": {"color": colors["text"]},
            },
        )

        return subplots, live_price

    @app.callback(
        # output
        [Output("info", "columns"), Output("info", "data")],
        # input
        [Input("submit-button-state", "n_clicks")],
        # state
        [State("stock_name", "value")],
    )
    def quotes_genrator(n_clicks, ticker):
        # info table
        current_stock = yf.get_quote_table(ticker, dict_result=False)
        columns = [{"name": i, "id": i} for i in current_stock.columns]
        t_data = current_stock.to_dict("records")

        return columns, t_data

    return app
