import sys
import os
import yfinance as yf
import pandas as pd
from sklearn.metrics import accuracy_score

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from model import train_model, model_trade_signal
from indicators import bollinger_trade_signal, macd_trade_signal, rsi_trade_signal

def get_financial_data(symbol='BTC-USD', period='3mo', interval='1h'):
    """
    Fetches financial data from Yahoo Finance.
    Args:
        symbol (str): The financial symbol (default is 'BTC-USD').
        period (str): The period to retrieve data (default is '3 months').
        interval (str): The data interval (default is '1 hour').

    Returns:
        pd.DataFrame: The historical data with necessary columns.
    """
    data = yf.download(symbol, period=period, interval=interval)
    data.reset_index(inplace=True)
    data.rename(columns={'Close': 'close'}, inplace=True)
    return data[['Datetime', 'close']]

def run_ml_backtest(initial_balance_usd=50):
    """
    Performs backtesting using a machine learning model.

    Args:
        initial_balance_usd (int): Starting USD balance for backtesting.

    Returns:
        tuple: The balance history and trade log.
    """
    data = get_financial_data()
    balance_usd = initial_balance_usd
    btc_balance = 0
    balance_history = []
    trade_log = pd.DataFrame(columns=['Datetime', 'Action', 'Price', 'BTC_Balance', 'USD_Balance'])

    # Train the model
    model = train_model(data)

    for i in range(20, len(data)):
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
            print(f"Buying BTC at {close_price} USD, BTC balance: {btc_balance}, USD balance: {balance_usd} (ML)")
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
            print(f"Selling BTC at {close_price} USD, BTC balance: {btc_balance}, USD balance: {balance_usd} (ML)")

        total_balance = balance_usd + btc_balance * close_price
        balance_history.append(total_balance)

    return balance_history, trade_log


if __name__ == "__main__":
    # Running the machine learning backtest
    balance_history, trade_log = run_ml_backtest()

    # Print balance history and log
    print(balance_history)
    print(trade_log)