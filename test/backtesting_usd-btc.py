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
    symbol = 'BTC-USD'
    data = yf.download(symbol, period='3mo', interval='1h')
    data.reset_index(inplace=True)
    data.rename(columns={'Close': 'close'}, inplace=True)
    return data[['Datetime', 'close']]

def run_backtest(indicator_signal, indicator_name):
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
        if signal == 'buy' and balance_usd > 0:
            btc_balance = balance_usd / close_price
            balance_usd = 0
            trade_log = trade_log.append({
                'Datetime': datetime,
                'Action': 'buy',
                'Price': close_price,
                'BTC_Balance': btc_balance,
                'USD_Balance': balance_usd
            }, ignore_index=True)
            print(f"Buying BTC at {close_price} USD, BTC balance: {btc_balance} (Indicator: {indicator_name})")
        elif signal == 'sell' and btc_balance > 0:
            balance_usd = btc_balance * close_price
            btc_balance = 0
            trade_log = trade_log.append({
                'Datetime': datetime,
                'Action': 'sell',
                'Price': close_price,
                'BTC_Balance': btc_balance,
                'USD_Balance': balance_usd
            }, ignore_index=True)
            print(f"Selling BTC at {close_price} USD, USD balance: {balance_usd} (Indicator: {indicator_name})")
        
        total_balance = balance_usd + btc_balance * close_price
        balance_history.append(total_balance)

    final_balance = balance_usd + btc_balance * data['close'].iloc[-1]
    print(f"Final balance using {indicator_name}: {final_balance} USD (Profit/Loss: {final_balance - initial_balance_usd} USD)")

    plt.figure(figsize=(12, 6))
    plt.plot(data['Datetime'][20:], balance_history, label=f'Balance Over Time ({indicator_name})')
    plt.xlabel('Date')
    plt.ylabel('Balance (USD)')
    plt.title(f'Backtesting Balance Over Time ({indicator_name})')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Trade log analizleri
    trade_log['Datetime'] = pd.to_datetime(trade_log['Datetime'])
    trade_log.set_index('Datetime', inplace=True)

    # Günlük ve aylık işlem yüzdelerini hesapla
    daily_trades = trade_log.resample('D').size()
    monthly_trades = trade_log.resample('M').size()

    # Günlük işlem sayısını grafikte göster
    plt.figure(figsize=(12, 6))
    daily_trades.plot(kind='bar', color='blue', alpha=0.7)
    plt.xlabel('Date')
    plt.ylabel('Number of Trades')
    plt.title(f'Daily Number of Trades ({indicator_name})')
    plt.grid(True)
    plt.show()

    # Aylık işlem sayısını grafikte göster
    plt.figure(figsize=(12, 6))
    monthly_trades.plot(kind='bar', color='green', alpha=0.7)
    plt.xlabel('Month')
    plt.ylabel('Number of Trades')
    plt.title(f'Monthly Number of Trades ({indicator_name})')
    plt.grid(True)
    plt.show()

    return final_balance

# Her bir indikatör için testleri çalıştır
run_backtest(bollinger_trade_signal, 'Bollinger Bands')
run_backtest(macd_trade_signal, 'MACD')
run_backtest(rsi_trade_signal, 'RSI')