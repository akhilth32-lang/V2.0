import discord
from discord import app_commands
from discord.ext import commands
import datetime
import pytz

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /ping command
    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: `{latency} ms`",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    # /showtime command
    @app_commands.command(name="showtime", description="Show current IST time")
    async def showtime(self, interaction: discord.Interaction):
        now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        embed = discord.Embed(
            title="🕒 Current Time (IST)",
            description=now.strftime("%d %B %Y, %I:%M %p"),
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    # /assignrole command
    @app_commands.command(name="assignrole", description="Assign a role to a user (Global/India)")
    @app_commands.describe(user="Select a user", role="Select a role", region="Choose Global or India")
    @app_commands.choices(region=[
        app_commands.Choice(name="Global", value="Global"),
        app_commands.Choice(name="India", value="India")
    ])
    async def assignrole(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        role: discord.Role,
        region: app_commands.Choice[str]
    ):
        try:
            await user.add_roles(role)
            embed = discord.Embed(
                title="✅ Role Assigned",
                description=f"User: {user.mention}\nRole: {role.mention}\nRegion: **{region.value}**",
                color=discord.Color.purple()
            )
            embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)

            # Send base link depending on region
            if region.value == "Global":
                await interaction.followup.send(f"🌍 Access link for {user.mention}: https://example.com/global/{user.id}")
            else:
                await interaction.followup.send(f"🇮🇳 Access link for {user.mention}: https://example.com/india/{user.id}")

        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to assign role: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
