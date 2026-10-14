import re
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, LinkPreviewOptions
from pyrogram.errors import FloodWait
from config import Config
from utils.database import db
from script import Script

BATCH_STATE = {}

def get_correct_chat_id(chat_id):
    if not chat_id: return chat_id
    try:
        chat_id_str = str(chat_id).strip()
        if chat_id_str.startswith("-100"): return int(chat_id_str)
        if chat_id_str.startswith("-"): return int(f"-100{chat_id_str[1:]}")
        return int(f"-100{chat_id_str}")
    except Exception: return chat_id

def get_file_info(message):
    try:
        media = message.document or message.video or message.audio or message.photo or message.animation or message.sticker or message.voice
        if media:
            f_id = media.file_id if not isinstance(media, list) else media[-1].file_id
            cap = message.caption.html if message.caption else ""
            return f_id, getattr(media, "file_unique_id", None), cap
    except Exception: pass
    text_content = message.text.html if message.text else ""
    return None, None, text_content

def extract_chat_and_msg_id(message: Message, default_db: int):
    # 1. Check Kurigram forward_origin (No deprecation warning)
    if getattr(message, "forward_origin", None):
        origin = message.forward_origin
        msg_id = getattr(origin, "message_id", None)
        chat = getattr(origin, "chat", None)
        chat_id = chat.id if chat else default_db
        if msg_id:
            return get_correct_chat_id(chat_id), msg_id

    # 2. Extract both Channel ID and Message ID from Telegram Link
    if message.text:
        private_match = re.search(r"t\.me/c/(\d+)/(\d+)", message.text)
        if private_match:
            c_id = get_correct_chat_id(private_match.group(1))
            m_id = int(private_match.group(2))
            return c_id, m_id
            
        public_match = re.search(r"t\.me/([a-zA-Z0-9_]+)/(\d+)", message.text)
        if public_match:
            return default_db, int(public_match.group(2))
            
    return default_db, None

@Client.on_message(filters.command("batch") & filters.private)
async def start_batch_command(client: Client, message: Message):
    user_id = message.from_user.id
    if not await db.is_admin(user_id):
        return
    
    settings = await db.get_settings()
    if not settings.get('active_db'):
        return await message.reply_text(Script.NO_DB_SET)
        
    BATCH_STATE[user_id] = {'step': 1}
    await message.reply_text(Script.BATCH_START)

@Client.on_message(filters.command("cancel") & filters.private)
async def cancel_batch(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in BATCH_STATE:
        del BATCH_STATE[user_id]
        await message.reply_text(Script.BATCH_CANCEL)

ALL_COMMANDS = ["start", "set_db", "set_log", "add_admin", "del_admin", "mode", "batch", "cancel", "add_fsub", "del_fsub", "fsub_list", "req_fsub", "auto_delete", "set_delete", "stats", "broadcast", "dbroadcast", "ban", "unban", "unban_all", "settings", "add_credit", "remove_credit", "shortlink", "set_shortlink", "set_tutorial", "plan", "premium", "buy", "set_pay", "add_prem", "del_prem", "set_owner_link", "set_group_link", "set_free_limit", "status", "delete", "index_links"]

@Client.on_message(filters.private & ~filters.command(ALL_COMMANDS))
async def message_handler(client: Client, message: Message):
    user_id = message.from_user.id
        
    if await db.is_banned(user_id):
        support_btn = InlineKeyboardMarkup([[InlineKeyboardButton(Script.BTN_CONTACT_SUPPORT, url=Config.SUPPORT_LINK)]]) if Config.SUPPORT_LINK else None
        return await message.reply_text(Script.BANNED_MSG, reply_markup=support_btn)

    if message.text and message.text.startswith("/"):
        return

    is_admin = await db.is_admin(user_id)
    if not is_admin:
        return

    settings = await db.get_settings()
    active_db = get_correct_chat_id(settings.get('active_db'))
    if not active_db:
        return await message.reply_text(Script.NO_DB_SET)

    if user_id in BATCH_STATE:
        target_chat_id, msg_id = extract_chat_and_msg_id(message, active_db)
        if not msg_id:
            return await message.reply_text(Script.WRONG_MSG_LINK)
            
        step = BATCH_STATE[user_id]['step']
        if step == 1:
            BATCH_STATE[user_id] = {'step': 2, 'first_id': msg_id, 'chat_id': target_chat_id}
            await message.reply_text(Script.BATCH_STEP_2.format(msg_id=msg_id))
        elif step == 2:
            first_id = BATCH_STATE[user_id]['first_id']
            batch_chat_id = BATCH_STATE[user_id].get('chat_id', target_chat_id)
            last_id = msg_id
            if first_id > last_id:
                first_id, last_id = last_id, first_id 
                
            wait_msg = await message.reply_text("⏳ **Generating Permanent Batch Link...**\n*(Scanning all files to save globally...)*")
            try:
                files_data = []
                last_error = None
                for m_id in range(first_id, last_id + 1):
                    try:
                        db_msg = await client.get_messages(batch_chat_id, m_id)
                        if db_msg and not getattr(db_msg, "empty", True):
                            f_id, f_uniq, cap = get_file_info(db_msg)
                            f_data = {}
                            if f_id: f_data['f'] = f_id
                            if cap: f_data['cap'] = cap
                            f_data['m'] = m_id
                            if f_id or cap:
                                files_data.append(f_data)
                    except FloodWait as e:
                        await asyncio.sleep(e.value + 1)
                        db_msg = await client.get_messages(batch_chat_id, m_id)
                        if db_msg and not getattr(db_msg, "empty", True):
                            f_id, f_uniq, cap = get_file_info(db_msg)
                            f_data = {}
                            if f_id: f_data['f'] = f_id
                            if cap: f_data['cap'] = cap
                            f_data['m'] = m_id
                            if f_id or cap:
                                files_data.append(f_data)
                    except Exception as err:
                        last_error = err
                    await asyncio.sleep(0.3)

                if not files_data:
                    err_detail = f"\n`{last_error}`" if last_error else ""
                    return await wait_msg.edit_text(
                        f"❌ **চ্যানেল (`{batch_chat_id}`) থেকে কোনো ফাইল পাওয়া যায়নি!**{err_detail}\n\n"
                        f"👉 বটকে ওই চ্যানেলে **Admin** করা আছে কি না চেক করুন এবং চ্যানেলে একটি নতুন মেসেজ পাঠিয়ে আবার চেষ্টা করুন।"
                    )

                unique_id = await db.save_batch(files_data=files_data, chat_id=batch_chat_id)
                if not unique_id:
                    return await wait_msg.edit_text("❌ **Database save failed. Please try again.**")
                
                custom_link = f"{Config.CUSTOM_DOMAIN}?start={unique_id}"
                total_files = len(files_data)
                reply_text = Script.BATCH_SUCCESS_LINK.format(total_files=total_files, custom_link=custom_link)
                buttons = InlineKeyboardMarkup([[InlineKeyboardButton(Script.BTN_ORIGINAL_LINK, url=custom_link, style="success")]])
                await wait_msg.edit_text(reply_text, reply_markup=buttons, link_preview_options=LinkPreviewOptions(is_disabled=True))
                
                log_channel = settings.get('log_channel')
                if log_channel:
                    try:
                        await client.send_message(log_channel, Script.LOG_BATCH_LINK.format(mention=message.from_user.mention, total_files=total_files, custom_link=custom_link))
                    except Exception:
                        pass
            except Exception as e:
                await wait_msg.edit_text(Script.ERROR_MSG.format(error=e))
            finally:
                del BATCH_STATE[user_id]
        return

    file_id, file_unique_id, caption = get_file_info(message)
    if not file_id:
        target_chat_id, db_msg_id = extract_chat_and_msg_id(message, active_db)
        if db_msg_id:
            # 🚀 FIX: Removed reply_to_message_id, replaced with quote=True
            wait_msg = await message.reply_text(Script.GEN_DB_LINK_WAIT, quote=True)
            try:
                db_msg = await client.get_messages(target_chat_id, db_msg_id)
                if not db_msg or getattr(db_msg, "empty", True):
                    return await wait_msg.edit_text(f"❌ **চ্যানেল (`{target_chat_id}`) এ মেসেজটি পাওয়া যায়নি!**")
                f_id, f_uniq, cap = get_file_info(db_msg)
            except Exception as e:
                return await wait_msg.edit_text(f"❌ **চ্যানেল থেকে ফাইল রিড করা যায়নি:** `{e}`")
                
            unique_id = await db.save_file(db_msg_id, target_chat_id, f_id, f_uniq, cap)
            if not unique_id:
                return await wait_msg.edit_text("❌ **Database save failed. Please try again.**")
                
            custom_link = f"{Config.CUSTOM_DOMAIN}?start={unique_id}"
            reply_text = Script.SINGLE_SUCCESS_LINK.format(custom_link=custom_link)
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton(Script.BTN_ORIGINAL_LINK, url=custom_link, style="success")]])
            await wait_msg.edit_text(reply_text, reply_markup=buttons, link_preview_options=LinkPreviewOptions(is_disabled=True))
            
            log_channel = settings.get('log_channel')
            if log_channel:
                try:
                    await client.send_message(log_channel, Script.LOG_SINGLE_LINK.format(mention=message.from_user.mention, custom_link=custom_link))
                except Exception:
                    pass
        return
        
    # 🚀 FIX: Removed reply_to_message_id, replaced with quote=True
    wait_msg = await message.reply_text(Script.GEN_LINK_WAIT, quote=True)
    existing_file = await db.check_file_exists(file_unique_id)
    if existing_file:
        custom_link = f"{Config.CUSTOM_DOMAIN}?start={existing_file['_id']}"
        reply_text = Script.FILE_EXISTS.format(custom_link=custom_link)
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton(Script.BTN_ORIGINAL_LINK, url=custom_link, style="success")]])
        await wait_msg.edit_text(reply_text, reply_markup=buttons, link_preview_options=LinkPreviewOptions(is_disabled=True))
        return

    buttons = InlineKeyboardMarkup([[InlineKeyboardButton(Script.BTN_GENERATE_LINK, callback_data=f"single_{message.id}", style="primary")]])
    await wait_msg.edit_text(Script.GEN_PERMANENT_WAIT, reply_markup=buttons)

@Client.on_callback_query(filters.regex(r"^single_"))
async def generate_single_link(client: Client, query):
    msg_id = int(query.data.split("_")[1])
    original_msg = await client.get_messages(query.message.chat.id, msg_id)
    settings = await db.get_settings()
    active_db = get_correct_chat_id(settings.get('active_db'))
    
    wait_msg = await query.message.edit_text(Script.PROCESSING_FILE)
    
    try:
        file_id, file_unique_id, caption = get_file_info(original_msg)
        
        final_msg_id = None
        forward_chat_id = None
        
        if getattr(original_msg, "forward_origin", None):
            origin = original_msg.forward_origin
            if getattr(origin, "chat", None):
                forward_chat_id = origin.chat.id
            if forward_chat_id and forward_chat_id == active_db:
                final_msg_id = getattr(origin, "message_id", None)
        
        if not final_msg_id:
            copied_msg = await original_msg.copy(chat_id=active_db)
            final_msg_id = copied_msg.id
            
        unique_id = await db.save_file(final_msg_id, active_db, file_id, file_unique_id, caption)
        if not unique_id:
            return await wait_msg.edit_text("❌ **Database save failed. Please try again.**")
            
        custom_link = f"{Config.CUSTOM_DOMAIN}?start={unique_id}"
        reply_text = Script.SAVED_IN_DB.format(custom_link=custom_link)
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton(Script.BTN_ORIGINAL_LINK, url=custom_link, style="success")]])
        await wait_msg.edit_text(reply_text, reply_markup=buttons, link_preview_options=LinkPreviewOptions(is_disabled=True))
        
        log_channel = settings.get('log_channel')
        if log_channel:
            try:
                await client.send_message(log_channel, Script.LOG_SINGLE_LINK.format(mention=query.from_user.mention, custom_link=custom_link))
            except Exception:
                pass
                
    except Exception as e:
        await wait_msg.edit_text(Script.ERROR_MSG.format(error=e))
