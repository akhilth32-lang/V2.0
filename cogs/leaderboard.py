import discord
from discord.ext import commands, tasks
from utils.db import get_collection
from utils.embeds import build_leaderboard
from utils.coc_client import fetch_top5000

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_global.start()

    def cog_unload(self):
        self.update_global.cancel()

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx, page: int = 1):
        """Show the leaderboard"""
        collection = get_collection("players")
        players = await collection.find().to_list(length=5000)
        embed = build_leaderboard(players, page=page)
        await ctx.send(embed=embed)

    @tasks.loop(hours=24)
    async def update_global(self):
        """Daily fetch top 5000 legend players"""
        players = await fetch_top5000()
        collection = get_collection("players")
        for p in players:
            await collection.update_one({"tag": p["tag"]}, {"$set": p}, upsert=True)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
