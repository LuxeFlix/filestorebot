import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import FloodWait, ChannelInvalid, ChannelPrivate, ChatAdminRequired
from pyrogram.enums import ParseMode
from config import Config
from utils.database import db
from utils.fsub_helper import check_fsub, get_fsub_keyboard
from utils.shortener import get_shortlink
from utils.shortlink_guard import ShortlinkGuard
from script import Script

def clean_url(url: str) -> str:
    if not url: return ""
    url = url.strip("<>[]()\"' ")
    if not url: return ""
    if url.startswith("t.me/"): return "https://" + url
    if not (url.startswith("http://") or url.startswith("https://") or url.startswith("tg://")):
        return "https://" + url
    return url

def format_caption(original_caption: str) -> str:
    if original_caption:
        return f"{original_caption}{Script.BRANDING_TAG}"
    return Script.BRANDING_TAG.strip()

async def delete_after_delay(client, chat_id, message_ids, delay):
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id, message_ids)
        await client.send_message(chat_id, Script.AUTO_DELETE_DONE)
    except Exception:
        pass

async def deliver_file(client: Client, chat_id: int, payload: str, reply_to_msg=None):
    unique_id = payload.replace(Config.CUSTOM_PREFIX, "") if payload.startswith(Config.CUSTOM_PREFIX) else payload
        
    try:
        file_data = await db.get_file(unique_id)
        if not file_data:
            if reply_to_msg:
                await reply_to_msg.reply_text(Script.INVALID_LINK)
            else:
                await client.send_message(chat_id, Script.INVALID_LINK)
            return

        sent_msg_ids = []
        settings = await db.get_settings()
        auto_delete_time = settings.get('auto_delete', 0)

        if file_data.get('t') == 'b':
            db_chat_id = file_data['c']
            first_id = file_data['f_id']
            last_id = file_data['l_id']
            total_files = (last_id - first_id) + 1
            
            wait_text = Script.BATCH_SENDING.format(total_files=total_files)
            if reply_to_msg:
                wait_msg = await reply_to_msg.reply_text(wait_text)
            else:
                wait_msg = await client.send_message(chat_id, wait_text)
                
            for msg_id in range(first_id, last_id + 1):
                db_msg = None
                final_cap = ""
                sent_m = None
                try:
                    db_msg = await client.get_messages(db_chat_id, msg_id)
                    if db_msg and not getattr(db_msg, "empty", True):
                        if db_msg.media:
                            orig_cap = db_msg.caption.html if db_msg.caption else ""
                            final_cap = format_caption(orig_cap)
                            sent_m = await client.copy_message(chat_id, db_chat_id, msg_id, caption=final_cap, parse_mode=ParseMode.HTML, protect_content=False)
                        else:
                            sent_m = await client.copy_message(chat_id, db_chat_id, msg_id, protect_content=False)
                    if sent_m: sent_msg_ids.append(sent_m.id)
                    await asyncio.sleep(0.15) 
                except FloodWait as e:
                    await asyncio.sleep(e.value + 1)
                    if db_msg and getattr(db_msg, "media", None):
                        sent_m = await client.copy_message(chat_id, db_chat_id, msg_id, caption=final_cap, parse_mode=ParseMode.HTML, protect_content=False)
                    elif db_msg:
                        sent_m = await client.copy_message(chat_id, db_chat_id, msg_id, protect_content=False)
                    if sent_m: sent_msg_ids.append(sent_m.id)
                except Exception:
                    pass 
            
            try:
                await wait_msg.delete()
            except Exception:
                pass
                
            if auto_delete_time > 0:
                success_msg = await client.send_message(chat_id, Script.BATCH_SUCCESS_WARN.format(auto_delete_time=auto_delete_time))
                sent_msg_ids.append(success_msg.id)
            else:
                await client.send_message(chat_id, Script.BATCH_SUCCESS)
                
        else:
            db_chat_id = file_data['c']
            msg_id = file_data['m']
            sent_m = None
            
            try:
                db_msg = await client.get_messages(db_chat_id, msg_id)
                if db_msg and not getattr(db_msg, "empty", True):
                    if db_msg.media:
                        orig_cap = db_msg.caption.html if db_msg.caption else ""
                        final_cap = format_caption(orig_cap)
                        sent_m = await client.copy_message(chat_id, db_chat_id, msg_id, caption=final_cap, parse_mode=ParseMode.HTML, protect_content=False)
                    else:
                        sent_m = await client.copy_message(chat_id, db_chat_id, msg_id, protect_content=False)
                else:
                    raise Exception("Message empty")
            except (ChannelInvalid, ChannelPrivate, ChatAdminRequired, Exception):
                if 'f' in file_data:
                    orig_cap = file_data.get('cap', '')
                    final_cap = format_caption(orig_cap)
                    try:
                        sent_m = await client.send_cached_media(chat_id, file_data['f'], caption=final_cap, parse_mode=ParseMode.HTML)
                    except Exception:
                        sent_m = await client.send_message(chat_id, Script.FILE_NOT_FOUND_SERVER)
                else:
                    sent_m = await client.send_message(chat_id, Script.MSG_NOT_FOUND_SERVER)
            
            if sent_m: 
                sent_msg_ids.append(sent_m.id)
                if auto_delete_time > 0:
                    warn_msg = await client.send_message(chat_id, Script.SINGLE_SUCCESS_WARN.format(auto_delete_time=auto_delete_time))
                    sent_msg_ids.append(warn_msg.id)

        if auto_delete_time > 0 and sent_msg_ids:
            asyncio.create_task(delete_after_delay(client, chat_id, sent_msg_ids, auto_delete_time * 60))
                    
    except Exception as e:
        await client.send_message(chat_id, Script.DELIVERY_ERROR)

async def handle_verification_check(client: Client, message: Message, user_id: int, payload: str, settings: dict):
    if await db.is_admin(user_id) or await db.is_premium(user_id):
        return False
        
    sl_type = settings.get('shortlink_type', 'time')
    needs_verify = False
    
    if sl_type == 'time':
        if not await db.is_user_verified(user_id, int(time.time())):
            needs_verify = True
    elif sl_type == 'credit':
        has_credit = await db.use_credit(user_id)
        if not has_credit:
            needs_verify = True

    if needs_verify:
        token = await db.create_verify_token(user_id, payload)
        bot_username = client.me.username if client.me else (await client.get_me()).username
        
        wait_msg = await message.reply_text(Script.GENERATING_SECURE_LINK)
        
        # 🚀 Web Guard Routing Logic
        is_guard_on = settings.get('web_guard', False)
        short_url = None
        
        if is_guard_on and Config.GUARD_URL:
            bypass_time = settings.get('bypass_time', 15)
            short_url = ShortlinkGuard.generate_cf_url(
                token=token,
                api_url=settings.get('shortener_url', ''),
                api_key=settings.get('shortener_api', ''),
                bot_username=bot_username,
                bypass_time=bypass_time
            )
            
        if not short_url:
            verify_url = f"https://t.me/{bot_username}?start=verify_{token}"
            raw_short_url = await get_shortlink(verify_url, settings.get('shortener_url'), settings.get('shortener_api'))
            short_url = clean_url(raw_short_url)
        
        verify_text = Script.VERIFY_REQUIRED_UI.format(mention=message.from_user.mention)
        
        btn_list = []
        tutorial_link = clean_url(settings.get('tutorial_link'))
        
        main_btns = []
        if short_url:
            main_btns.append(InlineKeyboardButton(Script.BTN_OPEN_LINK, url=short_url))
        if tutorial_link:
            main_btns.append(InlineKeyboardButton(Script.BTN_TUTORIAL, url=tutorial_link))
            
        if main_btns:
            btn_list.append(main_btns)
            
        premium_link = clean_url(Config.PREMIUM_LINK)
        if premium_link:
            btn_list.append([InlineKeyboardButton(Script.BTN_BUY_PREMIUM, url=premium_link)])
            
        btn = InlineKeyboardMarkup(btn_list)
        await wait_msg.delete()
        
        try:
            verify_img = clean_url(Config.VERIFY_IMG)
            if verify_img:
                await message.reply_photo(photo=verify_img, caption=verify_text, reply_markup=btn)
            else:
                await message.reply_text(verify_text, reply_markup=btn, disable_web_page_preview=True)
        except Exception:
            await message.reply_text(verify_text, reply_markup=btn, disable_web_page_preview=True)
            
        return True
        
    return False

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    
    if await db.is_banned(user_id):
        support_btn = []
        if Config.SUPPORT_LINK:
            support_btn.append([InlineKeyboardButton(Script.BTN_CONTACT_SUPPORT, url=clean_url(Config.SUPPORT_LINK))])
        reply_markup = InlineKeyboardMarkup(support_btn) if support_btn else None
        return await message.reply_text(Script.BANNED_MSG, reply_markup=reply_markup, quote=True)

    is_new_user = await db.add_user(user_id)
    settings = await db.get_settings()
    is_admin = await db.is_admin(user_id)
    
    log_channel = settings.get('log_channel')
    if is_new_user and log_channel:
        try:
            await client.send_message(
                log_channel, 
                Script.NEW_USER_LOG.format(mention=message.from_user.mention, user_id=user_id, text=message.text)
            )
        except Exception:
            pass

    if settings.get('mode') == 'private' and not is_admin:
        await message.reply_text(Script.PRIVATE_MODE_MSG, quote=True)
        return

    text = message.text
    payload = text.split()[1] if len(text.split()) > 1 else None
    
    if not is_admin: 
        missing_fsubs = await check_fsub(client, user_id)
        if missing_fsubs:
            keyboard = await get_fsub_keyboard(client, missing_fsubs, payload)
            await message.reply_text(Script.FSUB_WARNING, reply_markup=keyboard, quote=True)
            return

    if payload:
        # 🚀 STANDALONE WEB GUARD (Cryptographic Signature Checking)
        if payload.startswith("vpass_"):
            parts = payload.split("_")
            if len(parts) >= 3:
                token = parts[1]
                signature = parts[2]
                
                # 🚀 CHECK CRYPTOGRAPHIC SIGNATURE
                expected_signature = ShortlinkGuard.generate_signature(token)
                
                if signature == expected_signature:
                    token_data = await db.get_verify_token(token)
                    if token_data and token_data['user_id'] == user_id:
                        sl_type = settings.get('shortlink_type', 'time')
                        if sl_type == 'time':
                            duration = settings.get('verify_duration', 24)
                            expire_time = int(time.time()) + (duration * 3600)
                            await db.verify_user(user_id, expire_time)
                            success_msg = await message.reply_text(Script.VERIFY_SUCCESS_TIME.format(duration=duration))
                        else:
                            creds = settings.get('bypass_credits', 3)
                            await db.add_credits(user_id, creds)
                            success_msg = await message.reply_text(Script.VERIFY_SUCCESS_CREDIT.format(creds=creds))

                        await asyncio.sleep(1.5)
                        await deliver_file(client, message.chat.id, token_data['payload'], reply_to_msg=success_msg)
                    else:
                        return await message.reply_text(Script.VERIFY_INVALID)
                else:
                    # 🚀 Invalid Signature (Bypass Detected)
                    return await message.reply_text(Script.GUARD_BANNED)
            else:
                return await message.reply_text(Script.VERIFY_INVALID)
            return

        # 🚀 OLD VERIFY FLOW (Fallback)
        elif payload.startswith("verify_"):
            token = payload.split("_")[1]
            token_data = await db.get_verify_token(token)
            
            if token_data and token_data['user_id'] == user_id:
                bypass_time = settings.get('bypass_time', 15)
                time_taken = int(time.time()) - token_data.get('createdAt', 0)
                if bypass_time > 0 and time_taken < bypass_time:
                    return await message.reply_text(Script.BYPASS_DETECTED)
                
                sl_type = settings.get('shortlink_type', 'time')
                if sl_type == 'time':
                    duration = settings.get('verify_duration', 24)
                    expire_time = int(time.time()) + (duration * 3600)
                    await db.verify_user(user_id, expire_time)
                    success_msg = await message.reply_text(Script.VERIFY_SUCCESS_TIME.format(duration=duration))
                else:
                    creds = settings.get('bypass_credits', 3)
                    await db.add_credits(user_id, creds)
                    success_msg = await message.reply_text(Script.VERIFY_SUCCESS_CREDIT.format(creds=creds))

                await asyncio.sleep(1.5)
                await deliver_file(client, message.chat.id, token_data['payload'], reply_to_msg=success_msg)
            else:
                await message.reply_text(Script.VERIFY_INVALID)
            return

        # 🚀 NORMAL FILE REQUEST
        if settings.get('shortlink_status'):
            is_locked = await handle_verification_check(client, message, user_id, payload, settings)
            if is_locked: return

        await deliver_file(client, message.chat.id, payload, reply_to_msg=message)
        return

    welcome_text = Script.START_MSG.format(mention=message.from_user.mention)
    
    if await db.is_premium(user_id):
        welcome_text += Script.PREMIUM_USER_TAG
    elif settings.get('shortlink_status') and settings.get('shortlink_type') == 'credit' and not is_admin:
        creds = await db.get_credits(user_id)
        welcome_text += Script.CREDIT_TAG.format(creds=creds)
        
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton(Script.BTN_UPDATES_CHANNEL, url="https://t.me/koreandrama006", style="primary")]])
    await message.reply_text(welcome_text, reply_markup=buttons)

@Client.on_callback_query(filters.regex(r"^chkF_"))
async def check_fsub_callback(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    
    if await db.is_banned(user_id):
        support_btn = []
        if Config.SUPPORT_LINK:
            support_btn.append([InlineKeyboardButton(Script.BTN_CONTACT_SUPPORT, url=clean_url(Config.SUPPORT_LINK))])
        reply_markup = InlineKeyboardMarkup(support_btn) if support_btn else None
        await query.message.reply_text(Script.BANNED_CB_MSG, reply_markup=reply_markup)
        return await query.answer(Script.BANNED_CB_ALERT, show_alert=True)
        
    payload = query.data.split("_", 1)[1]
    missing_fsubs = await check_fsub(client, user_id)
    
    if missing_fsubs:
        await query.answer(Script.FSUB_NOT_JOINED_ALERT, show_alert=True)
        return
        
    await query.answer(Script.FSUB_JOINED_ALERT, show_alert=True)
    try:
        await query.message.delete()
    except Exception:
        pass
        
    settings = await db.get_settings()
    if settings.get('shortlink_status'):
        is_locked = await handle_verification_check(client, query.message, user_id, payload, settings)
        if is_locked: return

    await deliver_file(client, query.message.chat.id, payload)
