import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from config import Config
from utils.database import db
from script import Script

def generate_premium_text(settings):
    plans = settings.get('premium_plans', {})
    text = "<blockquote>\n💎 <b>ᴘʀᴇᴍɪᴜᴍ sᴜʙsᴄʀɪᴘᴛɪᴏɴ</b>\n\n"
    for k, v in plans.items():
        limit_text = f"({v['limit']} ғʀᴇᴇ ʟɪɴᴋs / ᴅᴀʏ)" if v['limit'] > 0 else "(ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss)"
        text += f"• <b>{v['name']} :</b> {v['price']} ᴛᴋ {limit_text}\n"
    text += "</blockquote>"
    return text

@Client.on_callback_query(filters.regex("^show_premium_plans$"))
async def show_premium_plans_cb(client: Client, query: CallbackQuery):
    settings = await db.get_settings()
    text = generate_premium_text(settings)
    
    keyboard = [
        # 🚀 NEW: Buy Now Button
        [InlineKeyboardButton(Script.BTN_BUY_NOW, callback_data="buy_premium_menu")],
        [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close_settings")]
    ]
    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
    await query.answer()

@Client.on_message(filters.command(["plan", "premium"]))
async def plan_command(client: Client, message: Message):
    settings = await db.get_settings()
    text = generate_premium_text(settings)
    
    keyboard = [
        [InlineKeyboardButton(Script.BTN_BUY_NOW, callback_data="buy_premium_menu")],
        [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close_settings")]
    ]
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)

# 🚀 NEW: Dynamic Buy Menu Handler
@Client.on_callback_query(filters.regex("^buy_premium_menu$"))
async def buy_premium_cb(client: Client, query: CallbackQuery):
    settings = await db.get_settings()
    keyboard = []
    row = []
    
    owner_link = settings.get('owner_link', '')
    group_link = settings.get('group_link', '')
    
    if owner_link: row.append(InlineKeyboardButton(Script.BTN_OWNER, url=owner_link))
    if group_link: row.append(InlineKeyboardButton(Script.BTN_GROUP, url=group_link))
    if row: keyboard.append(row)
        
    keyboard.append([InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="show_premium_plans")])
    await query.message.edit_text(Script.BUY_PREMIUM_MSG, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)

@Client.on_message(filters.command("buy"))
async def buy_command(client: Client, message: Message):
    settings = await db.get_settings()
    keyboard = []
    row = []
    
    owner_link = settings.get('owner_link', '')
    group_link = settings.get('group_link', '')
    
    if owner_link: row.append(InlineKeyboardButton(Script.BTN_OWNER, url=owner_link))
    if group_link: row.append(InlineKeyboardButton(Script.BTN_GROUP, url=group_link))
    if row: keyboard.append(row)
        
    keyboard.append([InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close_settings")])
    await message.reply_text(Script.BUY_PREMIUM_MSG, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)

# ================= ADMIN CONTROLS =================

@Client.on_message(filters.command("set_owner_link") & filters.private)
async def set_owner_link(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID: return
    if len(message.command) < 2:
        return await message.reply_text("❌ `/set_owner_link https://t.me/your_id`")
    link = message.command[1]
    if link.lower() == "off": link = ""
    await db.update_settings('owner_link', link)
    await message.reply_text(f"✅ Owner Link Updated: {link}")

@Client.on_message(filters.command("set_group_link") & filters.private)
async def set_group_link(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID: return
    if len(message.command) < 2:
        return await message.reply_text("❌ `/set_group_link https://t.me/your_group`")
    link = message.command[1]
    if link.lower() == "off": link = ""
    await db.update_settings('group_link', link)
    await message.reply_text(f"✅ Group Link Updated: {link}")

@Client.on_message(filters.command("set_free_limit") & filters.private)
async def set_free_limit_cmd(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID: return
    if len(message.command) < 2:
        return await message.reply_text("❌ `/set_free_limit 5` (To give 5 free files/day to all users. Use 0 to disable)")
    try:
        limit = int(message.command[1])
        await db.update_settings('free_daily_limit', limit)
        await message.reply_text(f"✅ Daily Free Limit for all users set to: {limit}")
    except:
        await message.reply_text("❌ Limit must be a number!")

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
