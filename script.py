class Script:
    BRANDING_TAG = "\n\n<blockquote>Pᴏᴡᴇʀᴇᴅ Bʏ @koreandrama006</blockquote>"
    
    # ================= Delivery & Messages =================
    AUTO_DELETE_DONE = "<blockquote>🗑 <b>Yᴏᴜʀ Fɪʟᴇs Hᴀᴠᴇ Bᴇᴇɴ Aᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ Dᴇʟᴇᴛᴇᴅ!</b></blockquote>"
    INVALID_LINK = "<blockquote>❌ <b>Tʜɪs Lɪɴᴋ Is Iɴᴠᴀʟɪᴅ Oʀ Hᴀs Exᴘɪʀᴇᴅ!</b></blockquote>"
    BATCH_SENDING = "<blockquote>⏳ <b>Sᴇɴᴅɪɴɢ {total_files} Fɪʟᴇs... Pʟᴇᴀsᴇ Wᴀɪᴛ!</b></blockquote>"
    BATCH_SUCCESS = "<blockquote>✅ <b>Aʟʟ Yᴏᴜʀ Fɪʟᴇs Hᴀᴠᴇ Bᴇᴇɴ Sᴇɴᴛ Sᴜᴄᴄᴇssғᴜʟʟʏ!</b></blockquote>"
    BATCH_SUCCESS_WARN = "<blockquote>✅ <b>Aʟʟ Yᴏᴜʀ Fɪʟᴇs Hᴀᴠᴇ Bᴇᴇɴ Sᴇɴᴛ Sᴜᴄᴄᴇssғᴜʟʟʏ!</b>\n\n⚠️ <b>Wᴀʀɴɪɴɢ:</b> Tᴏ ᴘʀᴇᴠᴇɴᴛ sᴘᴀᴍ, ᴛʜᴇsᴇ ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ <b>{auto_delete_time} ᴍɪɴᴜᴛᴇs</b>. Pʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴛʜᴇᴍ ɴᴏᴡ.</blockquote>"
    FILE_NOT_FOUND_SERVER = "<blockquote>❌ <b>Fɪʟᴇ Nᴏᴛ Fᴏᴜɴᴅ Oɴ Sᴇʀᴠᴇʀ!</b></blockquote>"
    MSG_NOT_FOUND_SERVER = "<blockquote>❌ <b>Mᴇssᴀɢᴇ Nᴏᴛ Fᴏᴜɴᴅ Oɴ Sᴇʀᴠᴇʀ!</b></blockquote>"
    SINGLE_SUCCESS_WARN = "<blockquote>⚠️ <b>Wᴀʀɴɪɴɢ:</b> Tᴏ ᴘʀᴇᴠᴇɴᴛ sᴘᴀᴍ, ᴛʜɪs ғɪʟᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇᴅ ɪɴ <b>{auto_delete_time} ᴍɪɴᴜᴛᴇs</b>. Pʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ɪᴛ ɴᴏᴡ.</blockquote>"
    DELIVERY_ERROR = "<blockquote>❌ <b>Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀʀᴇᴅ Dᴜʀɪɴɢ Dᴇʟɪᴠᴇʀʏ!</b></blockquote>"
    
    # ================= Verification & Guard =================
    BYPASS_DETECTED = "<blockquote>🚫 <b>BYPASS DETECTED / INVALID SIGNATURE!</b> 🚫\n\nYᴏᴜ ʜᴀᴠᴇ ᴜsᴇᴅ ᴀ ᴛʜɪʀᴅ-ᴘᴀʀᴛʏ ʙʏᴘᴀss ᴛᴏᴏʟ ᴏʀ ᴇɴᴛᴇʀᴇᴅ ᴀɴ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ!\n\n<b>Pʟᴇᴀsᴇ ᴄʟɪᴄᴋ ᴛʜᴇ ʟɪɴᴋ ᴀɢᴀɪɴ ᴀɴᴅ ᴠᴇʀɪғʏ ʜᴏɴᴇsᴛʟʏ.</b></blockquote>"
    VERIFY_SUCCESS_TIME = "<blockquote>✅ <b>Vᴇʀɪғɪᴄᴀᴛɪᴏɴ Sᴜᴄᴄᴇssғᴜʟ!</b>\n\n🎉 Yᴏᴜ ᴄᴀɴ ɴᴏᴡ ᴅᴏᴡɴʟᴏᴀᴅ ᴜɴʟɪᴍɪᴛᴇᴅ ғɪʟᴇs ғᴏʀ ᴛʜᴇ ɴᴇxᴛ <b>{duration} ʜᴏᴜʀs</b>. Sᴇɴᴅɪɴɢ ʏᴏᴜʀ ғɪʟᴇ...</blockquote>"
    VERIFY_SUCCESS_CREDIT = "<blockquote>✅ <b>Vᴇʀɪғɪᴄᴀᴛɪᴏɴ Sᴜᴄᴄᴇssғᴜʟ!</b>\n\n🎁 <b>{creds} ᴄʀᴇᴅɪᴛs</b> ʜᴀᴠᴇ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ. Sᴇɴᴅɪɴɢ ʏᴏᴜʀ ғɪʟᴇ...</blockquote>"
    VERIFY_INVALID = "<blockquote>❌ <b>Iɴᴠᴀʟɪᴅ Oʀ Exᴘɪʀᴇᴅ Vᴇʀɪғɪᴄᴀᴛɪᴏɴ Tᴏᴋᴇɴ!</b>\nPʟᴇᴀsᴇ ᴄʟɪᴄᴋ ᴛʜᴇ ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ ᴀɴᴅ ᴠᴇʀɪғʏ ᴀɢᴀɪɴ.</blockquote>"
    GENERATING_SECURE_LINK = "<blockquote>⏳ <b>Gᴇɴᴇʀᴀᴛɪɴɢ Hɪɢʜʟʏ Sᴇᴄᴜʀᴇ Lɪɴᴋ...</b></blockquote>"
    VERIFY_REQUIRED_UI = "📊 <b>ʜᴇʏ ʙʀᴏ/sɪs,</b>\n\n‼️ <b>ɢᴇᴛ ᴀʟʟ ꜰɪʟᴇꜱ ɪɴ ᴀ ꜱɪɴɢʟᴇ ʟɪɴᴋ</b> ‼️\n\n➪ <b>Yᴏᴜʀ ʟɪɴᴋ ɪs ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴠᴇʀɪғʏ ʟɪɴᴋ ʙᴜᴛᴛᴏɴ..</b>"
    
    GUARD_BANNED = "<blockquote>🚫 <b>BYPASS TOOL DETECTED!</b>\nIɴᴠᴀʟɪᴅ sɪɢɴᴀᴛᴜʀᴇ! Yᴏᴜ ᴀᴛᴛᴇᴍᴘᴛᴇᴅ ᴛᴏ ʙʏᴘᴀss ᴛʜᴇ ʟɪɴᴋ ᴍᴀɴᴜᴀʟʟʏ.</blockquote>"
    
    # ================= Start & FSub =================
    BANNED_MSG = "<blockquote>❌ <b>Sᴏʀʀʏ! Yᴏᴜ Hᴀᴠᴇ Bᴇᴇɴ Pᴇʀᴍᴀɴᴇɴᴛʟʏ Bᴀɴɴᴇᴅ Fʀᴏᴍ Tʜɪs Bᴏᴛ.</b>\n\nPʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ ғᴏʀ ᴀssɪsᴛᴀɴᴄᴇ.</blockquote>"
    BANNED_CB_MSG = "<blockquote>❌ <b>Sᴏʀʀʏ! Yᴏᴜ Hᴀᴠᴇ Bᴇᴇɴ Bᴀɴɴᴇᴅ Fʀᴏᴍ Tʜɪs Bᴏᴛ.</b></blockquote>"
    BANNED_CB_ALERT = "❌ Yᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴛʜɪs ʙᴏᴛ!"
    NEW_USER_LOG = "<blockquote>🆕 <b>Nᴇᴡ Usᴇʀ Aʟᴇʀᴛ</b>\n\n👤 <b>Nᴀᴍᴇ:</b> {mention}\n🆔 <b>ID:</b> <code>{user_id}</code>\n🔗 <b>Sᴛᴀʀᴛᴇᴅ Wɪᴛʜ:</b> <code>{text}</code></blockquote>"
    PRIVATE_MODE_MSG = "<blockquote>🔒 <b>Sᴏʀʀʏ! Tʜᴇ Bᴏᴛ Is Cᴜʀʀᴇɴᴛʟʏ Iɴ Pʀɪᴠᴀᴛᴇ Mᴏᴅᴇ.</b>\nYᴏᴜ ᴄᴀɴ ᴀᴄᴄᴇss ғɪʟᴇs ᴏɴᴄᴇ ᴛʜᴇ ᴀᴅᴍɪɴ ᴍᴀᴋᴇs ɪᴛ ᴘᴜʙʟɪᴄ.</blockquote>"
    FSUB_WARNING = "<blockquote>⚠️ <b>Yᴏᴜ Mᴜsᴛ Jᴏɪɴ Tʜᴇ Cʜᴀɴɴᴇʟs Bᴇʟᴏᴡ Tᴏ Gᴇᴛ Tʜᴇ Fɪʟᴇ!</b>\n\n<i>(Tʜᴇsᴇ ᴊᴏɪɴ ʟɪɴᴋs ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇᴅ ɪɴ 10 ᴍɪɴᴜᴛᴇs)</i></blockquote>"
    
    PREMIUM_USER_TAG = "\n\n🌟 <b>Yᴏᴜ Aʀᴇ A Pʀᴇᴍɪᴜᴍ Usᴇʀ! Nᴏ Aᴅs.</b>"
    CREDIT_TAG = "\n\n💳 <b>Aᴠᴀɪʟᴀʙʟᴇ Cʀᴇᴅɪᴛs:</b> <code>{creds}</code>"
    FSUB_NOT_JOINED_ALERT = "⚠️ Yᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ! Pʟᴇᴀsᴇ ᴊᴏɪɴ."
    FSUB_JOINED_ALERT = "✅ Cʜᴀɴɴᴇʟ Vᴇʀɪғɪᴄᴀᴛɪᴏɴ Sᴜᴄᴄᴇssғᴜʟ!"
    
    # 🚀 NEW: ULTRA PREMIUM START UI TEXTS (WITH HIDDEN HYPERLINKS)
    START_MSG = "» ʜᴇʏ {mention} ~\n\n<blockquote>Lᴏᴠᴇ K-Dʀᴀᴍᴀ & Mᴏᴠɪᴇs? I ᴀᴍ ᴍᴀᴅᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ғɪɴᴅ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ʟᴏᴏᴋɪɴɢ ғᴏʀ.</blockquote>"
    
    FOR_MORE_MSG = "» ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ: <a href='{updates}'>LᴜxᴇFʟɪx</a>\n\n<blockquote>» ᴜᴘᴅᴀᴛᴇs: <a href='{updates}'>Cʟɪᴄᴋ ʜᴇʀᴇ</a>\n» ᴍᴏᴠɪᴇs: <a href='{movies}'>Lᴜxᴇ Mᴏᴠɪᴇs</a>\n» sᴇʀɪᴇs: <a href='{series}'>Lᴜxᴇ Sᴇʀɪᴇs</a>\n» ᴅᴇᴠᴇʟᴏᴘᴇʀ: <a href='{developer}'>@ʟᴜxᴇʙᴏᴛᴜᴘᴅᴀᴛᴇ</a></blockquote>"
    
    ABOUT_MSG = "» ᴍʏ ɴᴀᴍᴇ: <b>{bot_name}</b>\n\n<blockquote>» ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='{updates}'>Cʟɪᴄᴋ ʜᴇʀᴇ</a>\n» ᴏᴡɴᴇʀ: <a href='{owner}'>Lᴜxᴇ Oᴡɴᴇʀ</a>\n» ʟᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/'>Pʏᴛʜᴏɴ 3</a>\n» ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a>\n» ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/'>Mᴏɴɢᴏ DB</a>\n» ᴅᴇᴠᴇʟᴏᴘᴇʀ: <a href='{developer}'>@ʟᴜxᴇʙᴏᴛᴜᴘᴅᴀᴛᴇ</a></blockquote>"
    
    COMMANDS_MSG = "<blockquote>» ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:</blockquote>\n\n<blockquote>» /batch : Cʀᴇᴀᴛᴇ ɢʀᴏᴜᴘ ᴍᴇssᴀɢᴇs\n» /genlink : Cʀᴇᴀᴛᴇ ʟɪɴᴋ ғᴏʀ ᴏɴᴇ ᴘᴏsᴛ\n» /broadcast : Bʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ\n» /dbroadcast : Aᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ʙʀᴏᴀᴅᴄᴀsᴛ\n» /settings : Vɪᴇᴡ ᴍᴇssᴀɢᴇ/ғɪʟᴇs ʀᴇʟᴀᴛᴇᴅ sᴇᴛᴛɪɴɢs\n» /stats : Vɪᴇᴡ ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs + ᴜᴘᴛɪᴍᴇ\n» /add_prem : Aᴅᴅ ᴀɴʏ ᴜsᴇʀ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ\n» /del_prem : Rᴇᴍᴏᴠᴇ ᴀɴʏ ᴜsᴇʀ ғʀᴏᴍ ᴘʀᴇᴍɪᴜᴍ</blockquote>"
    
    STATS_UI_MSG = "» ᴄᴏɴғɪɢᴜʀᴀᴛɪᴏɴs\n\n<blockquote>» ᴛᴏᴛᴀʟ ᴜsᴇʀs: <code>{total_users}</code>\n» ᴛᴏᴛᴀʟ ғɪʟᴇs: <code>{total_files}</code>\n» ᴛᴏᴛᴀʟ ʙᴀɴɴᴇᴅ ᴜsᴇʀs: <code>{total_banned}</code>\n» ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴏᴅᴇ: <b>{auto_delete}</b>\n» ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ: <b>{protect}</b>\n» ᴡᴇʙ ɢᴜᴀʀᴅ: <b>{guard}</b></blockquote>"

    # ================= Generate Link =================
    NOT_ADMIN_WARN = "<blockquote>⚠️ <b>Wᴀʀɴɪɴɢ:</b> Yᴏᴜ Dᴏ Nᴏᴛ Hᴀᴠᴇ Pᴇʀᴍɪssɪᴏɴ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ! Oɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴄʀᴇᴀᴛᴇ ʟɪɴᴋs.</blockquote>"
    NOT_ADMIN_SIMPLE = "<blockquote>⚠️ <b>Wᴀʀɴɪɴɢ:</b> Yᴏᴜ Aʀᴇ Nᴏᴛ Aɴ Aᴅᴍɪɴ! Yᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜᴘʟᴏᴀᴅ ғɪʟᴇs ᴏʀ ᴄʀᴇᴀᴛᴇ ʟɪɴᴋs.</blockquote>"
    NO_DB_SET = "<blockquote>❌ <b>Pʟᴇᴀsᴇ Sᴇᴛ Tʜᴇ Dᴀᴛᴀʙᴀsᴇ Cʜᴀɴɴᴇʟ Fɪʀsᴛ!</b> <code>/set_db -100xxxx</code></blockquote>"
    BATCH_START = "<blockquote>🟢 <b>Bᴀᴛᴄʜ Lɪɴᴋ Gᴇɴᴇʀᴀᴛɪᴏɴ Sᴛᴀʀᴛᴇᴅ!</b>\n\n➡️ <b>Sᴛᴇᴘ 1:</b> Fᴏʀᴡᴀʀᴅ ʏᴏᴜʀ <b>Fɪʀsᴛ Fɪʟᴇ</b> ғʀᴏᴍ ᴛʜᴇ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ ʜᴇʀᴇ ᴏʀ sᴇɴᴅ ᴛʜᴇ <b>Lɪɴᴋ</b> ᴏғ ᴛʜᴇ ғɪʀsᴛ ғɪʟᴇ.\n\n<i>(Sᴇɴᴅ /cancel ᴛᴏ ᴀʙᴏʀᴛ)</i></blockquote>"
    BATCH_CANCEL = "<blockquote>✅ <b>Bᴀᴛᴄʜ Pʀᴏᴄᴇss Cᴀɴᴄᴇʟʟᴇᴅ.</b></blockquote>"
    WRONG_MSG_LINK = "<blockquote>❌ <b>Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴍᴇssᴀɢᴇ ʟɪɴᴋ ᴏʀ ғᴏʀᴡᴀʀᴅᴇᴅ ғɪʟᴇ!</b></blockquote>"
    BATCH_STEP_2 = "<blockquote>✅ <b>Fɪʀsᴛ Fɪʟᴇ ID Cᴀᴘᴛᴜʀᴇᴅ:</b> <code>{msg_id}</code>\n\n➡️ <b>Sᴛᴇᴘ 2:</b> Nᴏᴡ ғᴏʀᴡᴀʀᴅ ʏᴏᴜʀ <b>Lᴀsᴛ Fɪʟᴇ</b> ғʀᴏᴍ ᴛʜᴇ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟ ᴏʀ sᴇɴᴅ ɪᴛs <b>Lɪɴᴋ</b>.</blockquote>"
    GEN_BATCH_LINK_WAIT = "<blockquote>⏳ <b>Gᴇɴᴇʀᴀᴛɪɴɢ Bᴀᴛᴄʜ Lɪɴᴋ...</b></blockquote>"
    BATCH_SUCCESS_LINK = "<blockquote>✅ <b>Bᴀᴛᴄʜ Sᴛᴏʀᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ! ({total_files} Fɪʟᴇs)</b>\n\n🔗 <b>Lɪɴᴋ:</b> <code>{custom_link}</code></blockquote>"
    LOG_BATCH_LINK = "<blockquote>🔗 <b>Nᴇᴡ Bᴀᴛᴄʜ Lɪɴᴋ</b>\n\n👤 <b>Bʏ:</b> {mention}\n📦 <b>Fɪʟᴇs:</b> <code>{total_files}</code>\n🔗 <b>Lɪɴᴋ:</b> <code>{custom_link}</code></blockquote>"
    GEN_DB_LINK_WAIT = "<blockquote>⏳ <b>Gᴇɴᴇʀᴀᴛɪɴɢ Lɪɴᴋ Fᴏʀ DB Cʜᴀɴɴᴇʟ Mᴇssᴀɢᴇ...</b></blockquote>"
    SINGLE_SUCCESS_LINK = "<blockquote>✅ <b>Sᴀᴠᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!</b>\n🔗 <b>Lɪɴᴋ:</b> <code>{custom_link}</code></blockquote>"
    LOG_SINGLE_LINK = "<blockquote>🔗 <b>Nᴇᴡ Sɪɴɢʟᴇ Lɪɴᴋ</b>\n\n👤 <b>Bʏ:</b> {mention}\n🔗 <b>Lɪɴᴋ:</b> <code>{custom_link}</code></blockquote>"
    GEN_LINK_WAIT = "<blockquote>⏳ <b>Gᴇɴᴇʀᴀᴛɪɴɢ Lɪɴᴋ...</b></blockquote>"
    FILE_EXISTS = "<blockquote>⚠️ <b>Fɪʟᴇ Aʟʀᴇᴀᴅʏ Exɪsᴛs!</b>\n🔗 <b>Lɪɴᴋ:</b> <code>{custom_link}</code></blockquote>"
    GEN_PERMANENT_WAIT = "<blockquote>👇 <b>Cʟɪᴄᴋ Bᴇʟᴏᴡ Tᴏ Gᴇɴᴇʀᴀᴛᴇ Pᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋ:</b></blockquote>"
    PROCESSING_FILE = "<blockquote>⏳ <b>Pʀᴏᴄᴇssɪɴɢ Fɪʟᴇ...</b></blockquote>"
    SAVED_IN_DB = "<blockquote>✅ <b>Sᴀᴠᴇᴅ Iɴ Dᴀᴛᴀʙᴀsᴇ!</b>\n🔗 <b>Lɪɴᴋ:</b> <code>{custom_link}</code></blockquote>"
    ERROR_MSG = "<blockquote>❌ <b>Eʀʀᴏʀ:</b> {error}</blockquote>"
    
    # ================= Admin Utils =================
    NOT_OWNER_WARN = "<blockquote>⚠️ <b>Wᴀʀɴɪɴɢ:</b> Oɴʟʏ Tʜᴇ Oᴡɴᴇʀ Cᴀɴ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ!</blockquote>"
    FETCHING_STATS = "<blockquote>⏳ <b>Fᴇᴛᴄʜɪɴɢ Uɴɪǫᴜᴇ Sᴛᴀᴛɪsᴛɪᴄs...</b></blockquote>"
    STATS_MSG = "<blockquote>📊 <b>Bᴏᴛ Aᴅᴠᴀɴᴄᴇᴅ Sᴛᴀᴛɪsᴛɪᴄs</b>\n\n⏱ <b>Uᴘᴛɪᴍᴇ:</b> <code>{uptime}</code>\n👥 <b>Tᴏᴛᴀʟ Usᴇʀs:</b> <code>{total_users}</code>\n🚫 <b>Bᴀɴɴᴇᴅ Usᴇʀs:</b> <code>{total_banned}</code>\n📁 <b>Tᴏᴛᴀʟ Fɪʟᴇs Sᴀᴠᴇᴅ:</b> <code>{total_files}</code>\n🗄 <b>Mᴜʟᴛɪ-DB Sᴛᴀᴛᴜs:</b> <code>{multi_db_status}</code>\n🔗 <b>Sʜᴏʀᴛʟɪɴᴋ:</b> <code>{sl_status} ({sl_type})</code>\n🛡 <b>Wᴇʙ Gᴜᴀʀᴅ:</b> <code>{guard_status}</code></blockquote>"
    REPLY_DBROADCAST = "<blockquote>❌ <b>Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ:</b> Rᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴀɴᴅ sᴇɴᴅ <code>/dbroadcast 10</code> (Mɪɴᴜᴛᴇs)!</blockquote>"
    MINUTES_NUMBER_ERROR = "<blockquote>❌ <b>Mɪɴᴜᴛᴇs ᴍᴜsᴛ ʙᴇ ᴀ ɴᴜᴍʙᴇʀ!</b></blockquote>"
    DBROADCAST_START = "<blockquote>⏳ <b>Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ Bʀᴏᴀᴅᴄᴀsᴛ Sᴛᴀʀᴛᴇᴅ ({mins} ᴍɪɴs)...</b></blockquote>"
    DBROADCAST_DONE = "<blockquote>✅ <b>Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ Bʀᴏᴀᴅᴄᴀsᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ!</b>\n\n🟢 <b>Sᴇɴᴛ:</b> <code>{sent}</code>\n🔴 <b>Fᴀɪʟᴇᴅ:</b> <code>{failed}</code>\n🗑 <b>Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ ɪɴ:</b> <code>{mins} ᴍɪɴs</code></blockquote>"
    REPLY_BROADCAST = "<blockquote>❌ <b>Rᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ᴍᴇssᴀɢᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ!</b></blockquote>"
    BROADCAST_START = "<blockquote>⏳ <b>Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ sᴛᴀʀᴛᴇᴅ...</b></blockquote>"
    BROADCAST_DONE = "<blockquote>✅ <b>Bʀᴏᴀᴅᴄᴀsᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ!</b>\n\n🟢 <b>Sᴜᴄᴄᴇssғᴜʟʟʏ Sᴇɴᴛ:</b> <code>{sent}</code>\n🔴 <b>Fᴀɪʟᴇᴅ/Bʟᴏᴄᴋᴇᴅ:</b> <code>{failed}</code></blockquote>"
    BAN_USAGE = "<blockquote>❌ <b>Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ:</b> <code>/ban UserID</code></blockquote>"
    BAN_SELF = "<blockquote>❌ <b>Yᴏᴜ ᴄᴀɴɴᴏᴛ ʙᴀɴ ʏᴏᴜʀsᴇʟғ.</b></blockquote>"
    BAN_SUCCESS = "<blockquote>🚫 <b>Usᴇʀ Bᴀɴɴᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ:</b> <code>{user_id}</code></blockquote>"
    ID_NUMBER_ERROR = "<blockquote>❌ <b>Usᴇʀ ID ᴍᴜsᴛ ʙᴇ ᴀ ɴᴜᴍʙᴇʀ!</b></blockquote>"
    UNBAN_USAGE = "<blockquote>❌ <b>Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ:</b> <code>/unban UserID</code></blockquote>"
    UNBAN_SUCCESS = "<blockquote>✅ <b>Usᴇʀ Uɴʙᴀɴɴᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ:</b> <code>{user_id}</code></blockquote>"
    UNBAN_ALL_SUCCESS = "<blockquote>✅ <b>Sᴜᴄᴄᴇssғᴜʟʟʏ ᴜɴʙᴀɴɴᴇᴅ {count} ᴜsᴇʀs!</b></blockquote>"
    ADD_CREDIT_USAGE = "<blockquote>❌ <b>Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ:</b> <code>/add_credit UserID Amount</code></blockquote>"
    ADD_CREDIT_SUCCESS = "<blockquote>✅ <b>Aᴅᴅᴇᴅ {amount} ᴄʀᴇᴅɪᴛs ᴛᴏ ᴜsᴇʀ <code>{user_id}</code></b></blockquote>"
    REMOVE_CREDIT_USAGE = "<blockquote>❌ <b>Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ:</b> <code>/remove_credit UserID Amount</code></blockquote>"
    REMOVE_CREDIT_SUCCESS = "<blockquote>✅ <b>Rᴇᴍᴏᴠᴇᴅ {amount} ᴄʀᴇᴅɪᴛs ғʀᴏᴍ ᴜsᴇʀ <code>{user_id}</code></b></blockquote>"
    ID_AMOUNT_ERROR = "<blockquote>❌ <b>ID ᴀɴᴅ Aᴍᴏᴜɴᴛ ᴍᴜsᴛ ʙᴇ ɴᴜᴍʙᴇʀs!</b></blockquote>"
    SET_SL_USAGE = "<blockquote>❌ <b>Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ:</b> <code>/set_shortlink &lt;url&gt; &lt;api_key&gt;</code>\n<i>Exᴀᴍᴘʟᴇ:</i> <code>/set_shortlink shareus.io 123456789abc</code></blockquote>"
    SET_SL_SUCCESS = "<blockquote>✅ <b>Sʜᴏʀᴛʟɪɴᴋ API Uᴘᴅᴀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!</b>\n\n🌐 <b>URL:</b> <code>{url}</code>\n🔑 <b>API Kᴇʏ:</b> <code>{api}</code></blockquote>"
    SET_TUTORIAL_USAGE = "<blockquote>❌ <b>Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ:</b> <code>/set_tutorial https://t.me/your_video</code>\n<i>(Tᴏ ʀᴇᴍᴏᴠᴇ ᴛᴜᴛᴏʀɪᴀʟ sᴇɴᴅ <code>/set_tutorial off</code>)</i></blockquote>"
    TUTORIAL_REMOVED = "<blockquote>✅ <b>Tᴜᴛᴏʀɪᴀʟ Lɪɴᴋ Rᴇᴍᴏᴠᴇᴅ!</b>\nTʜᴇ ᴛᴜᴛᴏʀɪᴀʟ ʙᴜᴛᴛᴏɴ ᴡɪʟʟ ɴᴏ ʟᴏɴɢᴇʀ ʙᴇ ᴅɪsᴘʟᴀʏᴇᴅ.</blockquote>"
    TUTORIAL_SUCCESS = "<blockquote>✅ <b>Tᴜᴛᴏʀɪᴀʟ Lɪɴᴋ Uᴘᴅᴀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!</b>\n\n🔗 <b>Lɪɴᴋ:</b> {link}</blockquote>"
    
    SET_DELETE_USAGE = "<blockquote>❌ <b>Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ:</b> <code>/set_delete 10</code> (ᴍɪɴᴜᴛᴇs) ᴏʀ <code>/set_delete off</code></blockquote>"
    SET_DELETE_OFF = "<blockquote>✅ <b>Aᴜᴛᴏ Dᴇʟᴇᴛᴇ Is Nᴏᴡ OFF!</b>\nFɪʟᴇs ᴡɪʟʟ ɴᴏ ʟᴏɴɢᴇʀ ʙᴇ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇᴅ.</blockquote>"
    SET_DELETE_ON = "<blockquote>✅ <b>Aᴜᴛᴏ Dᴇʟᴇᴛᴇ Is Nᴏᴡ ON!</b>\nUsᴇʀ ғɪʟᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀғᴛᴇʀ <b>{mins} ᴍɪɴᴜᴛᴇs</b>.</blockquote>"
    
    SETTINGS_MSG = "<blockquote>⚙️ <b>Aᴅᴠᴀɴᴄᴇᴅ Bᴏᴛ Sᴇᴛᴛɪɴɢs Pᴀɴᴇʟ</b>\n\nCʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛʀᴏʟ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴀɴᴅ sʜᴏʀᴛʟɪɴᴋ sʏsᴛᴇᴍs:</blockquote>"
    NOT_OWNER_ALERT = "❌ Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴛʜᴇ ᴏᴡɴᴇʀ!"
    SETTINGS_UPDATED_ALERT = "✅ Sᴇᴛᴛɪɴɢs Uᴘᴅᴀᴛᴇᴅ!"
    
    BUY_PREMIUM_MSG = "<blockquote><b>Iғ Yᴏᴜ Wᴀɴᴛ Tᴏ Bᴜʏ Pʀᴇᴍɪᴜᴍ, Cᴏɴᴛᴀᴄᴛ Tʜᴇ Oᴡɴᴇʀ</b></blockquote>"
    
    BTN_OWNER = "👤 ᴏᴡɴᴇʀ"
    BTN_GROUP = "👥 ɢʀᴏᴜᴘ"
    BTN_BUY_NOW = "🛒 ʙᴜʏ ɴᴏᴡ"
    
    BTN_UPDATES_CHANNEL = "📢 ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ"
    BTN_CONTACT_SUPPORT = "🛠 ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ"
    BTN_OPEN_LINK = "• ᴠᴇʀɪғʏ ʟɪɴᴋ"
    BTN_TUTORIAL = "ʜᴏᴡ ᴛᴏ ᴠᴇʀɪғʏ •"
    
    BTN_BUY_PREMIUM = "• ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ •"
    BTN_PREMIUM_SETTINGS = "💎 ᴘʀᴇᴍɪᴜᴍ sᴇᴛᴛɪɴɢs"
    
    # 🚀 NEW: ULTRA PREMIUM MENU BUTTONS
    BTN_FOR_MORE = "• ғᴏʀ ᴍᴏʀᴇ •"
    BTN_ABOUT = "• ᴀʙᴏᴜᴛ •"
    BTN_COMMANDS = "ᴄᴏᴍᴍᴀɴᴅs •"
    BTN_BACK_START = "• ʙᴀᴄᴋ •"
    BTN_CLOSE = "ᴄʟᴏsᴇ •"
    BTN_STATS = "sᴛᴀᴛs •"
    
    BTN_CHECK_JOINED = "🔄 ᴄʜᴇᴄᴋ ᴊᴏɪɴᴇᴅ"
    BTN_JOIN_CHANNEL = "🟢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ {idx}"
    BTN_ORIGINAL_LINK = "🌐 ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ"
    BTN_GENERATE_LINK = "📁 ɢᴇɴᴇʀᴀᴛᴇ ʟɪɴᴋ"
    BTN_SL_STATUS = "🔗 sʜᴏʀᴛʟɪɴᴋ: {status}"
    BTN_SL_MODE = "⚙️ ᴍᴏᴅᴇ: {mode}"
    BTN_SL_TIME = "⏱ ᴠᴇʀɪғʏ ᴅᴜʀᴀᴛɪᴏɴ: {time} ʜᴏᴜʀs 🔄"
    BTN_SL_CREDIT = "🎁 ᴄʀᴇᴅɪᴛs: {creds} ғɪʟᴇs 🔄"
    BTN_BYPASS_TIME = "🛡 ʙʏᴘᴀss ᴛɪᴍᴇ ɢᴜᴀʀᴅ: {time}s 🔄"
    BTN_WEB_GUARD = "🔥 ᴄʟᴏᴜᴅғʟᴀʀᴇ ᴡᴇʙ ɢᴜᴀʀᴅ: {status}"
    BTN_PROTECT_CONTENT = "🔒 ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ: {status}"
    BTN_CLOSE_PANEL = "❌ ᴄʟᴏsᴇ ᴘᴀɴᴇʟ"
