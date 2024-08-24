# test_trading_bot.py
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from main import SignalPool, model_trade_signal
from indicators import bollinger_trade_signal, macd_trade_signal, rsi_trade_signal

def test_trading_bot():
    # Bitcoin'in son 3 aydaki fiyat verilerini indiriyoruz
    symbol = 'BTC-USD'
    data = yf.download(symbol, period='3mo', interval='1h')  # Son 3 ay, 1 saatlik veriler

    # Veriyi hazırlıyoruz
    data.reset_index(inplace=True)
    data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)

    # Özellik mühendisliği ve etiketleme
    data['bollinger_signal'] = bollinger_trade_signal(data)
    data['macd_signal'] = macd_trade_signal(data)
    data['rsi_signal'] = rsi_trade_signal(data)

    # Etiketleme
    data['target'] = (data['close'].shift(-1) > data['close']).astype(int)

    # Özellikler ve etiketlerin ayrılması
    features = ['bollinger_signal', 'macd_signal', 'rsi_signal']
    X = data[features]
    y = data['target']

    # Eğitim ve test veri setlerine ayırma
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model mimarisi ve eğitim
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Model değerlendirmesi
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Basit bir doğrulama
    assert accuracy > 0.5, "Model accuracy is below the threshold."

    # Sinyal havuzunu oluşturuyoruz
    signal_pool = SignalPool()

    # Geriye dönük test (Backtesting) için her bir saatlik veri üzerinde botu çalıştırıyoruz
    for i in range(20, len(data)):  # İlk 20 veri noktası model eğitimi için kullanıldı
        df = data.iloc[:i].copy()

        # Farklı stratejilerden sinyalleri ekle
        signal_pool.add_signal('bollinger', bollinger_trade_signal(df), weight=1)
        signal_pool.add_signal('macd', macd_trade_signal(df), weight=1)
        signal_pool.add_signal('rsi', rsi_trade_signal(df), weight=1)
        signal_pool.add_signal('ml', model_trade_signal(df, model), weight=2)

        # Birleşik sinyali al ve işlem kararını loglayın
        combined_signal = signal_pool.get_combined_signal()
        
        # Basit bir doğrulama (örneğin, sinyalin geçerli olup olmadığını kontrol et)
        assert combined_signal in ['buy', 'sell', 'hold'], f"Unexpected signal: {combined_signal}"

        # Sinyal havuzunu temizle
        signal_pool.reset()