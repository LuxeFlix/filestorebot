import aiohttp
from urllib.parse import quote

async def get_shortlink(url: str, api_url: str, api_key: str):
    if not api_url or not api_key:
        return url
        
    try:
        api_req_url = f"https://{api_url}/api?api={api_key}&url={quote(url)}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_req_url) as response:
                data = await response.json()
                if data.get("status") == "success" or str(data.get("status")) == "200":
                    return data.get("shortenedUrl")
                elif "shortenedUrl" in data:
                    return data.get("shortenedUrl")
    except Exception as e:
        print(f"Shortener API Error: {e}")
        
    return url
