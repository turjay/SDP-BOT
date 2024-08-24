import sys
import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import train_model, model_trade_signal, SignalPool
from indicators import bollinger_trade_signal, macd_trade_signal, rsi_trade_signal

def get_yahoo_data():
    """
    Fetch historical BTC-USD data from Yahoo Finance.

    Yahoo Finance'den BTC-USD tarihsel verilerini çeker.
    
    Returns:
        pd.DataFrame: Datetime ve close fiyatlarını içeren bir DataFrame döner.
    """
    symbol = 'BTC-USD'
    data = yf.download(symbol, period='3mo', interval='1h')
    data.reset_index(inplace=True)
    data.rename(columns={'Close': 'close'}, inplace=True)
    return data[['Datetime', 'close']]

def run_backtest(indicator_signal, indicator_name):
    """
    Run backtesting on a given indicator signal.

    Verilen bir indikatör sinyali üzerinde geriye dönük test yapar.

    Args:
        indicator_signal (function): Test edilecek indikatör sinyali fonksiyonu.
        indicator_name (str): İndikatörün ismi.

    Returns:
        float: Final balance after backtesting.
    """
    data = get_yahoo_data()
    initial_balance_usd = 50
    balance_usd = initial_balance_usd
    btc_balance = 0
    balance_history = []
    trade_log = pd.DataFrame(columns=['Datetime', 'Action', 'Price', 'BTC_Balance', 'USD_Balance'])

    for i in range(20, len(data)):
        df = data.iloc[:i].copy()
        signal = indicator_signal(df)
        
        close_price = df['close'].iloc[-1]
        datetime = df['Datetime'].iloc[-1]
        
        # Alış sinyali
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
            progress_percent = (i - 19) / (len(data) - 20) * 100
            print(f"Buying BTC at {close_price} USD, BTC balance: {btc_balance} (Indicator: {indicator_name}, Progress: {progress_percent:.2f}%)")
        
        # Satış sinyali
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
            progress_percent = (i - 19) / (len(data) - 20) * 100
            print(f"Selling BTC at {close_price} USD, USD balance: {balance_usd} (Indicator: {indicator_name}, Progress: {progress_percent:.2f}%)")
        
        total_balance = balance_usd + btc_balance * close_price
        balance_history.append(total_balance)

    final_balance = balance_usd + btc_balance * data['close'].iloc[-1]
    print(f"Final balance using {indicator_name}: {final_balance} USD (Profit/Loss: {final_balance - initial_balance_usd} USD)")

    plt.plot(data['Datetime'][20:], balance_history, label=f'Balance Over Time ({indicator_name})')

    # Trade log analizleri
    trade_log['Datetime'] = pd.to_datetime(trade_log['Datetime'])
    trade_log.set_index('Datetime', inplace=True)

    return final_balance, trade_log

# Her bir indikatör için testleri çalıştır ve grafikte göster
plt.figure(figsize=(12, 6))

# Bollinger Bands
final_balance_bollinger, trade_log_bollinger = run_backtest(bollinger_trade_signal, 'Bollinger Bands')

# MACD
final_balance_macd, trade_log_macd = run_backtest(macd_trade_signal, 'MACD')

# RSI
final_balance_rsi, trade_log_rsi = run_backtest(rsi_trade_signal, 'RSI')

# Machine Learning Modeli için geriye dönük test
def run_ml_backtest():
    data = get_yahoo_data()
    initial_balance_usd = 50
    balance_usd = initial_balance_usd
    btc_balance = 0
    balance_history = []
    trade_log = pd.DataFrame(columns=['Datetime', 'Action', 'Price', 'BTC_Balance', 'USD_Balance'])

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
            progress_percent = (i - 19) / (len(data) - 20) * 100
            print(f"Buying BTC at {close_price} USD, BTC balance: {btc_balance} (Indicator: ML, Progress: {progress_percent:.2f}%)")

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
            progress_percent = (i - 19) / (len(data) - 20) * 100
            print(f"Selling BTC at {close_price} USD, USD balance: {balance_usd} (Indicator: ML, Progress: {progress_percent:.2f}%)")

        total_balance = balance_usd + btc_balance * close_price
        balance_history.append(total_balance)

    final_balance = balance_usd + btc_balance * data['close'].iloc[-1]
    print(f"Final balance using ML: {final_balance} USD (Profit/Loss: {final_balance - initial_balance_usd} USD)")

    plt.plot(
        data['Datetime'][20:], balance_history, label='Balance Over Time (ML)'
    )

    return final_balance, trade_log

# Machine Learning ile backtesting
final_balance_ml, trade_log_ml = run_ml_backtest()

plt.xlabel('Date')
plt.ylabel('Balance (USD)')
plt.title('Backtesting Balance Over Time')
plt.legend()
plt.grid(True)
plt.show()