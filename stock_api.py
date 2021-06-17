import yfinance as yf

import utils


def get_stock_analytics(stock_symbol, start='2020-01-01', end='2021-06-15'):
    ticker = yf.Ticker(stock_symbol)
    data = ticker.history(start=start, end=end)['Open']
    figure = utils.get_byte_plot(data)
    emoji = utils.get_current_trend_emoji(data[-1], data[-2])
    return {'current_price': data[-1], 'figure': figure, 'currency': ticker.info.get('currency'),
            'company_name': ticker.info.get('longName'), 'emoji': emoji}

