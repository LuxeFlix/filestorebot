from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from config import Config
from utils.database import db
from script import Script

def get_settings_keyboard(settings):
    sl_status = "🟢 ON" if settings.get('shortlink_status') else "🔴 OFF"
    sl_type = "⏳ Time" if settings.get('shortlink_type') == 'time' else "💳 Credit"
    verify_time = settings.get('verify_duration', 24)
    bypass_cred = settings.get('bypass_credits', 3)
    bypass_time = settings.get('bypass_time', 15)
    
    # 🚀 Fetch Guard Status
    guard_status = "🟢 ON" if settings.get('web_guard', False) else "🔴 OFF"
    
    keyboard = [
        [InlineKeyboardButton(Script.BTN_SL_STATUS.format(status=sl_status), callback_data="set_sl_status"),
         InlineKeyboardButton(Script.BTN_SL_MODE.format(mode=sl_type), callback_data="set_sl_type")]
    ]
    
    if settings.get('shortlink_type') == 'time':
        keyboard.append([InlineKeyboardButton(Script.BTN_SL_TIME.format(time=verify_time), callback_data="set_sl_time")])
    else:
        keyboard.append([InlineKeyboardButton(Script.BTN_SL_CREDIT.format(creds=bypass_cred), callback_data="set_sl_cred")])
        
    keyboard.append([InlineKeyboardButton(Script.BTN_BYPASS_TIME.format(time=bypass_time), callback_data="set_bypass_time")])
    
    # 🚀 Add Web Guard Button
    keyboard.append([InlineKeyboardButton(Script.BTN_WEB_GUARD.format(status=guard_status), callback_data="set_web_guard")])
        
    keyboard.append([InlineKeyboardButton(Script.BTN_CLOSE_PANEL, callback_data="close_settings")])
    return InlineKeyboardMarkup(keyboard)

@Client.on_message(filters.command("settings") & filters.private)
async def settings_command(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID:
        return await message.reply_text(Script.NOT_OWNER_WARN)
        
    settings = await db.get_settings()
    await message.reply_text(Script.SETTINGS_MSG, reply_markup=get_settings_keyboard(settings))

@Client.on_callback_query(filters.regex(r"^set_sl_|^set_bypass_|^set_web_"))
async def settings_callbacks(client: Client, query: CallbackQuery):
    if query.from_user.id != Config.OWNER_ID:
        return await query.answer(Script.NOT_OWNER_ALERT, show_alert=True)
        
    settings = await db.get_settings()
    action = query.data
    
    if action == "set_sl_status":
        new_status = not settings.get('shortlink_status', False)
        await db.update_settings('shortlink_status', new_status)
        
    elif action == "set_sl_type":
        current_type = settings.get('shortlink_type', 'time')
        new_type = 'credit' if current_type == 'time' else 'time'
        await db.update_settings('shortlink_type', new_type)
        
    elif action == "set_sl_time":
        times = [1, 4, 8, 16, 24]
        current = settings.get('verify_duration', 24)
        next_idx = (times.index(current) + 1) % len(times) if current in times else 0
        await db.update_settings('verify_duration', times[next_idx])
        
    elif action == "set_sl_cred":
        creds = [1, 2, 3, 5, 10, 20]
        current = settings.get('bypass_credits', 3)
        next_idx = (creds.index(current) + 1) % len(creds) if current in creds else 0
        await db.update_settings('bypass_credits', creds[next_idx])
        
    elif action == "set_bypass_time":
        times = [0, 5, 10, 15, 20, 30, 45, 60]
        current = settings.get('bypass_time', 15)
        next_idx = (times.index(current) + 1) % len(times) if current in times else 0
        await db.update_settings('bypass_time', times[next_idx])
        
    # 🚀 Handle Web Guard Toggle
    elif action == "set_web_guard":
        new_status = not settings.get('web_guard', False)
        await db.update_settings('web_guard', new_status)
        
    updated_settings = await db.get_settings()
    await query.message.edit_reply_markup(get_settings_keyboard(updated_settings))
    await query.answer(Script.SETTINGS_UPDATED_ALERT)

@Client.on_callback_query(filters.regex("close_settings"))
async def close_settings(client: Client, query: CallbackQuery):
    if query.from_user.id != Config.OWNER_ID:
        return
    await query.message.delete()
