import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from config import Config
from utils.database import db

# 🚀 FIX: Clean Small Caps 
def generate_premium_text(settings):
    plans = settings.get('premium_plans', {})
    text = "<blockquote>\n💎 <b>ᴘʀᴇᴍɪᴜᴍ sᴜʙsᴄʀɪᴘᴛɪᴏɴ</b>\n\n"
    for k, v in plans.items():
        limit_text = f"({v['limit']} ғʀᴇᴇ ʟɪɴᴋs / ᴅᴀʏ)" if v['limit'] > 0 else "(ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss)"
        text += f"• <b>{v['name']} :</b> {v['price']} ᴛᴋ {limit_text}\n"
    
    pay_info = settings.get('payment_info', 'Contact Admin')
    text += f"\n<i>💳 ᴘᴀʏᴍᴇɴᴛ ɪɴғᴏ :</i>\n{pay_info}\n</blockquote>"
    return text

@Client.on_callback_query(filters.regex("^show_premium_plans$"))
async def show_premium_plans_cb(client: Client, query: CallbackQuery):
    settings = await db.get_settings()
    text = generate_premium_text(settings)
    
    keyboard = [
        [InlineKeyboardButton("👤 ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ", url=Config.SUPPORT_LINK if Config.SUPPORT_LINK else f"https://t.me/koreandrama006")],
        [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close_settings")]
    ]
    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
    await query.answer()

@Client.on_message(filters.command(["plan", "premium", "buy"]))
async def plan_command(client: Client, message: Message):
    settings = await db.get_settings()
    text = generate_premium_text(settings)
    
    keyboard = [
        [InlineKeyboardButton("👤 ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ", url=Config.SUPPORT_LINK if Config.SUPPORT_LINK else f"https://t.me/koreandrama006")],
        [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close_settings")]
    ]
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)

@Client.on_message(filters.command("set_pay") & filters.private)
async def set_payment_info(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID: return
    if len(message.command) < 2:
        return await message.reply_text("❌ <b>sʏɴᴛᴀx :</b> `/set_pay Bkash: 017... Send Screenshot`", parse_mode=ParseMode.HTML)
        
    new_info = message.text.split(None, 1)[1]
    await db.update_settings('payment_info', new_info)
    await message.reply_text("✅ <b>ᴘᴀʏᴍᴇɴᴛ ɪɴғᴏ ᴜᴘᴅᴀᴛᴇᴅ !</b>", parse_mode=ParseMode.HTML)

@Client.on_message(filters.command("add_prem") & filters.private)
async def add_premium_cmd(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID: return
    parts = message.command
    if len(parts) < 3:
        return await message.reply_text("❌ <b>sʏɴᴛᴀx :</b> `/add_prem <user_id> <days> <daily_limit_number>`\n<i>(Use 0 for Unlimited)</i>\n\nExample: `/add_prem 12345 7 5`", parse_mode=ParseMode.HTML)
        
    try:
        user_id = int(parts[1])
        days = int(parts[2])
        limit = int(parts[3]) if len(parts) > 3 else 0
        
        time_seconds = days * 24 * 60 * 60
        await db.add_premium(user_id, time_seconds, limit)
        
        await message.reply_text(f"✅ <b>ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ !</b>\n\n👤 User: `{user_id}`\n⏳ Days: {days}\n📈 Daily Limit: {limit if limit > 0 else 'Unlimited'}", parse_mode=ParseMode.HTML)
        
        try:
            await client.send_message(user_id, f"🎉 <b>Cᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs!</b>\n\nYour Premium Subscription has been activated for {days} days!\nEnjoy seamless downloading.", parse_mode=ParseMode.HTML)
        except:
            pass
    except ValueError:
        await message.reply_text("❌ ID and Days must be numbers!")

@Client.on_message(filters.command("del_prem") & filters.private)
async def del_premium_cmd(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID: return
    if len(message.command) < 2:
        return await message.reply_text("❌ <b>sʏɴᴛᴀx :</b> `/del_prem <user_id>`", parse_mode=ParseMode.HTML)
        
    try:
        user_id = int(message.command[1])
        await db.remove_premium(user_id)
        await message.reply_text(f"🗑 <b>ᴘʀᴇᴍɪᴜᴍ ʀᴇᴍᴏᴠᴇᴅ !</b>\n👤 User: `{user_id}`", parse_mode=ParseMode.HTML)
    except ValueError:
        pass
