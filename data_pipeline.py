import yfinance as yf
import pandas as pd

def get_data(ticker_symbol: str, start: str=None, end: str=None,period:str=None):
    try:
        df = yf.download(tickers=ticker_symbol, start=start, end=end, period=period)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except Exception:
        return pd.DataFrame

def get_volume_close_data(ticker_symbol: str, start: str, end: str):
    df=get_data(ticker_symbol=ticker_symbol,start=start,end=end)
    if df.empty:
        raise ValueError(
            f"No data found for '{ticker_symbol}'. "
            f"For Indian NSE stocks, use the '.NS' suffix (e.g. 'TCS.NS')."
        )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()
    df.columns.name = None

    final_df = df[["Date", "Volume", "Close"]].copy()
    final_df["Date"] = final_df["Date"].astype(str)

    return final_df.to_dict(orient="records")
    
def generate_metrics(ticker_symbol: str, period:str='13mo'):
    try:
        df=get_data(ticker_symbol=ticker_symbol,period=period)
        # Metrics
        
        df['Daily Return'] = (df['Close'] - df['Open']) / df['Open']
        df['MA_7'] = df['Close'].rolling(7).mean()
        df['MA_30'] = df['Close'].rolling(30).mean()
        df['Volatility'] = df['Daily Return'].rolling(7).std()
        df['Momentum'] = df['Close'] - df['Close'].shift(7)

        df['Trend'] = (df['MA_7'] > df['MA_30']).map({True: "Uptrend", False: "Downtrend"})

        threshold = df['Volatility'].quantile(0.75)
        df['Risk'] = (df['Volatility'] > threshold).map({True: "High", False: "Low"})

        df=df.reset_index()
        df.dropna(subset=['MA_7', 'MA_30', 'Volatility'], inplace=True)

        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].round(2)

        return df.to_dict(orient="records")
    
    except Exception as e:
        raise RuntimeError(f"Error generating metrics: {e}")


def generate_insights(symbol:str,period:str='13mo'):

    df=generate_metrics(ticker_symbol=symbol,period=period)
    if df is None:
        return {"error": "No data available"}
    
    df=pd.DataFrame(df)
    latest = df.iloc[-1]
    return {
        "latestday_trend": latest['Trend'],
        "latestday_risk": latest['Risk'],
        "latest_close": float(latest['Close']),
        "avg_return": float(df['Daily Return'].mean()),
        "52w_high": float(df['Close'].max()),
        "52w_low": float(df['Close'].min()),
    }
