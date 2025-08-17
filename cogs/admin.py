import discord
from discord.ext import commands
from utils.db import get_collection

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name="remove")
    async def remove(self, ctx, tag: str):
        """Admin command: remove player by tag"""
        collection = get_collection("players")
        result = await collection.delete_one({"tag": tag})
        if result.deleted_count == 0:
            await ctx.send("⚠ Player not found.")
        else:
            await ctx.send(f"✅ Player {tag} removed from database.")

async def setup(bot):
    await bot.add_cog(Admin(bot))
