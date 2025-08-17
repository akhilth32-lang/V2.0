import aiohttp
import os

# Clash of Clans API Proxy link from Render env vars
COC_API_URL = os.getenv("COC_PROXY_URL", "https://api.clashofclans.com/v1")

# Global Legends endpoint (top 5000 players)
TOP5000_ENDPOINT = "/leagues/29000022/seasons/latest"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('COC_API_TOKEN', '')}"
}

async def fetch_top5000():
    """Fetch top 5000 global legend players"""
    url = f"{COC_API_URL}{TOP5000_ENDPOINT}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status != 200:
                return []
            data = await resp.json()
            players = []
            for p in data.get("items", []):
                players.append({
                    "tag": p.get("tag"),
                    "name": p.get("name"),
                    "trophies": p.get("trophies"),
                    "offence": "0/0",  # Will reset daily
                    "defence": "0/0"
                })
            return players
