import pandas as pd

# Basit hareketli ortalamayı hesaplayan fonksiyon
def simple_moving_average(df, period):
    return df['close'].astype(float).rolling(window=period).mean()

# Bollinger Bantlarını hesaplayan fonksiyon
def bollinger_bands(df, window=20, no_of_std=2):
    df['SMA'] = df['close'].rolling(window=window).mean()
    df['STD'] = df['close'].rolling(window=window).std()
    df['Upper Band'] = df['SMA'] + (df['STD'] * no_of_std)
    df['Lower Band'] = df['SMA'] - (df['STD'] * no_of_std)
    return df

# Bollinger bantlarına dayalı işlem sinyali üreten fonksiyon
def bollinger_trade_signal(df, trend_period=50):
    df = bollinger_bands(df)
    df['Trend'] = df['close'].rolling(window=trend_period).mean()
    
    if df['close'].iloc[-1] > df['Upper Band'].iloc[-1] and df['close'].iloc[-1] > df['Trend'].iloc[-1]:
        return 'sell'  # Aşırı alım ve yukarı trend
    elif df['close'].iloc[-1] < df['Lower Band'].iloc[-1] and df['close'].iloc[-1] < df['Trend'].iloc[-1]:
        return 'buy'  # Aşırı satım ve aşağı trend
    else:
        return 'hold'

# MACD göstergesini hesaplayan fonksiyon
def macd(df, slow=26, fast=12, signal=9):
    df['EMA_slow'] = df['close'].ewm(span=slow, min_periods=slow).mean()
    df['EMA_fast'] = df['close'].ewm(span=fast, min_periods=fast).mean()
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']
    df['Signal Line'] = df['MACD'].ewm(span=signal, min_periods=signal).mean()
    return df

# MACD göstergesine dayalı işlem sinyali üreten fonksiyon
def macd_trade_signal(df, momentum_threshold=0.001):
    df = macd(df)
    df['Momentum'] = abs(df['MACD'] - df['Signal Line'])

    if df['MACD'].iloc[-1] > df['Signal Line'].iloc[-1] and df['Momentum'].iloc[-1] > momentum_threshold:
        return 'buy'
    elif df['MACD'].iloc[-1] < df['Signal Line'].iloc[-1] and df['Momentum'].iloc[-1] > momentum_threshold:
        return 'sell'
    else:
        return 'hold'

# RSI göstergesini hesaplayan fonksiyon
def rsi(df, period=14):
    df = df.copy()  # DataFrame'in bir kopyasını oluşturun
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    df.loc[:, 'RSI'] = 100 - (100 / (1 + rs))  # .loc ile değeri doğrudan güncelleyin
    return df

# RSI göstergesini dinamik periyotlarla hesaplayan fonksiyon
def rsi_with_dynamic_period(df, base_period=14, volatility_threshold=0.02):
    df['Volatility'] = df['close'].pct_change().rolling(window=base_period).std()
    df['Dynamic Period'] = (base_period * (1 + df['Volatility'] / volatility_threshold)).fillna(base_period).astype(int).clip(lower=2)
    
    rsi_values = []
    for i in range(len(df)):
        period = df['Dynamic Period'].iloc[i]
        if i < period:
            rsi_values.append(None)
        else:
            rsi_values.append(rsi(df.iloc[:i+1], period=period)['RSI'].iloc[-1])
    
    df['RSI'] = pd.Series(rsi_values, index=df.index)
    return df

# RSI göstergesine dayalı işlem sinyali üreten fonksiyon (Dinamik Periyot ile)
def rsi_trade_signal(df):
    df = rsi_with_dynamic_period(df)
    if df['RSI'].iloc[-1] < 30:
        return 'buy'
    elif df['RSI'].iloc[-1] > 70:
        return 'sell'
    else:
        return 'hold'

# RSI ve MACD kombinasyonuna dayalı işlem sinyali üreten fonksiyon
def rsi_macd_combined_signal(df):
    df = rsi(df)
    df = macd(df)
    
    if df['RSI'].iloc[-1] < 30 and df['MACD'].iloc[-1] > df['Signal Line'].iloc[-1]:
        return 'buy'
    elif df['RSI'].iloc[-1] > 70 and df['MACD'].iloc[-1] < df['Signal Line'].iloc[-1]:
        return 'sell'
    else:
        return 'hold'

# İki aşamalı RSI ve MACD kombinasyonu
def two_step_rsi_macd_signal(df):
    df = rsi(df)
    df = macd(df)
    
    rsi_signal = None
    macd_signal = None
    
    if df['RSI'].iloc[-1] < 30:
        rsi_signal = 'buy'
    elif df['RSI'].iloc[-1] > 70:
        rsi_signal = 'sell'
    
    if df['MACD'].iloc[-1] > df['Signal Line'].iloc[-1]:
        macd_signal = 'buy'
    elif df['MACD'].iloc[-1] < df['Signal Line'].iloc[-1]:
        macd_signal = 'sell'
    
    return rsi_signal if rsi_signal == macd_signal else 'hold'