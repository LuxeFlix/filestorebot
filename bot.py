import threading
import asyncio
import uvloop
from pyrogram import Client
from config import Config
from server import keep_alive
from utils.database import db

# 🚀 Uvloop: The Ultimate CPU & RAM Engine 
# এটি পাইথনের ডিফল্ট লুপকে রিপ্লেস করে C-লেভেলের স্পিড দেবে
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

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

# 🚀 Mach 2.5 Speed Database Indexing & TTL Cleaner
async def setup_indexes():
    try:
        await db.files_col1.create_index([("_id", 1)])
        if db.files_col2:
            await db.files_col2.create_index([("_id", 1)])
        if db.files_col3:
            await db.files_col3.create_index([("_id", 1)])
            
        # 🚀 MongoDB TTL Index (২৪ ঘণ্টা পর verify_tokens অটোমেটিক ডিলিট হবে, স্টোরেজ বাঁচবে)
        await db.tokens_col.create_index("createdAt", expireAfterSeconds=86400)
        
        print("⚡ MongoDB Auto-Indexing & TTL Complete! Ready for supersonic search.")
    except Exception as e:
        print(f"Indexing Error: {e}")

if __name__ == "__main__":
    print("🌐 Starting Ultra-Fast aiohttp Web Server with Uvloop...")
    threading.Thread(target=keep_alive, daemon=True).start()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_indexes())
    
    print("🚀 Advanced Bot is Starting with Kurigram!")
    app.run()
