import yfinance as yf

class YFApp:
    def __init__(self):
        pass

    def get_ticker_info(self, symbol):
        ticker = yf.Ticker(symbol)
        return ticker.info

    def get_ticker_calendar(self, symbol):
        ticker = yf.Ticker(symbol)
        return ticker.calendar

    def get_analyst_price_targets(self, symbol):
        ticker = yf.Ticker(symbol)
        return ticker.analyst_price_targets

    def get_quarterly_income_stmt(self, symbol):
        ticker = yf.Ticker(symbol)
        return ticker.quarterly_income_stmt

    def get_ticker_history(self, symbol, period='1mo'):
        ticker = yf.Ticker(symbol)
        return ticker.history(period=period)

    def get_option_chain_calls(self, symbol):
        ticker = yf.Ticker(symbol)
        return ticker.option_chain(ticker.options[0]).calls

    def get_multiple_tickers_info(self, symbols):
        tickers = yf.Tickers(symbols)
        return {symbol: tickers.tickers[symbol].info for symbol in symbols}

    def download_multiple_tickers(self, symbols, period='1mo'):
        return yf.download(symbols, period=period)

    def get_symbol_description(self, symbol):
        ticker = yf.Ticker(symbol)
        return ticker.funds_data.description

    def get_symbol_top_holdings(self, symbol):
        ticker = yf.Ticker(symbol)
        return ticker.funds_data.top_holdings