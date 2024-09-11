import sys
import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import additional signals
from indicators import stochastic_trade_signal, atr_trade_signal
from config import logger

def run_backtests():
    logger.info("Running backtests with various indicators...")

    balance_bollinger, trade_log_bollinger = run_backtest(bollinger_trade_signal, 'Bollinger Bands')
    balance_macd, trade_log_macd = run_backtest(macd_trade_signal, 'MACD')
    balance_rsi, trade_log_rsi = run_backtest(rsi_trade_signal, 'RSI')
    balance_stochastic, trade_log_stochastic = run_backtest(stochastic_trade_signal, 'Stochastic Oscillator')
    balance_atr, trade_log_atr = run_backtest(atr_trade_signal, 'ATR')
    balance_ml, trade_log_ml = run_ml_backtest()

    # Calculate total balance
    total_balance = [
        (balance_bollinger[i] + balance_macd[i] + balance_rsi[i] + balance_ml[i] +
         balance_stochastic[i] + balance_atr[i]) / 6
        for i in range(len(balance_bollinger))
    ]

    # Plot results
    data = get_yahoo_data()
    plt.plot(data['Datetime'][20:], balance_bollinger, label='Balance Over Time (Bollinger Bands)')
    plt.plot(data['Datetime'][20:], balance_macd, label='Balance Over Time (MACD)')
    plt.plot(data['Datetime'][20:], balance_rsi, label='Balance Over Time (RSI)')
    plt.plot(data['Datetime'][20:], balance_stochastic, label='Balance Over Time (Stochastic Oscillator)')
    plt.plot(data['Datetime'][20:], balance_atr, label='Balance Over Time (ATR)')
    plt.plot(data['Datetime'][20:], balance_ml, label='Balance Over Time (ML)')
    plt.plot(data['Datetime'][20:], total_balance, label='Total Balance', linestyle='--', linewidth=2, color='purple')

    plt.xlabel('Date')
    plt.ylabel('Balance (USD)')
    plt.title('Backtesting Balance Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_backtests()