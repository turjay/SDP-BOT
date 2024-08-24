import time
from api import get_ohlcv, place_order, get_account_balance
from utils import check_balance
from indicators import bollinger_trade_signal, macd_trade_signal, rsi_trade_signal
from model import train_model, model_trade_signal
from config import logger
from signal_pool import SignalPool
import logging

# Logging ayarları; INFO seviyesindeki logları kaydetmek için yapılandırılıyor
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # İşlem yapılacak sembol ve miktarlar tanımlanıyor
    symbol = 'BTCTRY'  # İşlem yapılacak kripto para sembolü
    quantity = 0.000047  # Alım/satım işlemleri için BTC miktarı
    tl_quantity = 100  # Alım işlemi için kullanılacak TL miktarı
    model = None  # Makine öğrenmesi modeli için başlangıç değeri

    # Sinyal havuzu oluşturuluyor; farklı stratejilerin sinyallerini toplamak için kullanılıyor
    signal_pool = SignalPool()
    previous_combined_signal = None  # Önceki birleşik sinyalin takibi için

    try:
        while True:
            # TL bakiyesini kontrol etme ve yeterli bakiye varsa BTC alımı yapma
            if check_balance('TRY', tl_quantity, get_account_balance()):
                logger.info('Buying BTC...')
                place_order(symbol, 'buy', tl_quantity)  # Belirtilen TL miktarı ile BTC alımı yapılıyor
            else:
                logger.info("Not enough TL balance to buy BTC.")  # Yetersiz bakiye durumu loglanıyor
            
            # OHLCV verilerini al ve analiz et
            df = get_ohlcv(symbol)
            if df.empty:  # Eğer veri yoksa bu döngüyü atla
                logger.info("No data to analyze. Skipping iteration.")
                time.sleep(300)  # 5 dakika bekle ve tekrar dene
                continue
            
            # Makine Öğrenmesi Modelini Eğitme (İlk Döngüde)
            if model is None:
                model = train_model(df)  # OHLCV verisi kullanılarak model eğitiliyor
                logger.info("Model trained successfully.")
            
            # Farklı stratejilerden sinyalleri sinyal havuzuna ekle (Ağırlıklandırılmış)
            signal_pool.add_signal('bollinger', bollinger_trade_signal(df), weight=1)
            signal_pool.add_signal('macd', macd_trade_signal(df), weight=1)
            signal_pool.add_signal('rsi', rsi_trade_signal(df), weight=1)
            signal_pool.add_signal('ml', model_trade_signal(df, model), weight=2)  # ML sinyali daha güçlü

            # Sinyal havuzundan birleşik sinyali al
            combined_signal = signal_pool.get_combined_signal()

            # Eğer birleşik sinyal değişmişse işlem yap
            if combined_signal != previous_combined_signal:
                if combined_signal == 'buy':
                    logger.info('Buying BTC (Combined Signal)...')
                    place_order(symbol, 'buy', quantity)
                elif combined_signal == 'sell':
                    logger.info('Selling BTC (Combined Signal)...')
                    place_order(symbol, 'sell', quantity)

                # Mevcut sinyali güncelle
                previous_combined_signal = combined_signal

            # Sinyal havuzunu temizle
            signal_pool.reset()

            # Bir süre bekle ve tekrar başla
            time.sleep(300)
    
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        time.sleep(60)  # Hata durumunda bekleme süresi ekle

if __name__ == "__main__":
    main()