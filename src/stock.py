import ipdb
import pandas as pd
from yahoofinancials import YahooFinancials

tech_stocks = ['AAPL', 'MSFT', 'INTC']
ipdb.set_trace()
yahoo_financials_tech = YahooFinancials(tech_stocks)
tech_cash_flow_data_an = yahoo_financials_tech.get_financial_stmts(
    'annual', 'cash')
tech_stock_price_data = yahoo_financials_tech.get_stock_price_data()
daily_tech_stock_prices = yahoo_financials_tech.get_historical_price_data('2008-09-15', '2018-09-15', 'daily')

tech_close_prices = []
for t in tech_stocks:
    prices = daily_tech_stock_prices[t]['prices']
    close_prices = [p['close'] for p in prices]
    tech_close_prices.append(close_prices)


def calc_rsi(price, n=14):
    gain = (price - price.shift(1)).fillna(0)

    def rsiCalc(p):
        avgGain = p[p > 0].sum() / n
        avgLoss = -p[p < 0].sum() / n
        rs = avgGain / avgLoss
        return 100 - 100 / (1 + rs)

    return gain.rolling(14).apply(rsiCalc)


apple = pd.Series(tech_close_prices[0])
calc_rsi(pd.Series(tech_close_prices[0]))

import talib
talib.RSI(apple)
# with open('sample_daily_stock_price.json', 'w') as f:
#     json.dump(daily_tech_stock_prices, f, indent=4)
