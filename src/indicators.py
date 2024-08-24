import pandas as pd

def simple_moving_average(df, period):
    """
    Calculates the Simple Moving Average (SMA) for the given period.

    Belirtilen periyot için Basit Hareketli Ortalama (SMA) hesaplar.

    Args:
        df (pd.DataFrame): Finansal verileri içeren DataFrame.
        period (int): SMA'nın hesaplanacağı periyot.

    Returns:
        pd.Series: SMA değerlerini içeren bir Seri.
    """
    return df['close'].astype(float).rolling(window=period).mean()

def bollinger_bands(df, window=20, no_of_std=2):
    """
    Calculates the Bollinger Bands for the given data.

    Verilen veri için Bollinger Bantlarını hesaplar.

    Args:
        df (pd.DataFrame): Finansal verileri içeren DataFrame.
        window (int): Hareketli ortalama için pencere boyutu (varsayılan: 20).
        no_of_std (int): Bantlar için standart sapma sayısı (varsayılan: 2).

    Returns:
        pd.DataFrame: SMA, Üst Bant ve Alt Bant için ek sütunlar içeren DataFrame.
    """
    df['SMA'] = df['close'].rolling(window=window).mean()
    df['STD'] = df['close'].rolling(window=window).std()
    df['Upper Band'] = df['SMA'] + (df['STD'] * no_of_std)
    df['Lower Band'] = df['SMA'] - (df['STD'] * no_of_std)
    return df

def bollinger_trade_signal(df, trend_period=50):
    """
    Generates a trade signal based on Bollinger Bands and a trend indicator.

    Bollinger Bantlarına ve bir trend göstergesine dayalı işlem sinyali üretir.

    Args:
        df (pd.DataFrame): Finansal verileri içeren DataFrame.
        trend_period (int): Trendin hesaplanacağı periyot (varsayılan: 50).

    Returns:
        str: Sinyale bağlı olarak 'buy', 'sell' veya 'hold'.
    """
    df = bollinger_bands(df)
    df['Trend'] = df['close'].rolling(window=trend_period).mean()
    
    if df['close'].iloc[-1] > df['Upper Band'].iloc[-1] and df['close'].iloc[-1] > df['Trend'].iloc[-1]:
        return 'sell'  # Overbought and in an upward trend / Aşırı alım ve yukarı trend
    elif df['close'].iloc[-1] < df['Lower Band'].iloc[-1] and df['close'].iloc[-1] < df['Trend'].iloc[-1]:
        return 'buy'  # Oversold and in a downward trend / Aşırı satım ve aşağı trend
    else:
        return 'hold'

def macd(df, slow=26, fast=12, signal=9):
    """
    Calculates the MACD (Moving Average Convergence Divergence) indicator.

    MACD (Hareketli Ortalama Yakınsama Uzaklaşma) göstergesini hesaplar.

    Args:
        df (pd.DataFrame): Finansal verileri içeren DataFrame.
        slow (int): Yavaş EMA periyodu (varsayılan: 26).
        fast (int): Hızlı EMA periyodu (varsayılan: 12).
        signal (int): Sinyal çizgisi EMA periyodu (varsayılan: 9).

    Returns:
        pd.DataFrame: MACD ve Sinyal Çizgisi için ek sütunlar içeren DataFrame.
    """
    df['EMA_slow'] = df['close'].ewm(span=slow, min_periods=slow).mean()
    df['EMA_fast'] = df['close'].ewm(span=fast, min_periods=fast).mean()
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']
    df['Signal Line'] = df['MACD'].ewm(span=signal, min_periods=signal).mean()
    return df

def macd_trade_signal(df, momentum_threshold=0.001):
    """
    Generates a trade signal based on the MACD indicator and momentum.

    MACD göstergesi ve momentum'a dayalı işlem sinyali üretir.

    Args:
        df (pd.DataFrame): Finansal verileri içeren DataFrame.
        momentum_threshold (float): Momentumun anlamlı kabul edileceği eşik değeri (varsayılan: 0.001).

    Returns:
        str: Sinyale bağlı olarak 'buy', 'sell' veya 'hold'.
    """
    df = macd(df)
    df['Momentum'] = abs(df['MACD'] - df['Signal Line'])

    if df['MACD'].iloc[-1] > df['Signal Line'].iloc[-1] and df['Momentum'].iloc[-1] > momentum_threshold:
        return 'buy'
    elif df['MACD'].iloc[-1] < df['Signal Line'].iloc[-1] and df['Momentum'].iloc[-1] > momentum_threshold:
        return 'sell'
    else:
        return 'hold'

def rsi(df, period=14):
    """
    Calculates the RSI (Relative Strength Index) for the given period.

    Verilen periyot için RSI (Göreceli Güç Endeksi) hesaplar.

    Args:
        df (pd.DataFrame): Finansal verileri içeren DataFrame.
        period (int): RSI'nın hesaplanacağı periyot (varsayılan: 14).

    Returns:
        pd.DataFrame: RSI değerleri için ek bir sütun içeren DataFrame.
    """
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def rsi_with_dynamic_period(df, base_period=14, volatility_threshold=0.02):
    """
    Calculates RSI with dynamic periods based on market volatility.

    Piyasa volatilitesine dayalı dinamik periyotlarla RSI hesaplar.

    Args:
        df (pd.DataFrame): DataFrame containing the financial data.
        base_period (int): The base period for calculating RSI (default: 14).
        volatility_threshold (float): The threshold for adjusting the period based on volatility (default: 0.02).

    Returns:
        pd.DataFrame: DataFrame with additional columns for RSI and dynamic periods.
    """
    df = df.copy()  # Veriyi kopyala
    df['Volatility'] = df['close'].pct_change().rolling(window=base_period).std()
    
    df['Dynamic Period'] = (base_period * (1 + df['Volatility'] / volatility_threshold)).fillna(base_period).astype(int).clip(lower=2)

    rsi_values = []
    for i in range(len(df)):
        period = df['Dynamic Period'].iloc[i]
        if i < period:
            rsi_values.append(None)
        else:
            temp_df = df.iloc[:i+1].copy()
            rsi_values.append(rsi(temp_df, period=period)['RSI'].iloc[-1])
    
    df['RSI'] = pd.Series(rsi_values, index=df.index)
    return df

def rsi_trade_signal(df):
    """
    Generates a trade signal based on RSI calculated with dynamic periods.

    Dinamik periyotlarla hesaplanan RSI'ya dayalı işlem sinyali üretir.

    Args:
        df (pd.DataFrame): DataFrame containing the financial data.

    Returns:
        str: 'buy', 'sell', or 'hold' depending on the signal.
    """
    df = rsi_with_dynamic_period(df)
    if df['RSI'].iloc[-1] < 30:
        return 'buy'
    elif df['RSI'].iloc[-1] > 70:
        return 'sell'
    else:
        return 'hold'

def rsi_macd_combined_signal(df):
    """
    Generates a trade signal based on the combination of RSI and MACD.

    RSI ve MACD kombinasyonuna dayalı işlem sinyali üretir.

    Args:
        df (pd.DataFrame): Finansal verileri içeren DataFrame.

    Returns:
        str: Kombine sinyale bağlı olarak 'buy', 'sell' veya 'hold'.
    """
    df = rsi(df)
    df = macd(df)
    
    if df['RSI'].iloc[-1] < 30 and df['MACD'].iloc[-1] > df['Signal Line'].iloc[-1]:
        return 'buy'
    elif df['RSI'].iloc[-1] > 70 and df['MACD'].iloc[-1] < df['Signal Line'].iloc[-1]:
        return 'sell'
    else:
        return 'hold'

def two_step_rsi_macd_signal(df):
    """
    Generates a trade signal using a two-step process combining RSI and MACD.

    RSI ve MACD kombinasyonunu kullanarak iki aşamalı bir işlem sinyali üretir.

    Args:
        df (pd.DataFrame): Finansal verileri içeren DataFrame.

    Returns:
        str: Sinyale bağlı olarak 'buy', 'sell' veya 'hold'.
    """
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