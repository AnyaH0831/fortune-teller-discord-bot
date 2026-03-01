import discord

def base_embed(title: str, color: discord.Color = discord.Color.dark_purple()) -> discord.Embed:
    return discord.Embed(title=title, color=color)

def error_embed(message: str) -> discord.Embed:
    embed = discord.Embed(title="Error", description=message, color=discord.Color.red())
    return embed

def success_embed(title: str, description: str) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=discord.Color.green())
    return embed