
import pandas as pd
import yfinance as yf


def getData(tickers: list, start: str = None, end: str = None, period: str = '1mo', interval: str = '1d') -> pd.DataFrame:
    """
    Retrieve data from yfinance library for specified tickers.

    Parameters
    ----------
    tickers : list
        symbol or list of symbols
    start : str, optional
        start date, by default None
    end : str, optional
        end date, by default None
    period : str, optional
        period, by default '1mo'
        valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    interval : str, optional
        interval, by default '1d', max 60 days
        valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

    Returns
    -------
    pd.DataFrame
        DataFrame with OHLC[A]V (Open, High, Low, Close, Adj Close, Volume).
    """
    return yf.download(tickers, start=None, end=None, auto_adjust=True, progress=False, period=period, interval=interval)
    

# Retrieve ticker object from yfinance library
def getTicker(ticker: str) -> yf.Ticker:
    """
    Retrieve ticker object from yfinance library.

    Parameters
    ----------
    ticker : str
        symbol

    Returns
    -------
    yf.Ticker
        Ticker object
    """

    # for all available options, refer yfinance
    # .info
    # .history      
    # .actions
    # .dividends
    # .splits
    # .financials
    # .quarterly_financials
    # .major_holders
    # .institutional_holders
    # .balance_sheet
    # .quarterly_balance_sheet
    # .cashflow
    # .quarterly_cashflow
    # .earnings
    # .quarterly_earnings
    # .sustainability
    # .recommendations
    # .calendar
    # .earnings_dates
    # .isin
    # .options
    #. option_chain('YYYY-MM-DD')
    # .news

    return yf.Ticker(ticker)
