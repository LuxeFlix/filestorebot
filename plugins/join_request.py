from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest
from utils.database import db

@Client.on_chat_join_request()
async def handle_join_request(client: Client, request: ChatJoinRequest):
    # 🚀 রিকোয়েস্ট আসামাত্রই ডাটাবেসে সেভ হবে যাতে ইউজার অ্যাপ্রুভালের আগেই ফাইল পেয়ে যায়
    await db.add_join_request(request.from_user.id, request.chat.id)
