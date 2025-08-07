import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ALPHA_VANTAGE_API_KEY = "T90T247V2L40B207"

def get_stock_data(ticker):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "OVERVIEW",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    r = requests.get(url, params=params)
    data = r.json()
    if not data or "Name" not in data:
        return None
    return {
        "Ticker": ticker.upper(),
        "Name": data.get("Name", "N/A"),
        "Price": get_stock_price(ticker),
        "1 Day Change": "N/A",  # Alpha Vantage free API does not provide this directly
        "P/E Ratio": data.get("PERatio", "N/A"),
        "Market Cap": data.get("MarketCapitalization", "N/A"),
        "Sector": data.get("Sector", "N/A")
    }

def get_historical_prices(ticker, start_date=None, end_date=None):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "outputsize": "full",
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    r = requests.get(url, params=params)
    data = r.json()
    time_series = data.get("Time Series (Daily)", {})
    prices = []
    for date, values in time_series.items():
        if (not start_date or date >= start_date) and (not end_date or date <= end_date):
            prices.append({"date": date, "close": float(values["4. close"])})
    # Sort by date ascending
    prices.sort(key=lambda x: x["date"])
    return prices

@app.route('/api/price_history')
def price_history():
    ticker = request.args.get('ticker')
    start = request.args.get('start')
    end = request.args.get('end')
    prices = get_historical_prices(ticker, start, end)
    return jsonify(prices)

def get_stock_price(ticker):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    r = requests.get(url, params=params)
    data = r.json()
    price = data.get("Global Quote", {}).get("05. price", "N/A")
    return f"${price}"

def get_news(ticker):
    # Alpha Vantage does not provide news in the free tier.
    # You can use Finnhub or another API for news.
    return [
        {
            "title": "No news available (demo)",
            "url": "#",
            "published_at": "",
            "summary": ""
        }
    ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stock')
def stock():
    ticker = request.args.get('ticker')
    if not ticker:
        return render_template('stock_detail.html', stock_data=None, news=[])
    stock_data = get_stock_data(ticker)
    news = get_news(ticker)
    return render_template('stock_detail.html', stock_data=stock_data, news=news)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)