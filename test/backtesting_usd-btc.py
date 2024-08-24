import sys
import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm  # İlerleme çubuğu için / For progress bar

# src dizinini Python yolu olarak ekle
# Add src path as Python pat
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import train_model, model_trade_signal, SignalPool
from indicators import bollinger_trade_signal, macd_trade_signal, rsi_trade_signal

def get_yahoo_data():
    """
    Yahoo Finance'ten BTC/USD verilerini çeker.
    Fetches BTC/USD data from Yahoo Finance.

    Returns:
        pd.DataFrame: BTC/USD verilerini içeren DataFrame.
        pd.DataFrame: DataFrame containing BTC/USD data.
    """
    symbol = 'BTC-USD'
    data = yf.download(symbol, period='3mo', interval='1h')  # Son 3 ay, 1 saatlik veriler / Last 3 months, 1-hour intervals
    data.reset_index(inplace=True)
    data.rename(columns={'Close': 'close'}, inplace=True)
    return data[['Datetime', 'close']]

# Veriyi oluşturma
# Creating the data
data = get_yahoo_data()

# Modeli eğitiyoruz
# Training the model
model = train_model(data)

# Sinyal havuzunu oluşturuyoruz
# Creating the signal pool
signal_pool = SignalPool()

# Başlangıç sermayesi ve BTC miktarını belirleyin
# Setting initial balance and BTC amount
initial_balance_usd = 50  # Başlangıç USD bakiyesi / Initial USD balance
balance_usd = initial_balance_usd
btc_balance = 0  # Başlangıçta BTC bakiyesi yok / Initial BTC balance is zero

# Bakiye takibi için liste
# List for tracking balance
balance_history = []

# Geriye dönük test (Backtesting) için her bir saatlik veri üzerinde botu çalıştırıyoruz
# Running the bot on each hourly data for backtesting
for i in range(20, len(data)):
    df = data.iloc[:i].copy()
    
    # Sinyalleri ekleme
    # Adding signals
    signal_pool.add_signal('bollinger', bollinger_trade_signal(df), weight=1)
    signal_pool.add_signal('macd', macd_trade_signal(df), weight=1)
    signal_pool.add_signal('rsi', rsi_trade_signal(df), weight=1)
    signal_pool.add_signal('ml', model_trade_signal(df, model), weight=2)
    
    # Kombine sinyali al
    # Getting the combined signal
    combined_signal = signal_pool.get_combined_signal()
    
    close_price = df['close'].iloc[-1]
    
    # Alım sinyali varsa ve USD bakiyesi varsa BTC al
    # If the signal is 'buy' and there is USD balance, buy BTC
    if combined_signal == 'buy' and balance_usd > 0:
        btc_balance = balance_usd / close_price
        balance_usd = 0
        buy_price = close_price  # Alım fiyatını kaydediyoruz / Recording the buy price
        print(f"Buying BTC at {close_price} USD, BTC balance: {btc_balance}")
    
    # Satış sinyali varsa ve BTC bakiyesi varsa BTC sat
    # If the signal is 'sell' and there is BTC balance, sell BTC
    elif combined_signal == 'sell' and btc_balance > 0:
        balance_usd = btc_balance * close_price
        btc_balance = 0
        print(f"Selling BTC at {close_price} USD, USD balance: {balance_usd}")
    
    # Toplam bakiyeyi hesapla
    # Calculate the total balance
    total_balance = balance_usd + btc_balance * close_price
    balance_history.append(total_balance)
    signal_pool.reset()

# Sonuçları yazdır
# Print the results
final_balance = balance_usd + btc_balance * data['close'].iloc[-1]
print(f"Initial balance: {initial_balance_usd} USD")
print(f"Final balance: {final_balance} USD")
print(f"Profit/Loss: {final_balance - initial_balance_usd} USD")

# Bakiye değişimini görselleştir
# Visualize balance changes
plt.figure(figsize=(12, 6))
plt.plot(data['Datetime'][20:], balance_history, label='Balance Over Time')
plt.xlabel('Date')
plt.ylabel('Balance (USD)')
plt.title('Backtesting Balance Over Time (USD)')
plt.legend()
plt.grid(True)
plt.show()
