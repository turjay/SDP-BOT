import time
from api import get_ohlcv, place_order, get_account_balance
from utils import check_balance
from indicators import bollinger_trade_signal, macd_trade_signal, rsi_trade_signal
from model import train_model, model_trade_signal
from config import logger
from signal_pool import SignalPool
import logging

# Configure logging to capture INFO level logs
# Logging ayarları; INFO seviyesindeki logları kaydetmek için yapılandırılıyor
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    The main function that runs the trading bot.

    Bu fonksiyon, ticaret botunu çalıştıran ana fonksiyondur.
    
    The function fetches market data, analyzes it using various strategies
    including machine learning models, and executes trades based on the signals generated.

    Fonksiyon, piyasa verilerini alır, çeşitli stratejiler (makine öğrenmesi modelleri dahil) 
    kullanarak analiz eder ve üretilen sinyallere göre alım satım işlemleri gerçekleştirir.
    """
    
    # Define the trading symbol and amounts
    # İşlem yapılacak sembol ve miktarlar tanımlanıyor
    symbol = 'BTCTRY'  # The trading symbol for the cryptocurrency / İşlem yapılacak kripto para sembolü
    quantity = 0.000047  # Amount of BTC for buy/sell orders / Alım/satım işlemleri için BTC miktarı
    tl_quantity = 100  # Amount of TL to be used for purchasing / Alım işlemi için kullanılacak TL miktarı
    model = None  # Initial value for the machine learning model / Makine öğrenmesi modeli için başlangıç değeri

    # Create a signal pool to aggregate signals from different strategies
    # Sinyal havuzu oluşturuluyor; farklı stratejilerin sinyallerini toplamak için kullanılıyor
    signal_pool = SignalPool()
    previous_combined_signal = None  # To keep track of the previous combined signal / Önceki birleşik sinyalin takibi için

    try:
        while True:
            try:
                # Check TL balance and buy BTC if sufficient balance is available
                if check_balance('TRY', tl_quantity, get_account_balance()):
                    logger.info('Buying BTC...')
                    place_order(symbol, 'buy', tl_quantity)
                else:
                    logger.info("Not enough TL balance to buy BTC.")
                
                # Fetch and analyze OHLCV data
                df = get_ohlcv(symbol)
                if df.empty:
                    logger.info("No data to analyze. Skipping iteration.")
                    time.sleep(300)
                    continue
                
                # Train the machine learning model (only in the first loop)
                if model is None:
                    model = train_model(df)
                    logger.info("Model trained successfully.")
                
                # Add signals from different strategies to the signal pool (weighted)
                signal_pool.add_signal('bollinger', bollinger_trade_signal(df), weight=1)
                signal_pool.add_signal('macd', macd_trade_signal(df), weight=1)
                signal_pool.add_signal('rsi', rsi_trade_signal(df), weight=1)
                signal_pool.add_signal('ml', model_trade_signal(df, model), weight=2)

                # Get the combined signal from the signal pool
                combined_signal = signal_pool.get_combined_signal()

                # Execute a trade if the combined signal has changed
                if combined_signal != previous_combined_signal:
                    if combined_signal == 'buy':
                        logger.info('Buying BTC (Combined Signal)...')
                        place_order(symbol, 'buy', quantity)
                    elif combined_signal == 'sell':
                        logger.info('Selling BTC (Combined Signal)...')
                        place_order(symbol, 'sell', quantity)

                    # Update the previous signal
                    previous_combined_signal = combined_signal

                # Reset the signal pool
                signal_pool.reset()

                # Wait for a while before the next iteration
                time.sleep(300)
            
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                time.sleep(60)  # Add a delay in case of error

    except KeyboardInterrupt:
        logger.info("Bot interrupted by user.")

if __name__ == "__main__":
    main()