import time
import hmac
import hashlib
import base64
import requests
import pandas as pd
from config import API_KEY, api_secret, GRAPH_API_URL, BASE_URL, logger
from utils import format_quantity

# API çağrıları için gerekli başlıkları oluşturan fonksiyon
def get_headers(endpoint, nonce):
    data = f"{API_KEY}{nonce}".encode('utf-8')
    signature = hmac.new(api_secret, data, hashlib.sha256).digest()
    signature = base64.b64encode(signature).decode('utf-8')
    return {
        'X-PCK': API_KEY,
        'X-Stamp': nonce,
        'X-Signature': signature,
        'Content-Type': 'application/json',
    }

# OHLCV (Open, High, Low, Close, Volume) verilerini API'den çeken fonksiyon
def get_ohlcv(symbol, limit=100):
    endpoint = f'/v1/ohlcs?pair={symbol}'
    url = GRAPH_API_URL + endpoint
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching OHLCV data: {e}")
        return pd.DataFrame()
    
    data = response.json()
    if not data:
        logger.error("No data received from API")
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df.tail(limit)

# Bir işlem emri (order) yerleştiren fonksiyon
def place_order(symbol, side, quantity, price=0, stop_loss=None, take_profit=None):
    endpoint = '/api/v1/order'
    nonce = str(int(time.time() * 1000))
    formatted_quantity = format_quantity(quantity, precision=8)
    params = {
        'pairSymbol': symbol,
        'quantity': f"{formatted_quantity:.8f}",
        'price': f"{price:.2f}" if price != 0 else 0,
        'orderType': 0 if side == 'buy' else 1,
        'orderMethod': 1,
        'stopPrice': f"{stop_loss:.2f}" if stop_loss else None,
        'takeProfitPrice': f"{take_profit:.2f}" if take_profit else None,
    }
    headers = get_headers(endpoint, nonce)
    url = BASE_URL + endpoint
    try:
        response = requests.post(url, headers=headers, json=params)
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error placing order: {e}")
        return None
    except requests.exceptions.JSONDecodeError:
        logger.error(f"Error placing order: {response.status_code} - Response is not JSON.")
        logger.error(f"Raw response content: {response.text}")
        return None
    if response.status_code != 200:
        logger.error(f"Error placing order: {response.status_code} - {response_data}")
        return None
    
    logger.info(f"Order placed: {response_data}")
    return response_data

# Kullanıcı bakiyesini çeken fonksiyon
def get_account_balance():
    endpoint = '/api/v1/users/balances'
    nonce = str(int(time.time() * 1000))
    headers = get_headers(endpoint, nonce)
    url = BASE_URL + endpoint
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching account balance: {e}")
        return []
    
    logger.info("Account balance fetched successfully.")
    return response.json().get('data', [])