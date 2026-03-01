
import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

COGS = ["cogs.eightball", "cogs.astrology", "cogs.zodiac"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def main():
    async with bot:
        for cog in COGS:
            await bot.load_extension(cog)
            print(f"Loaded {cog}")
        await bot.start(config.TOKEN)

import asyncio
asyncio.run(main())