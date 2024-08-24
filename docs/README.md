# SDP-BOT: Strategic Dynamic Profits Bot

## Overview

SDP-BOT is an advanced cryptocurrency trading bot developed in Python, designed to analyze financial market data and execute trades based on machine learning and technical indicators. This bot is capable of backtesting strategies, evaluating market conditions, and making real-time trading decisions using a combination of machine learning models and traditional trading signals.

## Features

- **Machine Learning Integration**: Utilizes Decision Tree Classifiers to predict market movements.
- **Technical Indicators**: Implements Bollinger Bands, MACD, and RSI to generate trading signals.
- **Modular Design**: Structured to allow easy expansion and modification.
- **Backtesting Capabilities**: Allows for backtesting of trading strategies with historical data.

## Project Structure

```
├── LICENSE
├── README.md
├── requirements.txt
├── src/
│   ├── api.py
│   ├── config.py
│   ├── indicators.py
│   ├── main.py
│   ├── model.py
│   ├── signal_pool.py
│   └── utils.py
├── tests/
│   └── backtesting_usd_btc.py
└── docs/
    └── README.md
```

- **`api.py`**: Handles API interactions with the crypto exchange, including order placement and fetching market data.
- **`config.py`**: Contains configuration settings and environment variable handling for API keys and endpoints.
- **`indicators.py`**: Implements various technical indicators like Bollinger Bands, MACD, and RSI.
- **`main.py`**: The main script that runs the trading bot, integrating various components to make trading decisions.
- **`model.py`**: Contains the machine learning model and functions to train it and generate trading signals.
- **`signal_pool.py`**: Manages the aggregation of different trading signals to make a final decision.
- **`utils.py`**: Utility functions for balance checks and quantity formatting.
- **`backtesting_usd_btc.py`**: Script for backtesting the bot's performance using historical BTC/USD data.
- **`machine_learning.py`**: Contains the implementation and training procedures for the machine learning model, including data preprocessing, model architecture definition, training loops, and evaluation metrics for generating trading signals.

## Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed. You will also need to install the required Python packages listed in the `requirements.txt` file.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/turjay/sdp-bot.git
   cd sdp-bot
    ```
2. Install the required packages:
   ```bash
    pip install -r requirements.txt
    ```
### Usage

1. Configure API Keys: Set up your API keys in the environment variables:
    export API_KEY="your_api_key"
    export API_SECRET="your_api_secret"

2. Running the Bot:
    ```bash
    python src/main.py
    ```
3. Backtesting:
    ```bash
    python tests/backtesting_usd_btc.py
    ```
## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or suggestions.

### License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- **LinkedIn**: [Türkay Kurtaran](https://www.linkedin.com/in/türkay-kurtaran-27b660324/)
- **Instagram**: [turjayay](https://www.instagram.com/turjayay/)
