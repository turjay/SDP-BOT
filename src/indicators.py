import pandas as pd

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
    """
    df['SMA'] = df['close'].rolling(window=window).mean()
    df['STD'] = df['close'].rolling(window=window).std()
    df['Upper Band'] = df['SMA'] + (df['STD'] * no_of_std)
    df['Lower Band'] = df['SMA'] - (df['STD'] * no_of_std)
    return df

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
    """
    df['EMA_slow'] = df['close'].ewm(span=slow, min_periods=slow).mean()
    df['EMA_fast'] = df['close'].ewm(span=fast, min_periods=fast).mean()
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']
    df['Signal Line'] = df['MACD'].ewm(span=signal, min_periods=signal).mean()
    return df

def macd_trade_signal(df: pd.DataFrame, momentum_threshold: float = 0.001) -> str:
    """
    Generates a trading signal based on the MACD indicator and momentum.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
        momentum_threshold (float, optional): The threshold for momentum strength (default is 0.001).

    Returns:
        str: 'buy' if MACD is above the Signal Line and momentum is strong, 'sell' if MACD is below the Signal Line and momentum is strong, otherwise 'hold'.
    """
    df = macd(df)
    df['Momentum'] = abs(df['MACD'] - df['Signal Line'])

    if df['MACD'].iloc[-1] > df['Signal Line'].iloc[-1] and df['Momentum'].iloc[-1] > momentum_threshold:
        return 'buy'
    elif df['MACD'].iloc[-1] < df['Signal Line'].iloc[-1] and df['Momentum'].iloc[-1] > momentum_threshold:
        return 'sell'
    else:
        return 'hold'

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
    if df['RSI'].iloc[-1] < 30:
        return 'buy'
    elif df['RSI'].iloc[-1] > 70:
        return 'sell'
    else:
        return 'hold'

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
        return 'sell'
    else:
        return 'hold'

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