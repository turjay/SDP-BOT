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
            # Check TL balance and buy BTC if sufficient balance is available
            # TL bakiyesini kontrol etme ve yeterli bakiye varsa BTC alımı yapma
            if check_balance('TRY', tl_quantity, get_account_balance()):
                logger.info('Buying BTC...')
                place_order(symbol, 'buy', tl_quantity)  # Purchase BTC with the specified TL amount / Belirtilen TL miktarı ile BTC alımı yapılıyor
            else:
                logger.info("Not enough TL balance to buy BTC.")  # Log if balance is insufficient / Yetersiz bakiye durumu loglanıyor
            
            # Fetch and analyze OHLCV data
            # OHLCV verilerini al ve analiz et
            df = get_ohlcv(symbol)
            if df.empty:  # Skip this iteration if no data is available / Eğer veri yoksa bu döngüyü atla
                logger.info("No data to analyze. Skipping iteration.")
                time.sleep(300)  # Wait for 5 minutes and try again / 5 dakika bekle ve tekrar dene
                continue
            
            # Train the machine learning model (only in the first loop)
            # Makine Öğrenmesi Modelini Eğitme (İlk Döngüde)
            if model is None:
                model = train_model(df)  # Train the model using OHLCV data / OHLCV verisi kullanılarak model eğitiliyor
                logger.info("Model trained successfully.")
            
            # Add signals from different strategies to the signal pool (weighted)
            # Farklı stratejilerden sinyalleri sinyal havuzuna ekle (Ağırlıklandırılmış)
            signal_pool.add_signal('bollinger', bollinger_trade_signal(df), weight=1)
            signal_pool.add_signal('macd', macd_trade_signal(df), weight=1)
            signal_pool.add_signal('rsi', rsi_trade_signal(df), weight=1)
            signal_pool.add_signal('ml', model_trade_signal(df, model), weight=2)  # ML signal is given more weight / ML sinyali daha güçlü

            # Get the combined signal from the signal pool
            # Sinyal havuzundan birleşik sinyali al
            combined_signal = signal_pool.get_combined_signal()

            # Execute a trade if the combined signal has changed
            # Eğer birleşik sinyal değişmişse işlem yap
            if combined_signal != previous_combined_signal:
                if combined_signal == 'buy':
                    logger.info('Buying BTC (Combined Signal)...')
                    place_order(symbol, 'buy', quantity)
                elif combined_signal == 'sell':
                    logger.info('Selling BTC (Combined Signal)...')
                    place_order(symbol, 'sell', quantity)

                # Update the previous signal
                # Mevcut sinyali güncelle
                previous_combined_signal = combined_signal

            # Reset the signal pool
            # Sinyal havuzunu temizle
            signal_pool.reset()

            # Wait for a while before the next iteration
            # Bir süre bekle ve tekrar başla
            time.sleep(300)
    
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        time.sleep(60)  # Add a delay in case of error / Hata durumunda bekleme süresi ekle

if __name__ == "__main__":
    main()
