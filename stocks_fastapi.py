from fastapi import FastAPI, HTTPException

from data_pipeline import generate_insights,get_volume_close_data,generate_metrics

app = FastAPI(title="Stock Data API")


def normalize_symbol(symbol: str) -> str:
    symbol = symbol.upper()
    if "." not in symbol:
        symbol = f"{symbol}.NS"
    return symbol

@app.get("/health")
def health_check():
    """Simple health check for liveness/readiness."""
    return {
        "status": "healthy",
        "service": "Stock Data API",
        "version": "1.0",
        "message": "OK"
    }


@app.get("/data/close")
def get_close_volume_data(symbol: str, start: str, end: str):
    try:
        symbol = normalize_symbol(symbol)
        data = get_volume_close_data(symbol, start, end)
        return {"symbol": symbol, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/summary")
def get_summary(symbol:str,period:str):
    try:
        symbol=normalize_symbol(symbol)
        summary=generate_metrics(ticker_symbol=symbol,period=period)
        return {"symbol":symbol,"data":summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary for {symbol}: {str(e)}")

@app.get("/insights/{symbol}")
def get_insights(symbol: str,period:str):
    """Get a metrics insights of the stock's current trend and key metrics."""
    try:
        symbol = normalize_symbol(symbol)

        summary=generate_insights(symbol=symbol,period=period)

        return {"symbol": symbol, "data": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary for {symbol}: {str(e)}")

@app.get("/compare")
def compare(symbol1: str, symbol2: str,period:str)-> dict:
    """Compare two stocks based on their latest trends and key metrics."""
    try:
        symbol1 = normalize_symbol(symbol1)
        symbol2 = normalize_symbol(symbol2)

        result= {
            "symbol1": generate_insights(symbol=symbol1,period=period),
            "symbol2": generate_insights(symbol=symbol2,period=period)
        }
        
        return {"symbol1": symbol1,"symbol2":symbol2, "data": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to Compare {symbol1} and {symbol2}: {e}")
