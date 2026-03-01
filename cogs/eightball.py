import discord
from discord.ext import commands
from discord import app_commands
import random
from data.responses import responses
import os
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ask", description="Ask the magical all-knowing fortune teller a question.")
    async def magic_8ball(self, interaction: discord.Interaction, question: str):
        answer = random.choice(responses)
        await interaction.response.send_message(f'**Question:** {question}\n**Fortune Teller:** {answer}')

    @app_commands.command(name="8ball", description="Ask the slightly-less magical less all-knowing 8-ball a question.")
    async def gemini_8ball(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        if not GEMINI_API_KEY:
            await interaction.followup.send("Gemini API key not set", ephemeral=True)
            return
        prompt = f"""
        You are a mystical, playful, and wise 8-ball. Answer the following question in a fun, mysterious, and concise way, as if you are a magical fortune teller.
        Question: {question}
        """
        try:
            response = client.models.generate_content(model="gemini-1.5-flash",contents=prompt)
            answer = response.text.strip()
        except Exception as e:
            answer = f"Sorry, the fortune teller ran away (temporarily). ({e})"
        await interaction.followup.send(f'**Question:** {question}\n**8ball:** {answer}')

    @app_commands.command(name="future", description="Ask the crystal ball what will happen.")
    async def future(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        if not GEMINI_API_KEY:
            await interaction.followup.send("Gemini API key not set", ephemeral=True)
            return
        prompt = f"""
        You are a magical fortune teller's crystal ball. Given the following situation, predict what will happen next. Be imaginative, mysterious, and concise, as if you are peering into the mists of the future.
        Question: {question}
        """
        try:
            response = client.models.generate_content(model="gemini-1.5-flash",contents=prompt)
            answer = response.text.strip()
        except Exception as e:
            answer = f"Sorry, the crystal ball got struck by lightening (currently attempting to fix). ({e})"
        await interaction.followup.send(f'**Question:** {question}\n**Crystal Ball:** {answer}')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith('c'):
            if random.random() < 0.05:
                await message.channel.send('cookiesssssss')
        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(EightBall(bot))