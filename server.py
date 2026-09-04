import os
import asyncio
from aiohttp import web

async def home(request):
    return web.Response(text="✅ Telegram Bot is running successfully with Ultra-Fast aiohttp Server!", content_type="text/plain")

def keep_alive():
    # 🚀 SUPERSONIC UPDATE: Flask রিমুভ করে aiohttp.web যুক্ত করা হয়েছে
    # এটি ব্যাকগ্রাউন্ড থ্রেডে একটি নতুন ইভেন্ট লুপ তৈরি করে চলবে
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    app = web.Application()
    app.router.add_get('/', home)
    
    port = int(os.environ.get("PORT", 8080))
    
    # AppRunner ব্যবহার করে মেইন টেলিগ্রাম বট লুপকে ডিস্টার্ব না করে সার্ভার রান হবে
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, host='0.0.0.0', port=port)
    loop.run_until_complete(site.start())
    
    # ওয়েব সার্ভারটি লাইভ রাখার জন্য
    loop.run_forever()

