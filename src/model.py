import pandas as pd
import numpy as np
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

    Returns:
        tuple: A tuple containing the training and testing sets (X_train, X_test, y_train, y_test).
    """
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

    Returns:
        str: 'buy' if the model predicts an upward movement, 'sell' otherwise.
    """
    latest_return = df['close'].pct_change().iloc[-1]  # Calculate the latest return / En son getiriyi hesapla
    prediction = model.predict(pd.DataFrame([[latest_return]], columns=['returns']))  # Predict the direction / Yönü tahmin et
    return 'buy' if prediction == 1 else 'sell'  # Return 'buy' or 'sell' based on the prediction / Tahmine göre 'buy' veya 'sell' döndür