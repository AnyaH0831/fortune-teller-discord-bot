import discord
from discord.ext import commands
from discord import app_commands
import random
from data.responses import responses

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ask", description="Ask the magical all-knowing fortune teller a question.")
    async def magic_8ball(self, interaction: discord.Interaction, question: str):
        answer = random.choice(responses)
        await interaction.response.send_message(f'**Question:** {question}\n**Answer:** {answer}')

async def setup(bot):
    await bot.add_cog(EightBall(bot))