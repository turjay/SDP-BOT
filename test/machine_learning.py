import yfinance as yf
import pandas as pd
from main import train_model, model_trade_signal, SignalPool
from indicators import bollinger_trade_signal, macd_trade_signal, rsi_trade_signal

# Bitcoin'in son 3 aydaki fiyat verilerini indiriyoruz
# Downloading Bitcoin's price data for the last 3 months
symbol = 'BTC-USD'
data = yf.download(symbol, period='3mo', interval='1h')  # Son 3 ay, 1 saatlik veriler
# Last 3 months, hourly data

# Veriyi hazırlıyoruz
# Preparing the data
data.reset_index(inplace=True)  # Zaman sütununu düzenlemek için
# To adjust the time column
data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)

# Modeli eğitiyoruz
# Training the model
model = train_model(data)

# Sinyal havuzunu oluşturuyoruz
# Creating the signal pool
signal_pool = SignalPool()

# Geriye dönük test (Backtesting) için her bir saatlik veri üzerinde botu çalıştırıyoruz
# Running the bot on each hourly data for backtesting
for i in range(20, len(data)):  # İlk 20 veri noktası model eğitimi için kullanıldı
    # The first 20 data points were used for model training
    df = data.iloc[:i].copy()  # Her adımda yeni veriyi ekleyerek ilerliyoruz ve copy() kullanarak kopya alıyoruz
    # Moving forward by adding new data at each step and using copy() to create a copy
    # Farklı stratejilerden sinyalleri ekle
    # Adding signals from different strategies
    signal_pool.add_signal('bollinger', bollinger_trade_signal(df), weight=1)
    signal_pool.add_signal('macd', macd_trade_signal(df), weight=1)
    signal_pool.add_signal('rsi', rsi_trade_signal(df), weight=1)
    signal_pool.add_signal('ml', model_trade_signal(df, model), weight=2)
    
    # Birleşik sinyali al ve işlem kararını loglayın
    # Get the combined signal and log the trading decision
    combined_signal = signal_pool.get_combined_signal()
    print(f"Date: {data['Datetime'].iloc[i]}, Combined Signal: {combined_signal}")
    
    # Sinyal havuzunu temizle
    # Reset the signal pool
    signal_pool.reset()
