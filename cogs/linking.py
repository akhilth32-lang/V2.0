import discord
from discord.ext import commands
from utils.db import get_collection

class Linking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="link")
    async def link(self, ctx, tag: str):
        """Link Clash of Clans account"""
        collection = get_collection("players")
        existing = await collection.find_one({"tag": tag})
        if existing:
            return await ctx.send("⚠ This account is already linked!")

        await collection.insert_one({
            "discord_id": ctx.author.id,
            "tag": tag,
            "trophies": 0,
            "offence": "0/0",
            "defence": "0/0"
        })
        await ctx.send(f"✅ Linked {tag} to {ctx.author.mention}")

    @commands.command(name="unlink")
    async def unlink(self, ctx):
        """Unlink Clash of Clans account"""
        collection = get_collection("players")
        result = await collection.delete_one({"discord_id": ctx.author.id})
        if result.deleted_count == 0:
            await ctx.send("⚠ You don’t have any linked account.")
        else:
            await ctx.send("✅ Account unlinked successfully.")

async def setup(bot):
    await bot.add_cog(Linking(bot))
