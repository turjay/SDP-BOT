import sys
import os
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Dosya yollarını ayarlıyoruz
# Setting up file paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from indicators import bollinger_trade_signal, macd_trade_signal, rsi_trade_signal

# Verileri indir ve hazırla
# Download and prepare the data
def prepare_data(symbol='BTC-USD', period='3mo', interval='1h'):
    """
    Bitcoin'in son 3 aydaki fiyat verilerini indirir ve veri çerçevesini hazırlar.
    Downloads Bitcoin's price data for the last 3 months and prepares the DataFrame.

    Args:
        symbol (str): İndirilecek sembol. (Varsayılan: 'BTC-USD')
                      Symbol to download. (Default: 'BTC-USD')
        period (str): Veri aralığı. (Varsayılan: '3mo')
                      Data period. (Default: '3mo')
        interval (str): Zaman aralığı. (Varsayılan: '1h')
                        Time interval. (Default: '1h')

    Returns:
        pd.DataFrame: İndirilen ve işlenmiş veri çerçevesi.
                      Downloaded and processed DataFrame.
    """
    data = yf.download(symbol, period=period, interval=interval)
    data.reset_index(inplace=True)
    data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
    return data

# Veriyi indir ve hazırla
# Download and prepare the data
data = prepare_data()

# Her bir sinyal fonksiyonunu uygula ve haritalama yap
# Apply each signal function and map the results
def map_signals(data):
    """
    İndikatör sinyallerini uygular ve bu sinyalleri makine öğrenmesi modeline uygun hale getirir.
    Applies indicator signals and prepares them for the machine learning model.

    Args:
        data (pd.DataFrame): Finansal verileri içeren veri çerçevesi.
                             DataFrame containing financial data.

    Returns:
        pd.DataFrame: İşlenmiş veri çerçevesi.
                      Processed DataFrame.
    """
    data['bollinger_signal'] = data.apply(lambda x: bollinger_trade_signal(data), axis=1).map({'buy': 1, 'sell': -1, 'hold': 0})
    data['macd_signal'] = data.apply(lambda x: macd_trade_signal(data), axis=1).map({'buy': 1, 'sell': -1, 'hold': 0})
    data['rsi_signal'] = data.apply(lambda x: rsi_trade_signal(data), axis=1).map({'buy': 1, 'sell': -1, 'hold': 0})
    return data

data = map_signals(data)

# Hedef değişkeni oluştur
# Create the target variable
data['target'] = (data['close'].shift(-1) > data['close']).astype(int)

# NaN değerleri çıkar
# Drop NaN values
data.dropna(inplace=True)

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

# Veri ve sonuçları kontrol etme
# Checking the data and results
print("Head of X_train:")
print(X_train.head())
print("\nHead of y_train:")
print(y_train.head())