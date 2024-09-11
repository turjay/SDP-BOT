import pandas as pd

<<<<<<< HEAD
def simple_moving_average(df: pd.DataFrame, period: int) -> pd.Series:
    """
    Calculates the Simple Moving Average (SMA) for a given period.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
        period (int): The period over which to calculate the moving average.

    Returns:
        pd.Series: A series representing the moving average.
    """
    return df['close'].astype(float).rolling(window=period).mean()

def bollinger_bands(df: pd.DataFrame, window: int = 20, no_of_std: int = 2) -> pd.DataFrame:
    """
    Calculates Bollinger Bands for the given data.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
        window (int, optional): The window size for the rolling mean (default is 20).
        no_of_std (int, optional): The number of standard deviations for the upper/lower bands (default is 2).

    Returns:
        pd.DataFrame: The DataFrame with added 'SMA', 'Upper Band', and 'Lower Band' columns.
=======
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
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
    """
    df['SMA'] = df['close'].rolling(window=window).mean()
    df['STD'] = df['close'].rolling(window=window).std()
    df['Upper Band'] = df['SMA'] + (df['STD'] * no_of_std)
    df['Lower Band'] = df['SMA'] - (df['STD'] * no_of_std)
    return df

<<<<<<< HEAD
def bollinger_trade_signal(df: pd.DataFrame, window: int = 20, no_of_std: int = 2, trend_period: int = 50) -> str:
    """
    Generates a trading signal based on Bollinger Bands and a trend filter.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
        window (int, optional): The window size for the rolling mean (default is 20).
        no_of_std (int, optional): The number of standard deviations for the upper/lower bands (default is 2).
        trend_period (int, optional): The period for calculating the trend (default is 50).

    Returns:
        str: 'buy' if the price is below the lower band and trend is down, 'sell' if price is above the upper band and trend is up, otherwise 'hold'.
    """
    df = bollinger_bands(df, window=window, no_of_std=no_of_std)
    df['Trend'] = df['close'].rolling(window=trend_period).mean()

    if df['close'].iloc[-1] > df['Upper Band'].iloc[-1] and df['close'].iloc[-1] > df['Trend'].iloc[-1]:
        return 'sell'
    elif df['close'].iloc[-1] < df['Lower Band'].iloc[-1] and df['close'].iloc[-1] < df['Trend'].iloc[-1]:
        return 'buy'
    else:
        return 'hold'

def macd(df: pd.DataFrame, slow: int = 26, fast: int = 12, signal: int = 9) -> pd.DataFrame:
    """
    Calculates the MACD (Moving Average Convergence Divergence) indicator.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
        slow (int, optional): The period for the slow EMA (default is 26).
        fast (int, optional): The period for the fast EMA (default is 12).
        signal (int, optional): The period for the signal line EMA (default is 9).

    Returns:
        pd.DataFrame: The DataFrame with added 'EMA_slow', 'EMA_fast', 'MACD', and 'Signal Line' columns.
=======
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
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
    """
    df['EMA_slow'] = df['close'].ewm(span=slow, min_periods=slow).mean()
    df['EMA_fast'] = df['close'].ewm(span=fast, min_periods=fast).mean()
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']
    df['Signal Line'] = df['MACD'].ewm(span=signal, min_periods=signal).mean()
    return df

<<<<<<< HEAD
def macd_trade_signal(df: pd.DataFrame, momentum_threshold: float = 0.001) -> str:
    """
    Generates a trading signal based on the MACD indicator and momentum.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
        momentum_threshold (float, optional): The threshold for momentum strength (default is 0.001).

    Returns:
        str: 'buy' if MACD is above the Signal Line and momentum is strong, 'sell' if MACD is below the Signal Line and momentum is strong, otherwise 'hold'.
=======
def macd_trade_signal(df, momentum_threshold=0.001):
    """
    Generates a trade signal based on the MACD indicator and momentum.

    MACD göstergesi ve momentum'a dayalı işlem sinyali üretir.

    Args:
        df (pd.DataFrame): Finansal verileri içeren DataFrame.
        momentum_threshold (float): Momentumun anlamlı kabul edileceği eşik değeri (varsayılan: 0.001).

    Returns:
        str: Sinyale bağlı olarak 'buy', 'sell' veya 'hold'.
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
    """
    df = macd(df)
    df['Momentum'] = abs(df['MACD'] - df['Signal Line'])

    if df['MACD'].iloc[-1] > df['Signal Line'].iloc[-1] and df['Momentum'].iloc[-1] > momentum_threshold:
        return 'buy'
    elif df['MACD'].iloc[-1] < df['Signal Line'].iloc[-1] and df['Momentum'].iloc[-1] > momentum_threshold:
        return 'sell'
    else:
        return 'hold'

<<<<<<< HEAD
def rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Calculates the Relative Strength Index (RSI) for the given data.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
        period (int, optional): The period over which to calculate RSI (default is 14).

    Returns:
        pd.DataFrame: The DataFrame with an added 'RSI' column.
    """
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def rsi_trade_signal(df: pd.DataFrame) -> str:
    """
    Generates a trading signal based on the RSI indicator.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.

    Returns:
        str: 'buy' if RSI is below 30 (oversold), 'sell' if RSI is above 70 (overbought), otherwise 'hold'.
    """
    df = rsi(df)
=======
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
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
    if df['RSI'].iloc[-1] < 30:
        return 'buy'
    elif df['RSI'].iloc[-1] > 70:
        return 'sell'
    else:
        return 'hold'

<<<<<<< HEAD
def stochastic_oscillator(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Calculates the Stochastic Oscillator for the given data.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
        period (int, optional): The period over which to calculate the Stochastic Oscillator (default is 14).

    Returns:
        pd.DataFrame: The DataFrame with added '%K' and '%D' columns.
    """
    df['L14'] = df['low'].rolling(window=period).min()
    df['H14'] = df['high'].rolling(window=period).max()
    df['%K'] = 100 * ((df['close'] - df['L14']) / (df['H14'] - df['L14']))
    df['%D'] = df['%K'].rolling(window=3).mean()
    return df

def stochastic_trade_signal(df: pd.DataFrame) -> str:
    """
    Generates a trading signal based on the Stochastic Oscillator.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.

    Returns:
        str: 'buy' if %K is below 20 and rising, 'sell' if %K is above 80 and falling, otherwise 'hold'.
    """
    df = stochastic_oscillator(df)
    if df['%K'].iloc[-1] < 20 and df['%K'].iloc[-1] > df['%K'].iloc[-2]:
        return 'buy'
    elif df['%K'].iloc[-1] > 80 and df['%K'].iloc[-1] < df['%K'].iloc[-2]:
=======
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
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
        return 'sell'
    else:
        return 'hold'

<<<<<<< HEAD
def atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Calculates the Average True Range (ATR) indicator for the given data.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
        period (int, optional): The period over which to calculate ATR (default is 14).

    Returns:
        pd.DataFrame: The DataFrame with an added 'ATR' column.
    """
    df['HL'] = df['high'] - df['low']
    df['HC'] = abs(df['high'] - df['close'].shift())
    df['LC'] = abs(df['low'] - df['close'].shift())
    df['TR'] = df[['HL', 'HC', 'LC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=period).mean()
    return df

def atr_trade_signal(df: pd.DataFrame) -> str:
    """
    Generates a trading signal based on the ATR indicator.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.

    Returns:
        str: 'buy' if volatility is low and increasing, 'sell' if volatility is high and decreasing, otherwise 'hold'.
    """
    df = atr(df)
    latest_atr = df['ATR'].iloc[-1]
    previous_atr = df['ATR'].iloc[-2]
    volatility_change = latest_atr - previous_atr

    if volatility_change > 0 and latest_atr < df['ATR'].mean():
        return 'buy'
    elif volatility_change < 0 and latest_atr > df['ATR'].mean():
        return 'sell'
    else:
        return 'hold'
=======
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
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
