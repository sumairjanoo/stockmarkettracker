class Stock:
    def __init__(self, ticker, financial_data, ratios, changes, news):
        self.ticker = ticker
        self.financial_data = financial_data
        self.ratios = ratios
        self.changes = changes
        self.news = news

    def get_summary(self):
        return {
            "ticker": self.ticker,
            "financial_data": self.financial_data,
            "ratios": self.ratios,
            "changes": self.changes,
            "news": self.news
        }