import yfinance as yf
import pandas as pd
from main import train_model, model_trade_signal, SignalPool
from indicators import bollinger_trade_signal, macd_trade_signal, rsi_trade_signal

# Bitcoin'in son 1 ayki fiyat verilerini indiriyoruz
symbol = 'BTC-USD'
data = yf.download(symbol, period='3mo', interval='1h')  # Son 1 ay, 1 saatlik veriler

# Veriyi hazırlıyoruz
data.reset_index(inplace=True)  # Zaman sütununu düzenlemek için
data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)

# Modeli eğitiyoruz
model = train_model(data)

# Sinyal havuzunu oluşturuyoruz
signal_pool = SignalPool()

# Geriye dönük test (Backtesting) için her bir saatlik veri üzerinde botu çalıştırıyoruz
for i in range(20, len(data)):  # İlk 20 veri noktası model eğitimi için kullanıldı
    df = data.iloc[:i].copy()  # Her adımda yeni veriyi ekleyerek ilerliyoruz ve copy() kullanarak kopya alıyoruz
    
    # Farklı stratejilerden sinyalleri ekle
    signal_pool.add_signal('bollinger', bollinger_trade_signal(df), weight=1)
    signal_pool.add_signal('macd', macd_trade_signal(df), weight=1)
    signal_pool.add_signal('rsi', rsi_trade_signal(df), weight=1)
    signal_pool.add_signal('ml', model_trade_signal(df, model), weight=2)
    
    # Birleşik sinyali al ve işlem kararını loglayın
    combined_signal = signal_pool.get_combined_signal()
    print(f"Date: {data['Datetime'].iloc[i]}, Combined Signal: {combined_signal}")
    
    # Sinyal havuzunu temizle
    signal_pool.reset()