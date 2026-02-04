from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from yf_app import YFApp

yf_app = YFApp()
app = FastAPI(
    title="Vercel + FastAPI",
    description="Vercel + FastAPI",
    version="1.0.0",
)


@app.post("/api/process-ticker")
async def process_ticker_webhook(request: Request):
    """
    Receives webhook from Notion automation
    Expected payload from Notion:
    {
        "Created time": "2024-01-01T00:00:00Z",
        "AI Summary": "some text",
        "Tickers": "AAPL, MSFT, GOOGL",
        "Tickers Formated": "AAPL, MSFT, GOOGL"
    }
    """
    # Get the data from Notion
    data = await request.json()
    
    # Extract the fields Notion sends
    created_time = data.get("Created time")
    ai_summary = data.get("AI Summary")
    tickers_raw = data.get("Tickers", "")
    tickers_formatted = data.get("Tickers Formated", "")
    
    # Parse tickers (use formatted version, fallback to raw)
    ticker_string = tickers_formatted or tickers_raw
    tickers = [t.strip() for t in ticker_string.split(",") if t.strip()]
    
    # Return quick response to Notion (so it doesn't timeout)
    response = {
        "status": "received",
        "tickers_count": len(tickers),
        "tickers": tickers
    }
    
    # TODO: Process tickers async and update Notion
    # For now, let's just return what we received
    
    return response


@app.post("/api/get-fundamentals")
async def get_fundamentals(request: Request):
    """
    Endpoint to fetch fundamental data for ticker(s)
    """
    data = await request.json()
    ticker_symbol = data.get("ticker")
    
    if not ticker_symbol:
        return {"error": "ticker is required"}
    
    try:
        # Fetch data from yfinance
        info = yf_app.get_ticker_info(ticker_symbol)
        
        # Extract key fundamentals
        fundamentals = {
            "ticker": ticker_symbol,
            "company_name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "price": info.get("currentPrice"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "dividend_yield": info.get("dividendYield"),
            "beta": info.get("beta"),
            "revenue": info.get("totalRevenue"),
            "profit_margin": info.get("profitMargins"),
            "debt_to_equity": info.get("debtToEquity"),
            "analyst_recommendation": info.get("recommendationKey"),
            "target_price": info.get("targetMeanPrice"),
        }
        
        return {"success": True, "data": fundamentals}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
