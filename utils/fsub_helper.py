import time
import asyncio
from datetime import datetime, timedelta
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from utils.database import db
from script import Script

# 🚀 1. Asynchronous Semaphore (অদৃশ্য ট্রাফিক পুলিশ)
fsub_semaphore = asyncio.Semaphore(5)

# 🚀 2. Anti-Spam Micro-Delay (Double-Click Protection)
MICRO_CACHE = {}
MICRO_CACHE_TTL = 3  # মাত্র ৩ সেকেন্ড

async def get_all_fsubs():
    db_fsubs = await db.get_fsub_channels()
    config_fsubs = [int(x) for x in str(Config.FSUB_CHANNELS).split(",") if x.strip()] if Config.FSUB_CHANNELS else []
    all_fsubs = list(set(config_fsubs + db_fsubs))[:6]
    return all_fsubs

async def check_fsub(client, user_id):
    current_time = time.time()
    
    # 🚀 FIX: Clean expired cache to prevent Memory Leak
    expired_keys = [k for k, v in MICRO_CACHE.items() if v.get('expires', 0) <= current_time]
    for k in expired_keys:
        del MICRO_CACHE[k]
    
    # 🚀 Double-Click Spam Protection & FSub Security Bug FIXED
    if user_id in MICRO_CACHE and current_time < MICRO_CACHE[user_id]['expires']:
        return MICRO_CACHE[user_id]['missing'] # 🚀 FIX: Return actual cached channels instead of empty []
    
    channels = await get_all_fsubs()
    missing_channels = []
    
    # 🚀 Semaphore Block: ট্রাফিক কন্ট্রোল করে রিয়েল-টাইম চেক করবে
    async with fsub_semaphore:
        for chat_id in channels:
            try:
                member = await client.get_chat_member(chat_id, user_id)
                if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
                    if not await db.has_join_request(user_id, chat_id):
                        missing_channels.append(chat_id)
            except UserNotParticipant:
                if not await db.has_join_request(user_id, chat_id):
                    missing_channels.append(chat_id)
            except FloodWait as e:
                # সেফটি ফিউজ: যদি কোনোভাবে লিমিট ক্রস হয়, বট নিজে থেকেই ওয়েট করবে
                await asyncio.sleep(e.value + 0.5)
                try:
                    member = await client.get_chat_member(chat_id, user_id)
                    if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
                        if not await db.has_join_request(user_id, chat_id):
                            missing_channels.append(chat_id)
                except Exception:
                    missing_channels.append(chat_id)
            except Exception:
                pass 
                
    # 🚀 FIX: Store the actual result in cache
    MICRO_CACHE[user_id] = {'expires': current_time + MICRO_CACHE_TTL, 'missing': missing_channels}            
    return missing_channels

async def get_fsub_keyboard(client, missing_channels, payload):
    buttons = []
    settings = await db.get_settings()
    is_req_fsub = settings.get('req_fsub', False)
    
    for idx, chat_id in enumerate(missing_channels, start=1):
        try:
            expire_time = datetime.now() + timedelta(minutes=10)
            
            invite_link = await client.create_chat_invite_link(
                chat_id=chat_id, 
                creates_join_request=is_req_fsub, 
                expire_date=expire_time
            )
            buttons.append([InlineKeyboardButton(Script.BTN_JOIN_CHANNEL.format(idx=idx), url=invite_link.invite_link)])
            
        except Exception as e:
            print(f"Error creating invite link for {chat_id}: {e}")
            continue
    
    if payload:
        buttons.append([InlineKeyboardButton(Script.BTN_CHECK_JOINED, callback_data=f"chkF_{payload}", style="primary")])
        
    return InlineKeyboardMarkup(buttons)
