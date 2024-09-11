import pandas as pd
import numpy as np
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

    Returns:
        tuple: A tuple containing the training and testing sets (X_train, X_test, y_train, y_test).
    """
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

    Returns:
        str: 'buy' if the model predicts an upward movement, 'sell' otherwise.
    """
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