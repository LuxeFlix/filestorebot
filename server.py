from flask import Flask
import os

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "✅ Telegram Bot is running successfully on Back4App!"

def keep_alive():
    # Back4app ডিফল্টভাবে যে পোর্ট দেয় সেটি নেবে, না পেলে 8080 ব্যবহার করবে
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)
