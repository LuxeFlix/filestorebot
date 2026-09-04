import time
import asyncio
import random
import gc
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, LinkPreviewOptions, WebAppInfo
from pyrogram.errors import FloodWait, ChannelInvalid, ChannelPrivate, ChatAdminRequired
from pyrogram.enums import ParseMode
from config import Config
from utils.database import db
from utils.fsub_helper import check_fsub, get_fsub_keyboard
from utils.shortener import get_shortlink
from utils.shortlink_guard import ShortlinkGuard
from script import Script

FILE_CACHE = {}
MAX_CACHE_SIZE = 50

async def get_cached_file(unique_id: str):
    if unique_id in FILE_CACHE:
        val = FILE_CACHE.pop(unique_id)
        FILE_CACHE[unique_id] = val
        return val
    file_data = await db.get_file(unique_id)
    if file_data:
        FILE_CACHE[unique_id] = file_data
        if len(FILE_CACHE) > MAX_CACHE_SIZE:
            FILE_CACHE.pop(next(iter(FILE_CACHE)))
    return file_data

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
    warn_msg_id = message_ids[-1]
    file_msg_ids = message_ids[:-1]
    
    try:
        if file_msg_ids:
            await client.delete_messages(chat_id, file_msg_ids)
    except Exception:
        pass
        
    try:
        await client.edit_message_text(chat_id, warn_msg_id, Script.AUTO_DELETE_DONE)
    except Exception:
        pass

async def deliver_file(client: Client, chat_id: int, payload: str, reply_to_msg=None):
    unique_id = payload
        
    try:
        file_data = await get_cached_file(unique_id)
        if not file_data:
            if reply_to_msg:
                await reply_to_msg.reply_text(Script.INVALID_LINK)
            else:
                await client.send_message(chat_id, Script.INVALID_LINK)
            return

        sent_msg_ids = []
        settings = await db.get_settings()
        auto_delete_time = settings.get('auto_delete', 0)
        is_protected = settings.get('protect_content', False)

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
                            sent_m = await client.copy_message(chat_id, db_chat_id, msg_id, caption=final_cap, parse_mode=ParseMode.HTML, protect_content=is_protected)
                        else:
                            sent_m = await client.copy_message(chat_id, db_chat_id, msg_id, protect_content=is_protected)
                    if sent_m: sent_msg_ids.append(sent_m.id)
                    
                    await asyncio.sleep(random.uniform(0.6, 1.8)) 
                except FloodWait as e:
                    await asyncio.sleep(e.value + random.uniform(1.0, 2.5))
                    if db_msg and getattr(db_msg, "media", None):
                        sent_m = await client.copy_message(chat_id, db_chat_id, msg_id, caption=final_cap, parse_mode=ParseMode.HTML, protect_content=is_protected)
                    elif db_msg:
                        sent_m = await client.copy_message(chat_id, db_chat_id, msg_id, protect_content=is_protected)
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
                        sent_m = await client.copy_message(chat_id, db_chat_id, msg_id, caption=final_cap, parse_mode=ParseMode.HTML, protect_content=is_protected)
                    else:
                        sent_m = await client.copy_message(chat_id, db_chat_id, msg_id, protect_content=is_protected)
                else:
                    raise Exception("Message empty")
            except (ChannelInvalid, ChannelPrivate, ChatAdminRequired, Exception):
                if 'f' in file_data:
                    orig_cap = file_data.get('cap', '')
                    final_cap = format_caption(orig_cap)
                    try:
                        sent_m = await client.send_cached_media(chat_id, file_data['f'], caption=final_cap, parse_mode=ParseMode.HTML, protect_content=is_protected)
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
    finally:
        gc.collect()

async def handle_verification_check(client: Client, message: Message, user_id: int, payload: str, settings: dict):
    if await db.is_admin(user_id) or await db.check_and_use_premium(user_id):
        return False
        
    free_limit = settings.get('free_daily_limit', 0)
    if free_limit > 0:
        if await db.check_and_use_free_limit(user_id, free_limit):
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
            
        btn_list.append([InlineKeyboardButton(Script.BTN_BUY_PREMIUM, callback_data="show_premium_plans")])
            
        btn = InlineKeyboardMarkup(btn_list)
        await wait_msg.delete()
        
        try:
            verify_img = clean_url(Config.VERIFY_IMG)
            if verify_img:
                await message.reply_photo(photo=verify_img, caption=verify_text, reply_markup=btn)
            else:
                await message.reply_text(verify_text, reply_markup=btn, link_preview_options=LinkPreviewOptions(is_disabled=True))
        except Exception:
            await message.reply_text(verify_text, reply_markup=btn, link_preview_options=LinkPreviewOptions(is_disabled=True))
            
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
        return await message.reply_text(Script.BANNED_MSG, reply_markup=reply_markup, reply_to_message_id=message.id)

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
        await message.reply_text(Script.PRIVATE_MODE_MSG, reply_to_message_id=message.id)
        return

    text = message.text
    payload = text.split()[1] if len(text.split()) > 1 else None
    
    if not is_admin: 
        missing_fsubs = await check_fsub(client, user_id)
        if missing_fsubs:
            keyboard = await get_fsub_keyboard(client, missing_fsubs, payload)
            await message.reply_text(Script.FSUB_WARNING, reply_markup=keyboard, reply_to_message_id=message.id)
            return

    if payload:
        if payload.startswith("vpass_"):
            parts = payload.split("_")
            if len(parts) >= 3:
                token = parts[1]
                signature = parts[2]
                
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
                    return await message.reply_text(Script.GUARD_BANNED)
            else:
                return await message.reply_text(Script.VERIFY_INVALID)
            return

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
        
    # 🚀 SMART BUTTON HIDING: সাধারণ ইউজাররা COMMANDS বাটন দেখতে পাবে না
    btn_list = [[InlineKeyboardButton(Script.BTN_FOR_MORE, callback_data="for_more_menu")]]
    if is_admin:
        btn_list.append([InlineKeyboardButton(Script.BTN_ABOUT, callback_data="about_menu"), InlineKeyboardButton(Script.BTN_COMMANDS, callback_data="commands_menu")])
    else:
        btn_list.append([InlineKeyboardButton(Script.BTN_ABOUT, callback_data="about_menu")])
        
    buttons = InlineKeyboardMarkup(btn_list)
    
    start_pic = getattr(Config, "START_PIC", None)
    if start_pic:
        try:
            await message.reply_photo(photo=start_pic, caption=welcome_text, reply_markup=buttons, parse_mode=ParseMode.HTML)
        except Exception:
            await message.reply_text(welcome_text, reply_markup=buttons, parse_mode=ParseMode.HTML, link_preview_options=LinkPreviewOptions(is_disabled=True))
    else:
        await message.reply_text(welcome_text, reply_markup=buttons, parse_mode=ParseMode.HTML, link_preview_options=LinkPreviewOptions(is_disabled=True))

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

@Client.on_callback_query(filters.regex(r"^(for_more_menu|about_menu|commands_menu|back_to_start|close_menu|stats_menu)$"))
async def start_menu_callbacks(client: Client, query: CallbackQuery):
    action = query.data
    user_id = query.from_user.id
    bot_name = client.me.first_name if client.me else (await client.get_me()).first_name

    if action == "close_menu":
        try:
            await query.message.delete()
        except Exception: pass
        return

    is_admin = await db.is_admin(user_id)

    if action == "back_to_start":
        settings = await db.get_settings()
        welcome_text = Script.START_MSG.format(mention=query.from_user.mention)

        if await db.is_premium(user_id):
            welcome_text += Script.PREMIUM_USER_TAG
        elif settings.get('shortlink_status') and settings.get('shortlink_type') == 'credit' and not is_admin:
            creds = await db.get_credits(user_id)
            welcome_text += Script.CREDIT_TAG.format(creds=creds)

        # 🚀 SMART BUTTON HIDING
        btn_list = [[InlineKeyboardButton(Script.BTN_FOR_MORE, callback_data="for_more_menu")]]
        if is_admin:
            btn_list.append([InlineKeyboardButton(Script.BTN_ABOUT, callback_data="about_menu"), InlineKeyboardButton(Script.BTN_COMMANDS, callback_data="commands_menu")])
        else:
            btn_list.append([InlineKeyboardButton(Script.BTN_ABOUT, callback_data="about_menu")])
            
        buttons = InlineKeyboardMarkup(btn_list)
        try:
            if query.message.photo or query.message.video:
                await query.message.edit_caption(welcome_text, reply_markup=buttons, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(welcome_text, reply_markup=buttons, parse_mode=ParseMode.HTML, link_preview_options=LinkPreviewOptions(is_disabled=True))
        except Exception: pass

    elif action == "for_more_menu":
        text = Script.FOR_MORE_MSG.format(
            updates=getattr(Config, "UPDATES_LINK", "https://t.me/"),
            movies=getattr(Config, "MOVIES_LINK", "https://t.me/"),
            series=getattr(Config, "SERIES_LINK", "https://t.me/"),
            developer=getattr(Config, "DEVELOPER_LINK", "https://t.me/")
        )
        
        # 🚀 SMART BUTTON HIDING: সাধারণ ইউজাররা STATS বাটন দেখতে পাবে না
        btn_list = []
        if is_admin:
            btn_list.append([InlineKeyboardButton(Script.BTN_BACK_START, callback_data="back_to_start"), InlineKeyboardButton(Script.BTN_STATS, callback_data="stats_menu")])
        else:
            btn_list.append([InlineKeyboardButton(Script.BTN_BACK_START, callback_data="back_to_start")])
            
        buttons = InlineKeyboardMarkup(btn_list)
        try:
            if query.message.photo or query.message.video:
                await query.message.edit_caption(text, reply_markup=buttons, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(text, reply_markup=buttons, parse_mode=ParseMode.HTML, link_preview_options=LinkPreviewOptions(is_disabled=True))
        except Exception: pass

    elif action == "about_menu":
        text = Script.ABOUT_MSG.format(
            bot_name=bot_name,
            updates=getattr(Config, "UPDATES_LINK", "https://t.me/"),
            owner=getattr(Config, "OWNER_LINK", "https://t.me/"),
            developer=getattr(Config, "DEVELOPER_LINK", "https://t.me/")
        )
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(Script.BTN_BACK_START, callback_data="back_to_start"), InlineKeyboardButton(Script.BTN_CLOSE, callback_data="close_menu")]
        ])
        try:
            if query.message.photo or query.message.video:
                await query.message.edit_caption(text, reply_markup=buttons, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(text, reply_markup=buttons, parse_mode=ParseMode.HTML, link_preview_options=LinkPreviewOptions(is_disabled=True))
        except Exception: pass

    elif action == "commands_menu":
        if not is_admin:
            return # 🚀 SILENT IGNORE FRONTEND GUARD
            
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(Script.BTN_BACK_START, callback_data="back_to_start"), InlineKeyboardButton(Script.BTN_CLOSE, callback_data="close_menu")]
        ])
        try:
            if query.message.photo or query.message.video:
                await query.message.edit_caption(Script.COMMANDS_MSG, reply_markup=buttons, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(Script.COMMANDS_MSG, reply_markup=buttons, parse_mode=ParseMode.HTML, link_preview_options=LinkPreviewOptions(is_disabled=True))
        except Exception: pass

    elif action == "stats_menu":
        if not is_admin:
            return # 🚀 SILENT IGNORE FRONTEND GUARD

        total_users = await db.total_users()
        total_files = await db.total_files()
        total_banned = await db.total_banned_users()
        settings = await db.get_settings()
        
        auto_del = f"ENABLED ({settings.get('auto_delete')}m)" if settings.get('auto_delete', 0) > 0 else "DISABLED"
        protect = "ENABLED" if settings.get('protect_content') else "DISABLED"
        guard = "ENABLED" if settings.get('web_guard') else "DISABLED"

        text = Script.STATS_UI_MSG.format(
            total_users=total_users, total_files=total_files, total_banned=total_banned, 
            auto_delete=auto_del, protect=protect, guard=guard
        )
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(Script.BTN_BACK_START, callback_data="for_more_menu"), InlineKeyboardButton(Script.BTN_CLOSE, callback_data="close_menu")]
        ])
        try:
            if query.message.photo or query.message.video:
                await query.message.edit_caption(text, reply_markup=buttons, parse_mode=ParseMode.HTML)
            else:
                await query.message.edit_text(text, reply_markup=buttons, parse_mode=ParseMode.HTML, link_preview_options=LinkPreviewOptions(is_disabled=True))
        except Exception: pass

    await query.answer()
