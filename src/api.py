import time
import hmac
import hashlib
import base64
import requests
import pandas as pd
from config import API_KEY, api_secret, GRAPH_API_URL, BASE_URL, logger
from utils import format_quantity

<<<<<<< HEAD
def get_headers(endpoint: str, nonce: str) -> dict:
    """
    Generates the necessary headers for API calls.

=======
def get_headers(endpoint, nonce):
    """
    Generates the necessary headers for API calls.

    API çağrıları için gerekli başlıkları oluşturur.

>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
    Args:
        endpoint (str): The API endpoint being accessed.
        nonce (str): A unique number to ensure the request is unique.

    Returns:
        dict: A dictionary containing the headers for the API request.
    """
<<<<<<< HEAD
    # Create the signature for authentication using HMAC and the API secret
    data = f"{API_KEY}{nonce}".encode('utf-8')
    signature = hmac.new(api_secret, data, hashlib.sha256).digest()
    signature = base64.b64encode(signature).decode('utf-8')

    # Return the necessary headers for authentication
=======
    # Concatenate API_KEY and nonce, and then encode it
    # API_KEY ve nonce değerlerini birleştirip, sonrasında encode eder
    data = f"{API_KEY}{nonce}".encode('utf-8')
    
    # Create HMAC signature using the api_secret and the encoded data
    # api_secret ve encode edilmiş veriyi kullanarak HMAC imzası oluşturur
    signature = hmac.new(api_secret, data, hashlib.sha256).digest()
    
    # Encode the signature to Base64
    # İmzayı Base64 formatında encode eder
    signature = base64.b64encode(signature).decode('utf-8')
    
    # Return the headers required for the API request
    # API isteği için gerekli olan başlıkları döndürür
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
    return {
        'X-PCK': API_KEY,
        'X-Stamp': nonce,
        'X-Signature': signature,
        'Content-Type': 'application/json',
    }

<<<<<<< HEAD
def get_ohlcv(symbol: str, limit: int = 100) -> pd.DataFrame:
    """
    Fetches OHLCV (Open, High, Low, Close, Volume) data from the API.

=======
def get_ohlcv(symbol, limit=100):
    """
    Fetches OHLCV (Open, High, Low, Close, Volume) data from the API.

    API'den OHLCV (Açılış, Yüksek, Düşük, Kapanış, Hacim) verilerini çeker.

>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
    Args:
        symbol (str): The trading pair symbol (e.g., 'BTCUSD').
        limit (int): The number of data points to return (default is 100).

    Returns:
<<<<<<< HEAD
        pd.DataFrame: A DataFrame containing the OHLCV data, or an empty DataFrame on failure.
=======
        pd.DataFrame: A DataFrame containing the OHLCV data.
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
    """
    endpoint = f'/v1/ohlcs?pair={symbol}'
    url = GRAPH_API_URL + endpoint
    try:
<<<<<<< HEAD
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

=======
        # Send a GET request to the API
        # API'ye GET isteği gönderir
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Log an error message if the request fails
        # İstek başarısız olursa hata mesajı kaydeder
        logger.error(f"Error fetching OHLCV data: {e}")
        return pd.DataFrame()
    
    data = response.json()
    if not data:
        # Log an error if no data is returned
        # Veri döndürülmezse hata kaydeder
        logger.error("No data received from API")
        return pd.DataFrame()
    
    # Convert the data into a pandas DataFrame
    # Veriyi pandas DataFrame formatına dönüştürür
    df = pd.DataFrame(data)
    
    # Convert the 'time' column to datetime and set it as the index
    # 'time' sütununu datetime formatına dönüştürür ve indeks olarak ayarlar
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    
    # Return the last 'limit' rows of the DataFrame
    # DataFrame'in son 'limit' satırını döndürür
    return df.tail(limit)

def place_order(symbol, side, quantity, price=0, stop_loss=None, take_profit=None):
    """
    Places an order (buy/sell) on the exchange.

    Borsada bir alım/satım emri yerleştirir.

>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
    Args:
        symbol (str): The trading pair symbol (e.g., 'BTCUSD').
        side (str): 'buy' for a buy order, 'sell' for a sell order.
        quantity (float): The amount of the asset to trade.
<<<<<<< HEAD
        price (float, optional): The price at which to place the order (default is 0 for market orders).
=======
        price (float): The price at which to place the order (default is 0 for market orders).
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
        stop_loss (float, optional): The price at which to trigger a stop loss.
        take_profit (float, optional): The price at which to trigger a take profit.

    Returns:
        dict or None: The response from the API if successful, otherwise None.
    """
    endpoint = '/api/v1/order'
<<<<<<< HEAD
    nonce = str(int(time.time() * 1000))  # Generate a unique nonce
    formatted_quantity = format_quantity(quantity, precision=8)  # Ensure correct precision for quantity

    # Construct the order parameters
=======
    nonce = str(int(time.time() * 1000))
    
    # Format the quantity with a precision of 8 decimal places
    # Miktarı 8 ondalık hassasiyetle formatlar
    formatted_quantity = format_quantity(quantity, precision=8)
    
    # Construct the parameters for the API request
    # API isteği için parametreleri oluşturur
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
    params = {
        'pairSymbol': symbol,
        'quantity': f"{formatted_quantity:.8f}",
        'price': f"{price:.2f}" if price != 0 else 0,
<<<<<<< HEAD
        'orderType': 0 if side == 'buy' else 1,  # 0 for buy, 1 for sell
=======
        'orderType': 0 if side == 'buy' else 1,
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
        'orderMethod': 1,
        'stopPrice': f"{stop_loss:.2f}" if stop_loss else None,
        'takeProfitPrice': f"{take_profit:.2f}" if take_profit else None,
    }
    
<<<<<<< HEAD
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
=======
    # Generate the necessary headers for the API request
    # API isteği için gerekli başlıkları oluşturur
    headers = get_headers(endpoint, nonce)
    url = BASE_URL + endpoint
    try:
        # Send a POST request to the API with the parameters
        # Parametrelerle birlikte API'ye POST isteği gönderir
        response = requests.post(url, headers=headers, json=params)
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        # Log an error message if the request fails
        # İstek başarısız olursa hata mesajı kaydeder
        logger.error(f"Error placing order: {e}")
        return None
    except requests.exceptions.JSONDecodeError:
        # Log an error if the response is not valid JSON
        # Yanıt geçerli bir JSON değilse hata kaydeder
        logger.error(f"Error placing order: {response.status_code} - Response is not JSON.")
        logger.error(f"Raw response content: {response.text}")
        return None
    
    if response.status_code != 200:
        # Log an error if the response status code is not 200 OK
        # Yanıt durum kodu 200 değilse hata kaydeder
        logger.error(f"Error placing order: {response.status_code} - {response_data}")
        return None
    
    logger.info(f"Order placed: {response_data}")
    return response_data

def get_account_balance():
    """
    Fetches the user's account balance from the exchange.

    Kullanıcının borsadaki hesap bakiyesini çeker.

    Returns:
        list: A list of balances for each currency in the account.
    """
    endpoint = '/api/v1/users/balances'
    nonce = str(int(time.time() * 1000))
    
    # Generate the necessary headers for the API request
    # API isteği için gerekli başlıkları oluşturur
    headers = get_headers(endpoint, nonce)
    url = BASE_URL + endpoint
    try:
        # Send a GET request to the API
        # API'ye GET isteği gönderir
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Log an error message if the request fails
        # İstek başarısız olursa hata mesajı kaydeder
        logger.error(f"Error fetching account balance: {e}")
        return []
    
    logger.info("Account balance fetched successfully.")
    return response.json().get('data', [])
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
