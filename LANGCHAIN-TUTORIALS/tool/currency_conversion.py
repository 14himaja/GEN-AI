from langchain_core.tools import tool
import requests

@tool
def currency_converter(amount, from_currency, to_currency):
    """Convert currency from one currency to another."""

    # API URL
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"

    # Get exchange rate
    response = requests.get(url)
    data = response.json()

    # Get target currency rate
    rate = data["rates"][to_currency]

    # Convert amount
    return amount * rate


result = currency_converter(500, "USD", "INR")

print(result)