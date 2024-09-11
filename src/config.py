import os
import base64
import logging

<<<<<<< HEAD
# Configure the logging system to capture logs at the INFO level
=======
# Logging configuration; sets up logging to capture INFO level logs
# Logging ayarı; INFO seviyesindeki logları kaydetmek için yapılandırılıyor
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve API keys from environment variables
<<<<<<< HEAD
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Check if API_KEY and API_SECRET are set, raise an error if not
if not API_KEY or not API_SECRET:
    raise ValueError("API_KEY and API_SECRET environment variables must be set.")

# Decode the API_SECRET, which is stored in base64 format
try:
    api_secret = base64.b64decode(API_SECRET)
except Exception as e:
    raise ValueError("Failed to decode API_SECRET. Make sure it is correctly base64-encoded.") from e

# API base URLs for different services
BASE_URL = 'https://api.btcturk.com'  # Base URL for primary API
GRAPH_API_URL = 'https://graph-api.btcturk.com'  # Base URL for graph API (historical data)

# Logging configuration settings
logger.info("API keys and base URLs loaded successfully.")
=======
# API anahtarlarını çevre değişkenlerinden alıyoruz
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Check if API_KEY and API_SECRET are set
# API_KEY ve API_SECRET'in varlığı kontrol ediliyor
if API_KEY is None or API_SECRET is None:
    raise ValueError("API_KEY and API_SECRET environment variables must be set.")
    # Eğer API_KEY ve API_SECRET çevre değişkenleri ayarlanmamışsa hata fırlatılır

# Decode the API_SECRET which is encoded in base64 format
# API_SECRET base64 formatında encode edilmiştir; decode işlemi yapılıyor
api_secret = base64.b64decode(API_SECRET)

# API URLs for different endpoints
# Farklı uç noktalar için API URL'leri
BASE_URL = 'https://api.btcturk.com'
GRAPH_API_URL = 'https://graph-api.btcturk.com'
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
