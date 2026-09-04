import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", 1234567)) 
    API_HASH = os.environ.get("API_HASH", "your_api_hash_here")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token_here")
    
    OWNER_ID = 8320250081
    
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", -1004440187778))
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -1004379104913))
    
    MONGO_URI_1 = os.environ.get("MONGO_URI_1", "your_primary_mongodb_url")
    MONGO_URI_2 = os.environ.get("MONGO_URI_2", "") 
    MONGO_URI_3 = os.environ.get("MONGO_URI_3", "") 
    
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "FileStoreBotDB")
    
    CUSTOM_DOMAIN = os.environ.get("CUSTOM_DOMAIN", "https://luxeflix.souravbosu947.workers.dev")
    # 🚀 CUSTOM_PREFIX রিমুভ করা হয়েছে আপনার নির্দেশ অনুযায়ী
    
    FSUB_CHANNELS = os.environ.get("FSUB_CHANNELS", "")
    SUPPORT_LINK = os.environ.get("SUPPORT_LINK", "https://t.me/YourSupportGroup")

    SHORTENER_URL = os.environ.get("SHORTENER_URL", "") 
    SHORTENER_API = os.environ.get("SHORTENER_API", "")
    VERIFY_EXPIRE = int(os.environ.get("VERIFY_EXPIRE", 86400))
    TUTORIAL_LINK = os.environ.get("TUTORIAL_LINK", "") 
    
    VERIFY_IMG = os.environ.get("VERIFY_IMG", "https://graph.org/file/341251a37c040d2eb2ec0.jpg") 
    PREMIUM_LINK = os.environ.get("PREMIUM_LINK", "https://t.me/koreandrama006") 
    
    # 🚀 Standalone Web Guard Settings
    GUARD_URL = os.environ.get("GUARD_URL", "https://luxeguard.souravbosu947.workers.dev")
    GUARD_SECRET = os.environ.get("GUARD_SECRET", "Luxe_Super_Secret_Guard_2026")
   
    # 🚀 NEW: ULTRA PREMIUM MENU LINKS
    UPDATES_LINK = os.environ.get("UPDATES_LINK", "https://t.me/LuxeFlix")
    MOVIES_LINK = os.environ.get("MOVIES_LINK", "https://t.me/moviefileshd1")
    SERIES_LINK = os.environ.get("SERIES_LINK", "https://t.me/")
    DEVELOPER_LINK = os.environ.get("DEVELOPER_LINK", "https://t.me/luxebotupdate")
    OWNER_LINK = os.environ.get("OWNER_LINK", "https://t.me/koreandrama006")
    
    # আপনার ছবির লিংক (যদি আগে না দিয়ে থাকেন)
    START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/your-image.jpg")

