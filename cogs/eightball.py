import discord
from discord.ext import commands
from discord import app_commands
import random
from data.responses import responses
import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

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
            model = genai.GenerativeModel('gemini-2.5-pro')
            response = model.generate_content(prompt)
            answer = response.text.strip()
        except Exception as e:
            answer = f"Sorry, the fortune teller ran away (temporarily). ({e})"
        await interaction.followup.send(f'**Question:** {question}\n**8ball:** {answer}')

        @commands.Cog.listener()
        async def on_message(self, message):
            if message.author.bot:
                return
            if message.content.startswith('c'):
                if random.random() < 0.05:
                    await message.channel.send('cookiesssssss')

async def setup(bot):
    await bot.add_cog(EightBall(bot))