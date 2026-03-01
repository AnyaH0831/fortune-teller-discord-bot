import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

# COGS = ["cogs.eightball", "cogs.astrology", "cogs.zodiac"]
COGS = ["cogs.astrology"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    await bot.tree.sync()

@bot.event
async def on_demand_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command. Try `!help`")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument. Usage: `{ctx.prefix}{ctx.command.name}`")

async def main():
    async with bot: 
        for cog in COGS:
            await bot.load_extension(cog)
            print(f"Loaded {cog}")
        await bot.start(config.TOKEN)

import asyncio
asyncio.run(main())