def validate_ticker_symbol(symbol):
    # Validate the ticker symbol format (e.g., length and allowed characters)
    if isinstance(symbol, str) and len(symbol) > 0 and len(symbol) <= 5:
        return True
    return False

def format_currency(value):
    # Format a numeric value as currency
    return "${:,.2f}".format(value)

def format_percentage(value):
    # Format a numeric value as a percentage
    return "{:.2f}%".format(value)