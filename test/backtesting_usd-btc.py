import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from main import train_model, model_trade_signal, SignalPool
from indicators import bollinger_trade_signal, macd_trade_signal, rsi_trade_signal
from tqdm import tqdm  # İlerleme çubuğu için

# Yahoo Finance'ten BTC/USD verisini çekme fonksiyonu
def get_yahoo_data():
    symbol = 'BTC-USD'
    data = yf.download(symbol, period='3mo', interval='1h')  # Son 3 ay, 1 saatlik veriler
    data.reset_index(inplace=True)
    data.rename(columns={'Close': 'close'}, inplace=True)
    return data[['Datetime', 'close']]

# Veriyi oluşturma
data = get_yahoo_data()

# Modeli eğitiyoruz
model = train_model(data)

# Sinyal havuzunu oluşturuyoruz
signal_pool = SignalPool()

# Başlangıç sermayesi ve BTC miktarını belirleyin
initial_balance_usd = 50  # Başlangıç USD bakiyesi
balance_usd = initial_balance_usd
btc_balance = 0  # Başlangıçta BTC bakiyesi yok

# Bakiye takibi için liste
balance_history = []

# Geriye dönük test (Backtesting) için her bir saatlik veri üzerinde botu çalıştırıyoruz
for i in range(20, len(data)):
    df = data.iloc[:i].copy()
    
    signal_pool.add_signal('bollinger', bollinger_trade_signal(df), weight=1)
    signal_pool.add_signal('macd', macd_trade_signal(df), weight=1)
    signal_pool.add_signal('rsi', rsi_trade_signal(df), weight=1)
    signal_pool.add_signal('ml', model_trade_signal(df, model), weight=2)
    
    combined_signal = signal_pool.get_combined_signal()
    
    close_price = df['close'].iloc[-1]
    if combined_signal == 'buy' and balance_usd > 0:
        btc_balance = balance_usd / close_price
        balance_usd = 0
        buy_price = close_price  # Alım fiyatını kaydediyoruz
        print(f"Buying BTC at {close_price} USD, BTC balance: {btc_balance}")
    elif combined_signal == 'sell' and btc_balance > 0:
        balance_usd = btc_balance * close_price
        btc_balance = 0
        print(f"Selling BTC at {close_price} USD, USD balance: {balance_usd}")
    
    total_balance = balance_usd + btc_balance * close_price
    balance_history.append(total_balance)
    signal_pool.reset()

final_balance = balance_usd + btc_balance * data['close'].iloc[-1]
print(f"Initial balance: {initial_balance_usd} USD")
print(f"Final balance: {final_balance} USD")
print(f"Profit/Loss: {final_balance - initial_balance_usd} USD")

plt.figure(figsize=(12, 6))
plt.plot(data['Datetime'][20:], balance_history, label='Balance Over Time')
plt.xlabel('Date')
plt.ylabel('Balance (USD)')
plt.title('Backtesting Balance Over Time (USD)')
plt.legend()
plt.grid(True)
plt.show()