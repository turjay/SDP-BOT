import pytest
import yfinance as yf
import pandas as pd
from tqdm import tqdm
from indicators import (
    bollinger_trade_signal,
    macd_trade_signal,
    rsi_trade_signal,
    stochastic_trade_signal,
    atr_trade_signal
)
from main import train_model, model_trade_signal

def get_yahoo_data():
    """
    Yahoo Finance'ten BTC-USD verisini indirir ve gerekli sütunları seçer.
    Returns:
        pd.DataFrame: İçinde Datetime ve close sütunları bulunan veri seti.
    """
    symbol = 'BTC-USD'
    data = yf.download(symbol, period='3mo', interval='1h')
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

    for i in tqdm(range(20, len(data)), desc=f"Running {indicator_name} Backtest"):
        df = data.iloc[:i].copy()
        signal = indicator_signal(df)
        
        close_price = df['close'].iloc[-1]
        
        if signal == 'buy' and balance_usd > 0:
            btc_balance = balance_usd / close_price
            balance_usd = 0
        elif signal == 'sell' and btc_balance > 0:
            balance_usd = btc_balance * close_price
            btc_balance = 0
        
        total_balance = balance_usd + btc_balance * close_price
        balance_history.append(total_balance)

    return balance_history

def run_ml_backtest(initial_balance_usd=50):
    """
    Makine öğrenmesi modeli kullanarak geriye dönük test gerçekleştirir.
    """
    data = get_yahoo_data()
    balance_usd = initial_balance_usd
    btc_balance = 0
    balance_history = []
    
    model = train_model(data)

    for i in tqdm(range(20, len(data)), desc="Running ML Backtest"):
        df = data.iloc[:i].copy()
        signal = model_trade_signal(df, model)

        close_price = df['close'].iloc[-1]

        if signal == 'buy' and balance_usd > 0:
            btc_balance = balance_usd / close_price
            balance_usd = 0
        elif signal == 'sell' and btc_balance > 0:
            balance_usd = btc_balance * close_price
            btc_balance = 0

        total_balance = balance_usd + btc_balance * close_price
        balance_history.append(total_balance)

    return balance_history

@pytest.mark.parametrize("signal_function, name", [
    (bollinger_trade_signal, "Bollinger Bands"),
    (macd_trade_signal, "MACD"),
    (rsi_trade_signal, "RSI"),
    (stochastic_trade_signal, "Stochastic Oscillator"),
    (atr_trade_signal, "ATR"),
])

def test_backtest(signal_function, name):
    balance_history = run_backtest(signal_function, name)
    assert len(balance_history) > 0, f"Balance history is empty for {name}."
    assert balance_history[-1] > 0, f"Final balance is not greater than zero for {name}."

def test_ml_backtest():
    balance_history = run_ml_backtest()
    assert len(balance_history) > 0, "Balance history is empty for ML."
    assert balance_history[-1] > 0, "Final balance is not greater than zero for ML."
