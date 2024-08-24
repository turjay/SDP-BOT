import os
import base64
import logging

# Logging ayarı; INFO seviyesindeki logları kaydetmek için yapılandırılıyor
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API anahtarlarını çevre değişkenlerinden alıyoruz
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# API_KEY ve API_SECRET'in varlığı kontrol ediliyor
if API_KEY is None or API_SECRET is None:
    raise ValueError("API_KEY and API_SECRET environment variables must be set.")

# API_SECRET base64 formatında encode edilmiştir; decode işlemi yapılıyor
api_secret = base64.b64decode(API_SECRET)

# API URL'leri
BASE_URL = 'https://api.btcturk.com'
GRAPH_API_URL = 'https://graph-api.btcturk.com'