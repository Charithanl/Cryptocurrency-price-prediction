#import necessary libraries
import pandas as pd
import yfinance as yf
from datetime import date, timedelta

# Get today's date
today = date.today()

# Define date range (past 2 years)
end_date = today.strftime("%Y-%m-%d")
start_date = (today - timedelta(days=730)).strftime("%Y-%m-%d")

# Download BTC-USD data
data = yf.download(
    'BTC-USD',
    start=start_date,
    end=end_date,
    progress=False,
    auto_adjust=False  # ensures 'Adj Close' column exists
)

# Add Date column
data["Date"] = data.index

# Select only available columns safely
expected_cols = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
available_cols = [col for col in expected_cols if col in data.columns]
data = data[available_cols]

# Reset index
data.reset_index(drop=True, inplace=True)

# Display
print(data.head())
