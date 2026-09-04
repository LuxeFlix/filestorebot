import time
from pyrogram.errors import UserNotParticipant
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from utils.database import db
from script import Script

async def get_all_fsubs():
    db_fsubs = await db.get_fsub_channels()
    config_fsubs = [int(x) for x in str(Config.FSUB_CHANNELS).split(",") if x.strip()] if Config.FSUB_CHANNELS else []
    all_fsubs = list(set(config_fsubs + db_fsubs))[:6]
    return all_fsubs

async def check_fsub(client, user_id):
    channels = await get_all_fsubs()
    missing_channels = []
    
    for chat_id in channels:
        try:
            member = await client.get_chat_member(chat_id, user_id)
            if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
                if not await db.has_join_request(user_id, chat_id):
                    missing_channels.append(chat_id)
        except UserNotParticipant:
            if not await db.has_join_request(user_id, chat_id):
                missing_channels.append(chat_id)
        except Exception:
            pass 
            
    return missing_channels

async def get_fsub_keyboard(client, missing_channels, payload):
    buttons = []
    settings = await db.get_settings()
    is_req_fsub = settings.get('req_fsub', False)
    
    for idx, chat_id in enumerate(missing_channels, start=1):
        try:
            expire_time = int(time.time()) + 600
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
