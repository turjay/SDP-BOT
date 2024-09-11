import pandas as pd
import numpy as np
<<<<<<< HEAD
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from indicators import simple_moving_average

def prepare_data(df: pd.DataFrame) -> tuple:
    """
    Prepares the data for the machine learning model by calculating returns,
    adding moving averages, and creating a binary direction column.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
            Expected columns: ['close', 'volume'].
=======
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

def prepare_data(df):
    """
    Prepares the data for the machine learning model.

    Makine öğrenmesi modeli için verileri hazırlar.

    This function calculates the percentage change in the closing prices (returns)
    and assigns a binary direction (1 for upward movement, 0 for downward movement).
    NaN values are dropped before splitting the data into features (X) and target (y).

    Bu fonksiyon, kapanış fiyatlarındaki yüzde değişimini (getiriler) hesaplar ve 
    ikili bir yön (1 yukarı hareket, 0 aşağı hareket) atar. NaN değerleri kaldırıldıktan 
    sonra veriler özellikler (X) ve hedef (y) olarak ayrılır.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de

    Returns:
        tuple: A tuple containing the training and testing sets (X_train, X_test, y_train, y_test).
    """
<<<<<<< HEAD
    # Calculate percentage change (returns) based on the 'close' price
    df['returns'] = df['close'].pct_change()

    # Add Simple Moving Average (SMA) as a new feature
    df['SMA_50'] = simple_moving_average(df, period=50)
    df['SMA_200'] = simple_moving_average(df, period=200)

    # Create a 'direction' column: 1 if returns are positive, 0 otherwise
    df['direction'] = np.where(df['returns'] > 0, 1, 0)

    # Drop any rows with NaN values that were created during the calculation
    df = df.dropna()

    # Define the features (X) including returns and moving averages, and the target variable (y)
    X = df[['returns', 'SMA_50', 'SMA_200', 'volume']]  # Adding volume and moving averages
    y = df['direction']

    # Split the data into training and testing sets (80% training, 20% testing)
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(df: pd.DataFrame, model_type: str = 'random_forest') -> RandomForestClassifier:
    """
    Trains a machine learning model on the prepared financial data.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
        model_type (str, optional): The type of model to use. Options are 'random_forest' or 'decision_tree'.
            Default is 'random_forest'.

    Returns:
        Trained model (RandomForestClassifier, DecisionTreeClassifier).
    """
    # Prepare the data by splitting it into training and testing sets
    X_train, X_test, y_train, y_test = prepare_data(df)

    # Initialize and train the chosen model
    if model_type == 'random_forest':
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
        from sklearn.tree import DecisionTreeClassifier
        model = DecisionTreeClassifier()

    model.fit(X_train, y_train)

    # Evaluate the model's accuracy and F1 score on the test set
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"Model Accuracy: {accuracy:.2f}")
    print(f"Model F1 Score: {f1:.2f}")

    return model

def model_trade_signal(df: pd.DataFrame, model) -> str:
    """
    Generates a trade signal based on the trained machine learning model.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
        model: The trained machine learning model.
=======
    df['returns'] = df['close'].pct_change()  # Calculate percentage change in closing prices / Kapanış fiyatlarındaki yüzde değişimi hesaplar
    df['direction'] = np.where(df['returns'] > 0, 1, 0)  # Assign direction based on returns / Getirilere göre yön ataması yapar
    df = df.dropna()  # Drop NaN values / NaN değerleri kaldırır
    X = df[['returns']]
    y = df['direction']
    return train_test_split(X, y, test_size=0.2, random_state=42)  # Split the data into training and testing sets / Veriyi eğitim ve test setlerine ayırır

def train_model(df):
    """
    Trains a Decision Tree Classifier on the prepared data.

    Hazırlanan veriler üzerinde bir Karar Ağacı Sınıflandırıcısı eğitir.

    This function uses the training set to fit a Decision Tree model,
    which can later be used to predict the direction of price movements.

    Bu fonksiyon, bir Karar Ağacı modelini eğitmek için eğitim setini kullanır ve
    bu model daha sonra fiyat hareketlerinin yönünü tahmin etmek için kullanılabilir.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.

    Returns:
        DecisionTreeClassifier: The trained Decision Tree model.
    """
    X_train, X_test, y_train, y_test = prepare_data(df)  # Prepare the data / Verileri hazırla
    model = DecisionTreeClassifier()  # Initialize the Decision Tree Classifier / Karar Ağacı Sınıflandırıcısını başlat
    model.fit(X_train, y_train)  # Train the model on the training data / Modeli eğitim verileri üzerinde eğit
    return model

def model_trade_signal(df, model):
    """
    Generates a trade signal based on the trained machine learning model.

    Eğitilmiş makine öğrenmesi modeline dayalı olarak işlem sinyali üretir.

    This function calculates the most recent return and uses the trained model
    to predict whether to buy or sell based on that return.

    Bu fonksiyon, en son getiriyi hesaplar ve eğitilmiş modeli kullanarak
    bu getirinin üzerine alım veya satım yapılacağını tahmin eder.

    Args:
        df (pd.DataFrame): The input DataFrame containing the financial data.
        model (DecisionTreeClassifier): The trained Decision Tree model.
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de

    Returns:
        str: 'buy' if the model predicts an upward movement, 'sell' otherwise.
    """
<<<<<<< HEAD
    # Calculate the latest return and moving averages for the most recent data point
    latest_return = df['close'].pct_change().iloc[-1]
    sma_50 = df['SMA_50'].iloc[-1]
    sma_200 = df['SMA_200'].iloc[-1]
    volume = df['volume'].iloc[-1]

    # Create the input features for prediction
    input_data = pd.DataFrame([[latest_return, sma_50, sma_200, volume]],
                              columns=['returns', 'SMA_50', 'SMA_200', 'volume'])

    # Predict the direction based on the latest data
    prediction = model.predict(input_data)

    # Return 'buy' if the model predicts upward movement, otherwise 'sell'
    return 'buy' if prediction == 1 else 'sell'
=======
    latest_return = df['close'].pct_change().iloc[-1]  # Calculate the latest return / En son getiriyi hesapla
    prediction = model.predict(pd.DataFrame([[latest_return]], columns=['returns']))  # Predict the direction / Yönü tahmin et
    return 'buy' if prediction == 1 else 'sell'  # Return 'buy' or 'sell' based on the prediction / Tahmine göre 'buy' veya 'sell' döndür
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
