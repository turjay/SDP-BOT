import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Verileri makine öğrenmesi modeline uygun hale getiren fonksiyon
def prepare_data(df):
    df['returns'] = df['close'].pct_change()
    df['direction'] = np.where(df['returns'] > 0, 1, 0)
    df = df.dropna()
    X = df[['returns']]
    y = df['direction']
    return train_test_split(X, y, test_size=0.2, random_state=42)

# Karar ağacı modeli ile verileri eğiten fonksiyon
def train_model(df):
    X_train, X_test, y_train, y_test = prepare_data(df)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    return model

# Eğitilmiş model ile işlem sinyali üreten fonksiyon
def model_trade_signal(df, model):
    latest_return = df['close'].pct_change().iloc[-1]
    prediction = model.predict(pd.DataFrame([[latest_return]], columns=['returns']))
    return 'buy' if prediction == 1 else 'sell'