# === Audioop bypass for environments where audioop is missing ===
import sys, types
if "audioop" not in sys.modules:
    audioop = types.ModuleType("audioop")
    def _nop(*args, **kwargs): return None
    audioop.add = audioop.mul = audioop.tomono = audioop.tostereo = _nop
    audioop.bias = audioop.reverse = audioop.ratecv = audioop.lin2lin = _nop
    audioop.lin2ulaw = audioop.ulaw2lin = audioop.lin2alaw = audioop.alaw2lin = _nop
    audioop.avg = audioop.max = audioop.minmax = audioop.rms = audioop.cross = _nop
    sys.modules["audioop"] = audioop

import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from utils.db import get_mongo_client

# === Bot setup ===
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# === Load cogs dynamically ===
initial_cogs = [
    "cogs.general",
    "cogs.leaderboard",
    "cogs.linking",
    "cogs.admin"
]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    for cog in initial_cogs:
        try:
            await bot.load_extension(cog)
            print(f"🔹 Loaded cog: {cog}")
        except Exception as e:
            print(f"❌ Failed to load {cog}: {e}")

# === Keep-alive for Render ===
keep_alive()

# === Run bot ===
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ DISCORD_BOT_TOKEN not set in environment!")
bot.run(TOKEN)
