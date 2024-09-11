"""
    To change the starting amount, you need to replace the values in 
    line 25, line 98 and line 155 with your starting amount.  
"""


import sys
import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import train_model, model_trade_signal
from indicators import atr_trade_signal, bollinger_trade_signal, macd_trade_signal, rsi_trade_signal, stochastic_trade_signal

def get_yahoo_data():
    symbol = 'BTC-USD'
    data = yf.download(symbol, period='5d', interval='1m')
    data.reset_index(inplace=True)
    data.rename(columns={'Close': 'close', 'Low': 'low', 'High': 'high', 'Volume': 'volume'}, inplace=True)
    return data[['Datetime', 'close', 'low', 'high', 'volume']]

def run_backtest(indicator_signal, indicator_name, initial_balance_usd=50, stop_loss_pct=0.05, take_profit_pct=0.1):
    data = get_yahoo_data()
    balance_usd = initial_balance_usd
    btc_balance = 0
    balance_history = []
    trade_log = pd.DataFrame(columns=['Datetime', 'Action', 'Price', 'BTC_Balance', 'USD_Balance'])
    entry_price = None

    for i in tqdm(range(20, len(data)), desc=f"Running {indicator_name} Backtest"):
        df = data.iloc[:i].copy()
        signal = indicator_signal(df)

        close_price = df['close'].iloc[-1]
        datetime = df['Datetime'].iloc[-1]

        if signal == 'buy' and balance_usd > 0:
            entry_price = close_price
            btc_balance = balance_usd / close_price
            balance_usd = 0
            new_row = pd.DataFrame({
                'Datetime': [datetime],
                'Action': ['buy'],
                'Price': [close_price],
                'BTC_Balance': [btc_balance],
                'USD_Balance': [balance_usd]
            })
            trade_log = pd.concat([trade_log, new_row], ignore_index=True)
            print(f"Buying BTC at {close_price} USD, BTC balance: {btc_balance}, USD balance: {balance_usd} (Indicator: {indicator_name})", flush=True)
        elif signal == 'sell' and btc_balance > 0:
            balance_usd = btc_balance * close_price
            btc_balance = 0
            new_row = pd.DataFrame({
                'Datetime': [datetime],
                'Action': ['sell'],
                'Price': [close_price],
                'BTC_Balance': [btc_balance],
                'USD_Balance': [balance_usd]
            })
            trade_log = pd.concat([trade_log, new_row], ignore_index=True)
            print(f"Selling BTC at {close_price} USD, BTC balance: {btc_balance}, USD balance: {balance_usd} (Indicator: {indicator_name})", flush=True)

        # Implement stop-loss and take-profit
        if btc_balance > 0 and entry_price is not None:
            if close_price <= entry_price * (1 - stop_loss_pct):
                balance_usd = btc_balance * close_price
                btc_balance = 0
                new_row = pd.DataFrame({
                    'Datetime': [datetime],
                    'Action': ['stop-loss'],
                    'Price': [close_price],
                    'BTC_Balance': [btc_balance],
                    'USD_Balance': [balance_usd]
                })
                trade_log = pd.concat([trade_log, new_row], ignore_index=True)
                print(f"Stop-loss triggered at {close_price} USD", flush=True)
            elif close_price >= entry_price * (1 + take_profit_pct):
                balance_usd = btc_balance * close_price
                btc_balance = 0
                new_row = pd.DataFrame({
                    'Datetime': [datetime],
                    'Action': ['take-profit'],
                    'Price': [close_price],
                    'BTC_Balance': [btc_balance],
                    'USD_Balance': [balance_usd]
                })
                trade_log = pd.concat([trade_log, new_row], ignore_index=True)
                print(f"Take-profit triggered at {close_price} USD", flush=True)

        total_balance = balance_usd + btc_balance * close_price
        balance_history.append(total_balance)

    return balance_history, trade_log

def run_ml_backtest(initial_balance_usd=50):
    data = get_yahoo_data()
    balance_usd = initial_balance_usd
    btc_balance = 0
    balance_history = []
    trade_log = pd.DataFrame(columns=['Datetime', 'Action', 'Price', 'BTC_Balance', 'USD_Balance'])

    model = train_model(data)

    for i in tqdm(range(20, len(data)), desc="Running ML Backtest"):
        df = data.iloc[:i].copy()
        signal = model_trade_signal(df, model)

        close_price = df['close'].iloc[-1]
        datetime = df['Datetime'].iloc[-1]

        if signal == 'buy' and balance_usd > 0:
            btc_balance = balance_usd / close_price
            balance_usd = 0
            new_row = pd.DataFrame({
                'Datetime': [datetime],
                'Action': ['buy'],
                'Price': [close_price],
                'BTC_Balance': [btc_balance],
                'USD_Balance': [balance_usd]
            })
            trade_log = pd.concat([trade_log, new_row], ignore_index=True)
            print(f"Buying BTC at {close_price} USD, BTC balance: {btc_balance}, USD balance: {balance_usd} (ML)", flush=True)
        elif signal == 'sell' and btc_balance > 0:
            balance_usd = btc_balance * close_price
            btc_balance = 0
            new_row = pd.DataFrame({
                'Datetime': [datetime],
                'Action': ['sell'],
                'Price': [close_price],
                'BTC_Balance': [btc_balance],
                'USD_Balance': [balance_usd]
            })
            trade_log = pd.concat([trade_log, new_row], ignore_index=True)
            print(f"Selling BTC at {close_price} USD, BTC balance: {btc_balance}, USD balance: {balance_usd} (ML)", flush=True)

        total_balance = balance_usd + btc_balance * close_price
        balance_history.append(total_balance)

    return balance_history, trade_log

# Run the backtests with different indicators
plt.figure(figsize=(12, 6))

balance_bollinger, trade_log_bollinger = run_backtest(bollinger_trade_signal, 'Bollinger Bands')
balance_macd, trade_log_macd = run_backtest(macd_trade_signal, 'MACD')
balance_rsi, trade_log_rsi = run_backtest(rsi_trade_signal, 'RSI')
balance_stochastic, trade_log_stochastic = run_backtest(stochastic_trade_signal, 'Stochastic')
balance_atr, trade_log_atr = run_backtest(atr_trade_signal, 'ATR')
balance_ml, trade_log_ml = run_ml_backtest()

# Calculate the total balance across strategies
initial_balance = 50
total_balance = [
    (balance_bollinger[i] + balance_macd[i] + balance_rsi[i] + balance_atr[i] + balance_stochastic[i] + balance_ml[i]) / 5
    for i in range(len(balance_bollinger))
]
total_balance = [initial_balance] + total_balance

data = get_yahoo_data()

plt.plot(data['Datetime'][20:len(balance_bollinger)+20], balance_bollinger, label='Balance Over Time (Bollinger Bands)')
plt.plot(data['Datetime'][20:], balance_macd, label='Balance Over Time (MACD)')
plt.plot(data['Datetime'][20:], balance_rsi, label='Balance Over Time (RSI)')
plt.plot(data['Datetime'][20:], balance_stochastic, label='Balance Over Time (Stochastic)')
plt.plot(data['Datetime'][20:], balance_atr, label='Balance Over Time (ATR)')
plt.plot(data['Datetime'][20:], balance_ml, label='Balance Over Time (ML)')
plt.plot(data['Datetime'][20:], total_balance, label='Total Balance', linestyle='--', linewidth=2, color='purple')

plt.xlabel('Date')
plt.ylabel('Balance (USD)')
plt.title('Backtesting Balance Over Time')
plt.legend()
plt.grid(True)
plt.show()