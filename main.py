from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from binance.client import Client
import hmac
import hashlib
import time
import os

app = FastAPI()

# Wprowadź tutaj swoje klucze Binance API
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY") or "TU_WKLEJ_API_KEY"
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET") or "TU_WKLEJ_SECRET"

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# Model danych przyjmowanych z TradingView
class TradingViewAlert(BaseModel):
    symbol: str
    side: str  # 'buy' lub 'sell'
    entry: str = None
    exit: str = None

@app.post("/trade")
async def handle_trade(alert: TradingViewAlert):
    symbol = alert.symbol.upper()  # np. BTCUSDC
    side = alert.side.lower()      # buy / sell

    # Binance wymaga symbol w formacie BTCUSDT albo BTCUSDC, upewnij się, że jest OK
    # Ten przykład działa na Binance Spot

    quantity = 0.001  # wielkość pozycji, ustaw według swojego zarządzania kapitałem

    try:
        if side == "buy":
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            return {"status": "success", "message": "Buy order executed", "order": order}

        elif side == "sell":
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            return {"status": "success", "message": "Sell order executed", "order": order}

        else:
            raise HTTPException(status_code=400, detail="Invalid side, must be 'buy' or 'sell'")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
