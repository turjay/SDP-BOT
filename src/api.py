import time
import hmac
import hashlib
import base64
import requests
import pandas as pd
from config import API_KEY, api_secret, GRAPH_API_URL, BASE_URL, logger
from utils import format_quantity

def get_headers(endpoint: str, nonce: str) -> dict:
    """
    Generates the necessary headers for API calls.

    Args:
        endpoint (str): The API endpoint being accessed.
        nonce (str): A unique number to ensure the request is unique.

    Returns:
        dict: A dictionary containing the headers for the API request.
    """
    # Create the signature for authentication using HMAC and the API secret
    data = f"{API_KEY}{nonce}".encode('utf-8')
    signature = hmac.new(api_secret, data, hashlib.sha256).digest()
    signature = base64.b64encode(signature).decode('utf-8')

    # Return the necessary headers for authentication
    return {
        'X-PCK': API_KEY,
        'X-Stamp': nonce,
        'X-Signature': signature,
        'Content-Type': 'application/json',
    }

def get_ohlcv(symbol: str, limit: int = 100) -> pd.DataFrame:
    """
    Fetches OHLCV (Open, High, Low, Close, Volume) data from the API.

    Args:
        symbol (str): The trading pair symbol (e.g., 'BTCUSD').
        limit (int): The number of data points to return (default is 100).

    Returns:
        pd.DataFrame: A DataFrame containing the OHLCV data, or an empty DataFrame on failure.
    """
    endpoint = f'/v1/ohlcs?pair={symbol}'
    url = GRAPH_API_URL + endpoint
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching OHLCV data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

    data = response.json()
    if not data:
        logger.error("No data received from API")
        return pd.DataFrame()  # Return an empty DataFrame if no data is received

    # Process the data into a DataFrame
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    
    return df.tail(limit)  # Return only the last 'limit' number of rows

def place_order(symbol: str, side: str, quantity: float, price: float = 0, stop_loss: float = None, take_profit: float = None) -> dict:
    """
    Places an order (buy/sell) on the exchange.

    Args:
        symbol (str): The trading pair symbol (e.g., 'BTCUSD').
        side (str): 'buy' for a buy order, 'sell' for a sell order.
        quantity (float): The amount of the asset to trade.
        price (float, optional): The price at which to place the order (default is 0 for market orders).
        stop_loss (float, optional): The price at which to trigger a stop loss.
        take_profit (float, optional): The price at which to trigger a take profit.

    Returns:
        dict or None: The response from the API if successful, otherwise None.
    """
    endpoint = '/api/v1/order'
    nonce = str(int(time.time() * 1000))  # Generate a unique nonce
    formatted_quantity = format_quantity(quantity, precision=8)  # Ensure correct precision for quantity

    # Construct the order parameters
    params = {
        'pairSymbol': symbol,
        'quantity': f"{formatted_quantity:.8f}",
        'price': f"{price:.2f}" if price != 0 else 0,
        'orderType': 0 if side == 'buy' else 1,  # 0 for buy, 1 for sell
        'orderMethod': 1,
        'stopPrice': f"{stop_loss:.2f}" if stop_loss else None,
        'takeProfitPrice': f"{take_profit:.2f}" if take_profit else None,
    }
    
    headers = get_headers(endpoint, nonce)  # Get the required headers for authentication
    url = BASE_URL + endpoint
    try:
        response = requests.post(url, headers=headers, json=params)
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error placing order: {e}")
        return None  # Return None in case of error
    except requests.exceptions.JSONDecodeError:
        logger.error(f"Error placing order: {response.status_code} - Response is not JSON.")
        logger.error(f"Raw response content: {response.text}")
        return None  # Return None if response is not JSON

    if response.status_code != 200:
        logger.error(f"Error placing order: {response.status_code} - {response_data}")
        return None  # Return None if the request fails with a non-200 status code
    
    logger.info(f"Order placed: {response_data}")  # Log success
    return response_data  # Return the API response data

def get_account_balance() -> list:
    """
    Fetches the user's account balance from the exchange.

    Returns:
        list: A list of balances for each currency in the account, or an empty list on failure.
    """
    endpoint = '/api/v1/users/balances'
    nonce = str(int(time.time() * 1000))  # Generate a unique nonce
    
    headers = get_headers(endpoint, nonce)  # Get the necessary headers
    url = BASE_URL + endpoint
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching account balance: {e}")
        return []  # Return an empty list in case of error
    
    logger.info("Account balance fetched successfully.")
    return response.json().get('data', [])  # Return the balance data or an empty list