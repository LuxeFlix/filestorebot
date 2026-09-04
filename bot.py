import threading
from pyrogram import Client
from config import Config
from server import keep_alive

plugins = dict(root="plugins")

app = Client(
    "AdvancedFileStore",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=plugins,
    sleep_threshold=30,
    max_concurrent_transmissions=5
)

if __name__ == "__main__":
    print("🌐 Starting Web Server for Health Check...")
    threading.Thread(target=keep_alive, daemon=True).start()
    
    print("🚀 Advanced Bot is Starting with Kurigram!")
    app.run()
