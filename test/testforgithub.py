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
    Yahoo Finance'ten BTC-USD verisini indirir ve gerekli sütunları seçer.
    Returns:
        pd.DataFrame: İçinde Datetime ve close sütunları bulunan veri seti.
    """
    symbol = 'BTC-USD'
    data = yf.download(symbol, period='1mo', interval='1h')
    data.reset_index(inplace=True)
    data.rename(columns={'Close': 'close'}, inplace=True)
    return data[['Datetime', 'close']]

def run_backtest(indicator_signal, indicator_name, initial_balance_usd=50):
    """
    Belirli bir indikatör sinyali kullanarak geriye dönük test gerçekleştirir.
    """
    data = get_yahoo_data()
    balance_usd = initial_balance_usd
    btc_balance = 0
    balance_history = []
    trade_log = pd.DataFrame(columns=['Datetime', 'Action', 'Price', 'BTC_Balance', 'USD_Balance'])

    for i in tqdm(range(20, len(data)), desc=f"Running {indicator_name} Backtest"):
        df = data.iloc[:i].copy()
        signal = indicator_signal(df)
        
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
        
        total_balance = balance_usd + btc_balance * close_price
        balance_history.append(total_balance)

    return balance_history, trade_log

def run_ml_backtest(initial_balance_usd=50):
    """
    Makine öğrenmesi modeli kullanarak geriye dönük test gerçekleştirir.
    """
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

        total_balance = balance_usd + btc_balance * close_price
        balance_history.append(total_balance)

    return balance_history, trade_log

# Test fonksiyonları
def test_bollinger_backtest():
    balance_history, _ = run_backtest(bollinger_trade_signal, 'Bollinger Bands')
    assert len(balance_history) > 0
    assert balance_history[-1] > 0

def test_macd_backtest():
    balance_history, _ = run_backtest(macd_trade_signal, 'MACD')
    assert len(balance_history) > 0
    assert balance_history[-1] > 0

def test_rsi_backtest():
    balance_history, _ = run_backtest(rsi_trade_signal, 'RSI')
    assert len(balance_history) > 0
    assert balance_history[-1] > 0

def test_ml_backtest():
    balance_history, _ = run_ml_backtest()
    assert len(balance_history) > 0
    assert balance_history[-1] > 0

# Eğer direkt olarak bu dosya çalıştırılıyorsa, grafik çizimi yapılır
if __name__ == "__main__":
    plt.figure(figsize=(12, 6))

    balance_bollinger, trade_log_bollinger = run_backtest(bollinger_trade_signal, 'Bollinger Bands')
    balance_macd, trade_log_macd = run_backtest(macd_trade_signal, 'MACD')
    balance_rsi, trade_log_rsi = run_backtest(rsi_trade_signal, 'RSI')
    balance_ml, trade_log_ml = run_ml_backtest()

    # Toplam bakiyeyi hesapla
    total_balance = [
        (balance_bollinger[i] + balance_macd[i] + balance_rsi[i] + balance_ml[i]) / 4
        for i in range(len(balance_bollinger))
    ]

    data = get_yahoo_data()

    plt.plot(data['Datetime'][20:], balance_bollinger, label='Balance Over Time (Bollinger Bands)')
    plt.plot(data['Datetime'][20:], balance_macd, label='Balance Over Time (MACD)')
    plt.plot(data['Datetime'][20:], balance_rsi, label='Balance Over Time (RSI)')
    plt.plot(data['Datetime'][20:], balance_ml, label='Balance Over Time (ML)')
    plt.plot(data['Datetime'][20:], total_balance, label='Total Balance', linestyle='--', linewidth=2, color='purple')

    plt.xlabel('Date')
    plt.ylabel('Balance (USD)')
    plt.title('Backtesting Balance Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()