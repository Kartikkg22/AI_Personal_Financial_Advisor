import requests
import pandas as pd
from datetime import datetime

# API endpoint (replace with the exact endpoint found in the Network tab)
url = "https://www.google.com/finance/quote/INFY:NSE"

# Make a request to Google Finance
response = requests.get(url)

if response.status_code == 200:
    # Extract the relevant data (example structure may vary based on API response)
    json_data = response.json()  # Assuming the API returns JSON
    stock_price = json_data["price"]  # Replace with the actual field name in the API response
    stock_name = json_data["name"]    # Replace with the actual field name

    # Prepare data for Excel
    data = {
        "Stock Name": [stock_name],
        "Stock Price": [stock_price],
        "Timestamp": [datetime.now()]
    }

    # Convert to a DataFrame
    df = pd.DataFrame(data)

    # Save to Excel
    df.to_excel("stock_prices.xlsx", index=False)
    print("Real-time stock price saved to Excel!")
else:
    print("Failed to fetch data. Status code:", response.status_code)
