# === audioop bypass ===
import sys, types
if 'audioop' not in sys.modules:
    audioop = types.ModuleType('audioop')
    def _stub(*args, **kwargs): return None
    audioop.add = audioop.mul = audioop.bias = audioop.tostereo = _stub
    audioop.tomono = audioop.findfactor = audioop.findfit = audioop.findmax = _stub
    audioop.avg = audioop.max = audioop.minmax = audioop.rms = audioop.avgpp = _stub
    audioop.cross = audioop.mulmul = _stub
    audioop.ratecv = lambda *a, **k: (b"", None)
    sys.modules['audioop'] = audioop

# === standard imports ===
import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from keep_alive import keep_alive
import asyncio
import importlib
import glob
import logging
from utils.db import init_db, reset_offence_defence_daily

# === logging ===
logging.basicConfig(level=logging.INFO)

# === load env ===
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
COC_PROXY = os.getenv("COC_PROXY")  # for clash API proxy

# === intents ===
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# === bot init ===
bot = commands.Bot(command_prefix="!", intents=intents)

# === database ===
db = init_db(MONGO_URI)

# === load all commands dynamically from commands/ ===
async def load_commands():
    for file in glob.glob("commands/*.py"):
        if file.endswith(".py") and not file.endswith("__init__.py"):
            module_name = file.replace("/", ".").replace("\\", ".")[:-3]
            try:
                await bot.load_extension(module_name)
                logging.info(f"✅ Loaded {module_name}")
            except Exception as e:
                logging.error(f"❌ Failed to load {module_name}: {e}")

# === on ready ===
@bot.event
async def on_ready():
    logging.info(f"Bot is online as {bot.user}")
    reset_task.start()

# === daily reset task ===
@tasks.loop(minutes=1)
async def reset_task():
    """Resets offence/defence data daily at 10:30 AM IST (UTC+5:30)."""
    import datetime
    from pytz import timezone
    now = datetime.datetime.now(timezone("Asia/Kolkata"))
    if now.hour == 10 and now.minute == 30:
        await reset_offence_defence_daily(db)

# === main run ===
async def main():
    keep_alive()  # flask keep-alive server
    async with bot:
        await load_commands()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
