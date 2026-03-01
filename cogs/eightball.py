import discord
from discord.ext import commands
import random
from data.responses import responses

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball")
    async def magic_8ball(self, ctx, *, question: str):
        answer = random.choice(responses)
        await ctx.send(f'**Question:** {question}\n**Answer:** {answer}')

async def setup(bot):
    await bot.add_cog(EightBall(bot))