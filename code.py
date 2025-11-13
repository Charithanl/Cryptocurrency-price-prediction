# ==========================================
# STEP 1: IMPORT LIBRARIES
# ==========================================
import pandas as pd
import yfinance as yf
from datetime import date, timedelta
import plotly.graph_objects as go # For creating interactive charts (candlestick, line plots, etc.)
import plotly.io as pio # For rendering plotly charts

# Use VS Code or Browser renderer
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
