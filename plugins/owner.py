from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from utils.database import db
from script import Script

@Client.on_message(filters.command("add_admin") & filters.private)
async def add_new_admin(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID:
        return await message.reply_text("⚠️ **Warning:** আপনি বটের ওনার নন! শুধুমাত্র ওনার নতুন অ্যাডমিন যুক্ত করতে পারেন।")

    if len(message.command) < 2:
        return await message.reply_text("❌ **সঠিক নিয়ম:** `/add_admin UserID`")
        
    try:
        user_id = int(message.command[1])
        success = await db.add_admin(user_id)
        if success:
            await message.reply_text(f"✅ **নতুন অ্যাডমিন যুক্ত করা হয়েছে:** `{user_id}`")
        else:
            await message.reply_text("⚠️ **এই ইউজার আগে থেকেই অ্যাডমিন!**")
    except ValueError:
        await message.reply_text("❌ ইউজার আইডি অবশ্যই সংখ্যা হতে হবে!")

@Client.on_message(filters.command("del_admin") & filters.private)
async def remove_admin_user(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID:
        return await message.reply_text("⚠️ **Warning:** আপনি বটের ওনার নন! শুধুমাত্র ওনার অ্যাডমিন রিমুভ করতে পারেন।")

    if len(message.command) < 2:
        return await message.reply_text("❌ **সঠিক নিয়ম:** `/del_admin UserID`")
        
    try:
        user_id = int(message.command[1])
        await db.remove_admin(user_id)
        await message.reply_text(f"🗑 **অ্যাডমিন রিমুভ করা হয়েছে:** `{user_id}`")
    except ValueError:
        await message.reply_text("❌ ইউজার আইডি অবশ্যই সংখ্যা হতে হবে!")

@Client.on_message(filters.command("mode") & filters.private)
async def toggle_bot_mode(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID:
        return await message.reply_text("⚠️ **Warning:** আপনি বটের ওনার নন! শুধুমাত্র ওনার বটের পাবলিক/প্রাইভেট মোড পরিবর্তন করতে পারেন।")

    if len(message.command) < 2 or message.command[1].lower() not in ['public', 'private']:
        return await message.reply_text("❌ **সঠিক নিয়ম:** `/mode public` অথবা `/mode private`")
        
    new_mode = message.command[1].lower()
    await db.update_settings('mode', new_mode)
    
    if new_mode == 'private':
        await message.reply_text("🔒 **Bot is now PRIVATE!**\nসাধারণ ইউজাররা আর কোনো ফাইল নিতে পারবে না।")
    else:
        await message.reply_text("🔓 **Bot is now PUBLIC!**\nসবাই বট থেকে ফাইল নিতে পারবে।")

@Client.on_message(filters.command("add_fsub") & filters.private)
async def add_fsub_channel(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(Script.NOT_OWNER_WARN)
        
    if len(message.command) < 2:
        return await message.reply_text("❌ **সঠিক নিয়ম:** `/add_fsub -100xxxxxxx`")
        
    try:
        chat_id = int(message.command[1])
        fsubs = await db.get_fsub_channels()
        if len(fsubs) >= 6:
            return await message.reply_text("❌ **আপনি সর্বোচ্চ ৬টি FSub চ্যানেল যুক্ত করতে পারবেন!**")
            
        await db.add_fsub_channel(chat_id)
        await message.reply_text(f"✅ **Force Subscribe Channel Added:** `{chat_id}`")
    except ValueError:
        await message.reply_text("❌ চ্যানেল আইডি অবশ্যই সংখ্যা হতে হবে!")

@Client.on_message(filters.command("del_fsub") & filters.private)
async def remove_fsub_channel(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(Script.NOT_OWNER_WARN)
        
    if len(message.command) < 2:
        return await message.reply_text("❌ **সঠিক নিয়ম:** `/del_fsub -100xxxxxxx`")
        
    try:
        chat_id = int(message.command[1])
        await db.remove_fsub_channel(chat_id)
        await message.reply_text(f"🗑 **Force Subscribe Channel Removed:** `{chat_id}`")
    except ValueError:
        await message.reply_text("❌ চ্যানেল আইডি অবশ্যই সংখ্যা হতে হবে!")

@Client.on_message(filters.command("fsub_list") & filters.private)
async def list_fsub_channels(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID: return
    
    fsubs = await db.get_fsub_channels()
    if not fsubs:
        return await message.reply_text("⚠️ **কোনো FSub চ্যানেল সেট করা নেই!**")
        
    text = "📌 **আপনার বর্তমান FSub চ্যানেলগুলো:**\n\n"
    for idx, chat_id in enumerate(fsubs, start=1):
        text += f"{idx}. `{chat_id}`\n"
    await message.reply_text(text)

@Client.on_message(filters.command("req_fsub") & filters.private)
async def toggle_req_fsub(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(Script.NOT_OWNER_WARN)

    if len(message.command) < 2 or message.command[1].lower() not in ['on', 'off']:
        return await message.reply_text("❌ **সঠিক নিয়ম:** `/req_fsub on` অথবা `/req_fsub off`")
        
    status = True if message.command[1].lower() == 'on' else False
    await db.update_settings('req_fsub', status)
    
    if status:
        await message.reply_text("✅ **Request to Join (Admin Approval) is now ON!**\nইউজারদের জয়েন রিকোয়েস্ট পাঠাতে হবে।")
    else:
        await message.reply_text("❌ **Request to Join is now OFF!**\nইউজাররা সরাসরি জয়েন করতে পারবে।")

# 🚀 SECURE UPDATE: /set_delete command properly configured with script.py
@Client.on_message(filters.command(["auto_delete", "set_delete"]) & filters.private)
async def toggle_auto_delete(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(Script.NOT_OWNER_WARN)

    if len(message.command) < 2:
        return await message.reply_text(Script.SET_DELETE_USAGE)
        
    arg = message.command[1].lower()
    if arg == 'off':
        await db.update_settings('auto_delete', 0)
        await message.reply_text(Script.SET_DELETE_OFF)
    elif arg.isdigit():
        mins = int(arg)
        await db.update_settings('auto_delete', mins)
        await message.reply_text(Script.SET_DELETE_ON.format(mins=mins))
    else:
        await message.reply_text(Script.SET_DELETE_USAGE)
