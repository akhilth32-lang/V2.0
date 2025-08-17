import discord
import math

def build_leaderboard(players, page=1, per_page=10):
    """Build leaderboard embed"""
    total_pages = math.ceil(len(players) / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    sliced = players[start:end]

    embed = discord.Embed(
        title=f"🏆 Leaderboard (Page {page}/{total_pages})",
        color=discord.Color.gold()
    )

    if not sliced:
        embed.description = "⚠ No players to show."
        return embed

    desc = ""
    for idx, p in enumerate(sliced, start=start+1):
        desc += (
            f"**{idx}. {p.get('name','Unknown')} ({p.get('tag')})**\n"
            f"🏆 {p.get('trophies',0)} | "
            f"⚔ Offence: {p.get('offence','0/0')} | "
            f"🛡 Defence: {p.get('defence','0/0')}\n\n"
        )

    embed.description = desc
    return embed
