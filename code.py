# ==========================================
# STEP 1: IMPORT LIBRARIES
# ==========================================
import pandas as pd
import yfinance as yf
from datetime import date, timedelta
import plotly.graph_objects as go # For creating interactive charts (candlestick, line plots, etc.)
import plotly.io as pio # For rendering plotly charts

# Set default Plotly renderer to browser (opens charts in your default web browser)
# If using VS Code, you can change this to "vscode"
pio.renderers.default = "browser"

# ==========================================
# STEP 2: FETCH HISTORICAL BITCOIN DATA
# ==========================================
today = date.today()
end_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
start_date = (today - timedelta(days=730)).strftime("%Y-%m-%d")

# Download data
data = yf.download(
    "BTC-USD",
    start=start_date,
    end=end_date,
    progress=False,
    auto_adjust=False,
    group_by="ticker"  # <--- ensures MultiIndex format is returned
)

# ---- Handle MultiIndex or Empty Data ----
if data.empty:
    print("⚠️ No data returned from Yahoo Finance. Try again later.")
else:
    # If MultiIndex, flatten columns properly
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[1] if col[1] != "" else col[0] for col in data.columns]

    # Verify columns
    print("Available columns after flattening:", data.columns.tolist())

    # Keep only expected columns
    cols_to_keep = [col for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume"] if col in data.columns]
    data = data[cols_to_keep].copy()

    # Drop missing data
    data.dropna(inplace=True)

    # Add Date column
    data["Date"] = data.index

    print(f"✅ Data downloaded successfully! ({len(data)} rows)")
    print(data.head())

    # ==========================================
    # STEP 3: VISUALIZE PRICE TRENDS
    # ==========================================
    figure = go.Figure(
        data=[
            go.Candlestick(
                x=data["Date"],
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"]
            )
        ]
    )

    figure.update_layout(
        title="📈 Bitcoin Price Analysis (Last 2 Years)",
        xaxis_title="Date",
        yaxis_title="BTC-USD Price (USD)",
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )

    figure.show()

# ==========================================
# STEP 2.1: HANDLE EMPTY OR MULTIINDEX DATA
# ==========================================

# If Yahoo Finance returns no data, show a warning message
if data.empty:
    print("⚠️ No data returned from Yahoo Finance. Try again later.")
else:
    # If data has MultiIndex columns (e.g., ('BTC-USD', 'Open')), flatten them
    if isinstance(data.columns, pd.MultiIndex):
        # Extract the second level of the column tuple (like 'Open', 'High', etc.)
        data.columns = [col[1] if col[1] != "" else col[0] for col in data.columns]

# Print available columns after flattening (for verification)
    print("Available columns after flattening:", data.columns.tolist())

    # Keep only the standard OHLCV (Open, High, Low, Close, Adj Close, Volume) columns
    cols_to_keep = [col for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume"] if col in data.columns]
    data = data[cols_to_keep].copy() 

# Drop any rows with missing (NaN) values to avoid visualization errors
    data.dropna(inplace=True)

    # Add a 'Date' column derived from the DataFrame index for plotting purposes
    data["Date"] = data.index
       
# Display confirmation message and preview first few rows
    print(f"✅ Data downloaded successfully! ({len(data)} rows)")
    print(data.head())


# STEP 3: VISUALIZE PRICE TRENDS (CANDLESTICK CHART)

# Create an interactive candlestick chart using Plotly
    # Each candlestick shows the opening, closing, highest, and lowest price for a given day
    figure = go.Figure(
        data=[
            go.Candlestick(
                x=data["Date"],        # X-axis: Date
                open=data["Open"],     # Y-axis (top of candle): Opening price
                high=data["High"],     # Y-axis (top wick): Highest price
                low=data["Low"],       # Y-axis (bottom wick): Lowest price
                close=data["Close"]    # Y-axis (bottom of candle): Closing price
            )
        ]
    )

# Customize the chart layout: titles, labels, and appearance
    figure.update_layout(
        title="📈 Bitcoin Price Analysis (Last 2 Years)",   # Chart title
        xaxis_title="Date",                                # Label for X-axis
        yaxis_title="BTC-USD Price (USD)",                 # Label for Y-axis
        xaxis_rangeslider_visible=False,                   # Hide date range slider for cleaner look
        template="plotly_dark"                             # Use a dark theme for a modern appearance
    )

    # Display the chart in browser or VS Code (depending on renderer setting)
    figure.show()