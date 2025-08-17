import discord
from discord.ext import commands
import datetime

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Check bot latency"""
        await ctx.send(f"🏓 Pong! `{round(self.bot.latency * 1000)}ms`")

    @commands.command(name="showtime")
    async def showtime(self, ctx):
        """Show current UTC and IST time"""
        now = datetime.datetime.utcnow()
        ist = now + datetime.timedelta(hours=5, minutes=30)
        embed = discord.Embed(title="🕒 Current Time", color=discord.Color.green())
        embed.add_field(name="UTC", value=now.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="IST", value=ist.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="assignrole")
    async def assign_role(self, ctx, user: discord.Member, role: discord.Role, region: str):
        """Assign a role and show region message (Global/India)"""
        await user.add_roles(role)
        base_link = "https://example.com/access"  # TODO: replace with real base link
        msg = f"✅ {user.mention} given role {role.mention}\n"
        if region.lower() == "global":
            msg += f"🌍 Global access link: {base_link}?user={user.id}"
        elif region.lower() == "india":
            msg += f"🇮🇳 India access link: {base_link}?user={user.id}"
        else:
            msg += "⚠ Unknown region, use `Global` or `India`"
        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(General(bot))
