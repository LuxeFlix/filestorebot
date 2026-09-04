import threading
import asyncio
from pyrogram import Client
from config import Config
from server import keep_alive
from utils.database import db

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

# 🚀 Mach 2.5 Speed Database Indexing
async def setup_indexes():
    try:
        await db.files_col1.create_index([("_id", 1)])
        if db.files_col2:
            await db.files_col2.create_index([("_id", 1)])
        if db.files_col3:
            await db.files_col3.create_index([("_id", 1)])
        print("⚡ MongoDB Auto-Indexing Complete! Ready for supersonic search.")
    except Exception as e:
        print(f"Indexing Error: {e}")

if __name__ == "__main__":
    print("🌐 Starting Ultra-Fast aiohttp Web Server...")
    threading.Thread(target=keep_alive, daemon=True).start()
    
    # ইনডেক্সিং প্রসেস লুপে এড করা হলো
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_indexes())
    
    print("🚀 Advanced Bot is Starting with Kurigram!")
    app.run()
