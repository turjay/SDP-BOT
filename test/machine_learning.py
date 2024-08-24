import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from main import SignalPool, model_trade_signal
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

# Özellik mühendisliği ve etiketleme
# Feature engineering and labeling
data['bollinger_signal'] = bollinger_trade_signal(data)
data['macd_signal'] = macd_trade_signal(data)
data['rsi_signal'] = rsi_trade_signal(data)

# Etiketleme için basit bir strateji: Kapanış fiyatının bir saat sonra artıp artmadığını belirlemek
data['target'] = (data['close'].shift(-1) > data['close']).astype(int)

# Özellikler ve etiketlerin ayrılması
# Separating features and labels
features = ['bollinger_signal', 'macd_signal', 'rsi_signal']
X = data[features]
y = data['target']

# Eğitim ve test veri setlerine ayırma
# Splitting into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model mimarisi ve eğitim
# Model architecture and training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Model değerlendirmesi
# Model evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

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
