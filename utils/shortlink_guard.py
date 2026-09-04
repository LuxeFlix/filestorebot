import orjson
import base64
import hashlib
from config import Config

class ShortlinkGuard:
    
    @staticmethod
    def generate_signature(token: str) -> str:
        """Generates a cryptographic signature to verify Cloudflare traffic"""
        secret = Config.GUARD_SECRET
        raw_string = f"{token}{secret}".encode('utf-8')
        return hashlib.sha256(raw_string).hexdigest()[:16]

    @staticmethod
    def generate_cf_url(token: str, api_url: str, api_key: str, bot_username: str, bypass_time: int) -> str:
        """Generates the base64 payload URL for Cloudflare Worker"""
        if not Config.GUARD_URL:
            return None
            
        try:
            data = {
                "t": token,          
                "u": api_url,        
                "k": api_key,        
                "b": bot_username,   
                "w": bypass_time     
            }
            
            # 🚀 Fastest Payload Generator: orjson implementation
            json_data = orjson.dumps(data)
            b64_data = base64.urlsafe_b64encode(json_data).decode('utf-8').rstrip("=")
            
            final_payload = f"{b64_data}.luxe"
            return f"{Config.GUARD_URL.rstrip('/')}/i?_v={final_payload}"

        except Exception as e:
            print(f"Web Guard Generation Error: {e}")
            return None
