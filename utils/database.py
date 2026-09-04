import time
import motor.motor_asyncio
import string
import secrets
from config import Config

class Database:
    def __init__(self):
        # 🚀 RAM সেভ এবং হাই-স্পিড ডেটা রিড/রাইট করার জন্য Connection Pooling
        pool_settings = {
            "maxPoolSize": 50,
            "minPoolSize": 5,
            "maxIdleTimeMS": 50000
        }
        
        self.client1 = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URI_1, **pool_settings)
        self.db1 = self.client1[Config.MONGO_DB_NAME]
        self.files_col1 = self.db1.files
        
        self.users_col = self.db1.users
        self.admins_col = self.db1.admins
        self.settings_col = self.db1.settings
        self.join_reqs_col = self.db1.join_requests
        self.links_col = self.db1.invite_links 
        self.banned_col = self.db1.banned_users
        
        self.tokens_col = self.db1.verify_tokens
        self.verified_col = self.db1.verified_users
        
        self.premium_col = self.db1.premium_users

        self.files_col2 = None
        if Config.MONGO_URI_2:
            self.db2 = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URI_2, **pool_settings)[Config.MONGO_DB_NAME]
            self.files_col2 = self.db2.files
            
        self.files_col3 = None
        if Config.MONGO_URI_3:
            self.db3 = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URI_3, **pool_settings)[Config.MONGO_DB_NAME]
            self.files_col3 = self.db3.files

    async def add_premium(self, user_id: int, time_seconds: int):
        expire_at = int(time.time()) + time_seconds
        await self.premium_col.update_one({'_id': user_id}, {'$set': {'expire_at': expire_at}}, upsert=True)
        
    async def remove_premium(self, user_id: int):
        await self.premium_col.delete_one({'_id': user_id})

    async def is_premium(self, user_id: int):
        doc = await self.premium_col.find_one({'_id': user_id})
        if doc and doc.get('expire_at', 0) > int(time.time()):
            return True
        if doc and doc.get('expire_at', 0) <= int(time.time()):
            await self.remove_premium(user_id) 
        return False

    async def get_user(self, user_id: int):
        return await self.users_col.find_one({'_id': user_id})

    async def add_credits(self, user_id: int, amount: int):
        await self.users_col.update_one({'_id': user_id}, {'$inc': {'credits': amount}}, upsert=True)

    async def get_credits(self, user_id: int):
        user = await self.get_user(user_id)
        return user.get('credits', 0) if user else 0

    async def use_credit(self, user_id: int):
        user = await self.get_user(user_id)
        if user and user.get('credits', 0) > 0:
            await self.users_col.update_one({'_id': user_id}, {'$inc': {'credits': -1}})
            return True
        return False

    async def create_verify_token(self, user_id: int, payload: str):
        token = secrets.token_hex(6)
        await self.tokens_col.insert_one({'_id': token, 'user_id': user_id, 'payload': payload, 'createdAt': int(time.time())})
        return token

    async def get_verify_token(self, token: str):
        doc = await self.tokens_col.find_one({'_id': token})
        if doc:
            await self.tokens_col.delete_one({'_id': token})
        return doc

    async def verify_user(self, user_id: int, expire_time: int):
        await self.verified_col.update_one({'_id': user_id}, {'$set': {'expire_at': expire_time}}, upsert=True)

    async def is_user_verified(self, user_id: int, current_time: int):
        doc = await self.verified_col.find_one({'_id': user_id})
        if doc and doc.get('expire_at', 0) > current_time:
            return True
        return False

    async def total_users(self):
        return await self.users_col.count_documents({})
        
    async def total_files(self):
        count = await self.files_col1.count_documents({})
        if self.files_col2: count += await self.files_col2.count_documents({})
        if self.files_col3: count += await self.files_col3.count_documents({})
        return count
        
    async def total_banned_users(self):
        return await self.banned_col.count_documents({})
        
    async def get_all_users(self):
        return self.users_col.find({})
        
    async def ban_user(self, user_id: int):
        await self.banned_col.update_one({'_id': user_id}, {'$set': {'banned': True}}, upsert=True)
        
    async def unban_user(self, user_id: int):
        await self.banned_col.delete_one({'_id': user_id})
        
    async def unban_all_users(self):
        result = await self.banned_col.delete_many({})
        return result.deleted_count
        
    async def is_banned(self, user_id: int):
        return bool(await self.banned_col.find_one({'_id': user_id}))

    async def save_invite_link(self, chat_id: int, link: str, expire_at: int):
        await self.links_col.insert_one({'chat_id': chat_id, 'link': link, 'expire_at': expire_at})

    async def get_expired_links(self, current_time: int):
        cursor = self.links_col.find({'expire_at': {'$lte': current_time}})
        return await cursor.to_list(length=None)

    async def remove_invite_link(self, link: str):
        await self.links_col.delete_one({'link': link})

    async def add_join_request(self, user_id: int, chat_id: int):
        await self.join_reqs_col.update_one({'user_id': user_id, 'chat_id': chat_id}, {'$set': {'requested': True}}, upsert=True)

    async def has_join_request(self, user_id: int, chat_id: int):
        return bool(await self.join_reqs_col.find_one({'user_id': user_id, 'chat_id': chat_id}))

    async def get_fsub_channels(self):
        settings = await self.settings_col.find_one({'_id': 'bot_settings'})
        return settings.get('fsub_channels', []) if settings else []

    async def add_fsub_channel(self, chat_id: int):
        await self.settings_col.update_one({'_id': 'bot_settings'}, {'$addToSet': {'fsub_channels': chat_id}}, upsert=True)

    async def remove_fsub_channel(self, chat_id: int):
        await self.settings_col.update_one({'_id': 'bot_settings'}, {'$pull': {'fsub_channels': chat_id}}, upsert=True)

    async def add_admin(self, user_id: int):
        if not await self.admins_col.find_one({'_id': user_id}):
            await self.admins_col.insert_one({'_id': user_id})
            return True
        return False

    async def remove_admin(self, user_id: int):
        await self.admins_col.delete_one({'_id': user_id})

    async def is_admin(self, user_id: int):
        if user_id == Config.OWNER_ID:
            return True
        return bool(await self.admins_col.find_one({'_id': user_id}))

    async def add_user(self, user_id: int):
        if not await self.users_col.find_one({'_id': user_id}):
            await self.users_col.insert_one({'_id': user_id})
            return True 
        return False

    async def get_settings(self):
        settings = await self.settings_col.find_one({'_id': 'bot_settings'})
        default_db = Config.DB_CHANNEL if Config.DB_CHANNEL != 0 else None
        default_log = Config.LOG_CHANNEL if Config.LOG_CHANNEL != 0 else None
        
        default_settings = {
            'active_db': default_db,
            'log_channel': default_log,
            'mode': 'public',
            'req_fsub': False,
            'auto_delete': 0,
            'shortlink_status': False,
            'shortlink_type': 'time',
            'verify_duration': 24,
            'bypass_credits': 3,
            'shortener_url': Config.SHORTENER_URL,
            'shortener_api': Config.SHORTENER_API,
            'tutorial_link': Config.TUTORIAL_LINK
        }
        
        if settings:
            for key, value in default_settings.items():
                if key not in settings or settings[key] is None:
                    settings[key] = value
            
            if not settings.get('active_db') and default_db:
                settings['active_db'] = default_db
            if not settings.get('log_channel') and default_log:
                settings['log_channel'] = default_log
                
            return settings
        return default_settings

    async def update_settings(self, key: str, value):
        await self.settings_col.update_one({'_id': 'bot_settings'}, {'$set': {key: value}}, upsert=True)

    # 🚀 SECURE UPDATE: Length changed to 50 for max security
    async def generate_unique_id(self, length=50):
        characters = string.ascii_letters + string.digits
        while True:
            unique_id = ''.join(secrets.choice(characters) for _ in range(length))
            if not await self.get_file(unique_id):
                return unique_id

    async def _insert_doc(self, doc):
        try:
            await self.files_col1.insert_one(doc)
        except Exception:
            if self.files_col2:
                try:
                    await self.files_col2.insert_one(doc)
                except Exception:
                    if self.files_col3:
                        await self.files_col3.insert_one(doc)

    async def save_file(self, message_id: int, chat_id: int, file_id: str, file_unique_id: str, caption: str = ""):
        unique_id = await self.generate_unique_id()
        doc = {'_id': unique_id, 't': 's', 'm': message_id, 'c': chat_id}
        if file_id: doc['f'] = file_id
        if file_unique_id: doc['u'] = file_unique_id
        if caption: doc['cap'] = caption
        await self._insert_doc(doc)
        return unique_id

    async def save_batch(self, first_id: int, last_id: int, chat_id: int):
        unique_id = await self.generate_unique_id()
        doc = {'_id': unique_id, 't': 'b', 'f_id': first_id, 'l_id': last_id, 'c': chat_id}
        await self._insert_doc(doc)
        return unique_id

    async def check_file_exists(self, file_unique_id: str):
        if not file_unique_id: return None
        doc = await self.files_col1.find_one({'u': file_unique_id})
        if not doc and self.files_col2: doc = await self.files_col2.find_one({'u': file_unique_id})
        if not doc and self.files_col3: doc = await self.files_col3.find_one({'u': file_unique_id})
        return doc

    async def get_file(self, unique_id: str):
        doc = await self.files_col1.find_one({'_id': unique_id})
        if not doc and self.files_col2: doc = await self.files_col2.find_one({'_id': unique_id})
        if not doc and self.files_col3: doc = await self.files_col3.find_one({'_id': unique_id})
        return doc

db = Database()
