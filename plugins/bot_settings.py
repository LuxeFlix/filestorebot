from pyrogram import Client, filters
from pyrogram.types import Message
from utils.database import db

@Client.on_message(filters.command(["set_db", "set_log"]) & filters.private)
async def settings_commands(client: Client, message: Message):
    if not await db.is_admin(message.from_user.id):
        return # 🚀 SILENT IGNORE (কোনো ওয়ার্নিং মেসেজ দেবে না)

    command = message.command[0]
    
    if len(message.command) < 2:
        await message.reply_text(f"❌ **সঠিক নিয়ম:** `/{command} -100xxxxxxx`")
        return
        
    try:
        channel_id = int(message.command[1])
        if command == "set_db":
            await db.update_settings('active_db', channel_id)
            await message.reply_text(f"✅ **Primary Database Channel সেট করা হয়েছে:** `{channel_id}`")
        elif command == "set_log":
            await db.update_settings('log_channel', channel_id)
            await message.reply_text(f"✅ **Log Channel সেট করা হয়েছে:** `{channel_id}`")
    except ValueError:
        await message.reply_text("❌ চ্যানেল আইডি অবশ্যই সংখ্যা হতে হবে!")
