import sys
import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import train_model, model_trade_signal, SignalPool
from indicators import bollinger_trade_signal, macd_trade_signal, rsi_trade_signal, combined_bollinger_rsi_signal

def get_binance_data(symbol='BTC/TRY', timeframe='1m', since=None, limit=1000):
    """
    Fetches historical data from Binance for the specified symbol.

    Args:
        symbol (str): The trading pair symbol (default is 'BTC/TRY').
        timeframe (str): The interval between data points (default is '5m').
        since (int): Timestamp in ms to start fetching data from.
        limit (int): Number of data points to retrieve (default is 1000).

    Returns:
        pd.DataFrame: A DataFrame containing the historical data.
    """
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
    data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    data['Datetime'] = pd.to_datetime(data['timestamp'], unit='ms')
    return data[['Datetime', 'close']]

def run_backtest(indicator_signal, indicator_name, initial_balance_try=1000, stop_loss_pct=0.05, take_profit_pct=0.1):
    data = get_binance_data()
    balance_try = initial_balance_try
    btc_balance = 0
    balance_history = []
    trade_log = pd.DataFrame(columns=['Datetime', 'Action', 'Price', 'BTC_Balance', 'TRY_Balance'])
    entry_price = None

    for i in tqdm(range(20, len(data)), desc=f"Running {indicator_name} Backtest"):
        df = data.iloc[:i].copy()
        signal = indicator_signal(df)

        close_price = df['close'].iloc[-1]
        datetime = df['Datetime'].iloc[-1]

        if signal == 'buy' and balance_try > 0:
            entry_price = close_price
            btc_balance = balance_try / close_price  # TRY to BTC conversion
            balance_try = 0
            new_row = pd.DataFrame({
                'Datetime': [datetime],
                'Action': ['buy'],
                'Price': [close_price],
                'BTC_Balance': [btc_balance],
                'TRY_Balance': [balance_try]
            })
            trade_log = pd.concat([trade_log, new_row], ignore_index=True)
            print(f"Buying BTC at {close_price} TRY/BTC, BTC balance: {btc_balance}, TRY balance: {balance_try} (Indicator: {indicator_name})", flush=True)
        elif signal == 'sell' and btc_balance > 0:
            balance_try = btc_balance * close_price  # BTC to TRY conversion
            btc_balance = 0
            new_row = pd.DataFrame({
                'Datetime': [datetime],
                'Action': ['sell'],
                'Price': [close_price],
                'BTC_Balance': [btc_balance],
                'TRY_Balance': [balance_try]
            })
            trade_log = pd.concat([trade_log, new_row], ignore_index=True)
            print(f"Selling BTC at {close_price} TRY/BTC, BTC balance: {btc_balance}, TRY balance: {balance_try} (Indicator: {indicator_name})", flush=True)

        # Implement stop-loss and take-profit
        if btc_balance > 0 and entry_price is not None:
            if close_price <= entry_price * (1 - stop_loss_pct):
                balance_try = btc_balance * close_price
                btc_balance = 0
                new_row = pd.DataFrame({
                    'Datetime': [datetime],
                    'Action': ['stop-loss'],
                    'Price': [close_price],
                    'BTC_Balance': [btc_balance],
                    'TRY_Balance': [balance_try]
                })
                trade_log = pd.concat([trade_log, new_row], ignore_index=True)
                print(f"Stop-loss triggered at {close_price} TRY/BTC", flush=True)
            elif close_price >= entry_price * (1 + take_profit_pct):
                balance_try = btc_balance * close_price
                btc_balance = 0
                new_row = pd.DataFrame({
                    'Datetime': [datetime],
                    'Action': ['take-profit'],
                    'Price': [close_price],
                    'BTC_Balance': [btc_balance],
                    'TRY_Balance': [balance_try]
                })
                trade_log = pd.concat([trade_log, new_row], ignore_index=True)
                print(f"Take-profit triggered at {close_price} TRY/BTC", flush=True)

        total_balance = balance_try + (btc_balance * close_price)
        balance_history.append(total_balance)

    return balance_history, trade_log

def run_ml_backtest(initial_balance_try=1000):
    data = get_binance_data()
    balance_try = initial_balance_try
    btc_balance = 0
    balance_history = []
    trade_log = pd.DataFrame(columns=['Datetime', 'Action', 'Price', 'BTC_Balance', 'TRY_Balance'])

    model = train_model(data)

    for i in tqdm(range(20, len(data)), desc="Running ML Backtest"):
        df = data.iloc[:i].copy()
        signal = model_trade_signal(df, model)

        close_price = df['close'].iloc[-1]
        datetime = df['Datetime'].iloc[-1]

        if signal == 'buy' and balance_try > 0:
            btc_balance = balance_try / close_price
            balance_try = 0
            new_row = pd.DataFrame({
                'Datetime': [datetime],
                'Action': ['buy'],
                'Price': [close_price],
                'BTC_Balance': [btc_balance],
                'TRY_Balance': [balance_try]
            })
            trade_log = pd.concat([trade_log, new_row], ignore_index=True)
            print(f"Buying BTC at {close_price} TRY/BTC, BTC balance: {btc_balance}, TRY balance: {balance_try} (ML)", flush=True)
        elif signal == 'sell' and btc_balance > 0:
            balance_try = btc_balance * close_price
            btc_balance = 0
            new_row = pd.DataFrame({
                'Datetime': [datetime],
                'Action': ['sell'],
                'Price': [close_price],
                'BTC_Balance': [btc_balance],
                'TRY_Balance': [balance_try]
            })
            trade_log = pd.concat([trade_log, new_row], ignore_index=True)
            print(f"Selling BTC at {close_price} TRY/BTC, BTC balance: {btc_balance}, TRY balance: {balance_try} (ML)", flush=True)

        total_balance = balance_try + (btc_balance * close_price)
        balance_history.append(total_balance)

    return balance_history, trade_log

# Run the backtests with different indicators
plt.figure(figsize=(12, 6))

balance_bollinger, trade_log_bollinger = run_backtest(bollinger_trade_signal, 'Bollinger Bands')
balance_macd, trade_log_macd = run_backtest(macd_trade_signal, 'MACD')
balance_rsi, trade_log_rsi = run_backtest(rsi_trade_signal, 'RSI')
balance_combined, trade_log_combined = run_backtest(combined_bollinger_rsi_signal, 'Combined Bollinger & RSI')
balance_ml, trade_log_ml = run_ml_backtest()

# Calculate the total balance across strategies
total_balance = [
    (balance_bollinger[i] + balance_macd[i] + balance_rsi[i] + balance_combined[i] + balance_ml[i]) / 5
    for i in range(len(balance_bollinger))
]

data = get_binance_data()

plt.plot(data['Datetime'][20:], balance_bollinger, label='Balance Over Time (Bollinger Bands)')
plt.plot(data['Datetime'][20:], balance_macd, label='Balance Over Time (MACD)')
plt.plot(data['Datetime'][20:], balance_rsi, label='Balance Over Time (RSI)')
plt.plot(data['Datetime'][20:], balance_combined, label='Balance Over Time (Combined Bollinger & RSI)')
plt.plot(data['Datetime'][20:], balance_ml, label='Balance Over Time (ML)')
plt.plot(data['Datetime'][20:], total_balance, label='Total Balance', linestyle='--', linewidth=2, color='purple')

plt.xlabel('Date')
plt.ylabel('Balance (TRY)')
plt.title('Backtesting Balance Over Time (TRY/BTC)')
plt.legend()
plt.grid(True)
plt.show()