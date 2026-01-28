import yfinance as yf
from utils.cache import cache

def get_market_data(ticker: str):# Check cache first
    if ticker in cache:
        return cache[ticker]
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1y")  # last 1 year

        if history.empty:
            return {"error": "Ticker not found or no data available"}

        data = {
            "ticker": ticker,
            "prices": history["Close"].tolist(),
            "dates": history.index.strftime("%Y-%m-%d").tolist()
        }

        # store in cache
        cache[ticker] = data
        return data

    except Exception as e:
        return {"error": str(e)}
