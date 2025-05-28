from flask import Flask, request
import hmac
import hashlib
import json
import requests

app = Flask(__name__)

BINANCE_API_KEY = 'YOUR_API_KEY'
BINANCE_API_SECRET = 'YOUR_SECRET_KEY'

def send_binance_order(symbol, side, quantity):
    url = 'https://api.binance.com/api/v3/order'
    headers = {
        'X-MBX-APIKEY': BINANCE_API_KEY
    }

    params = {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
        'quantity': quantity,
        'timestamp': int(requests.get("https://api.binance.com/api/v3/time").json()["serverTime"])
    }

    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(BINANCE_API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params['signature'] = signature

    response = requests.post(url, headers=headers, params=params)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if data.get('passphrase') != 'moje_haslo':  # Ustal hasło do weryfikacji sygnału
        return {'error': 'Nieprawidłowe hasło'}, 403

    symbol = data.get('symbol', 'BTCUSDC')
    quantity = float(data.get('quantity', 0.001))

    result = send_binance_order(symbol=symbol, side='BUY', quantity=quantity)

    return {'result': result}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
