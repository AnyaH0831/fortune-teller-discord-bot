import discord
from discord.ext import commands
from discord import app_commands
import os
from groq import AsyncGroq

# DECISION MAKERRRRRRRR

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = AsyncGroq(api_key=GROQ_API_KEY)

class Happy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="happy", description="Describe a situation and see the bright side!")
    async def happy(self, interaction: discord.Interaction, situation: str):
        await interaction.response.defer()
        if not GROQ_API_KEY:
            await interaction.followup.send("Groq API key not set.", ephemeral=True)
            return
        try:
            response = await client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an extremely enthusiastic and relentlessly optimistic hype person. No matter what situation the user describes, no matter how bad, you find the the most positive, uplifting, and encouraging outlook possible. Be warm, energetic, and sincere. Answer in at most 3 sentences."},
                    {"role": "user", "content": situation}
                ],
                max_tokens=200
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"Even the optimism bot hit a wall... it's okay, it'll bounce back!"
        await interaction.followup.send(f"**{interaction.user.display_name}:** {situation}\n**Happy Bot:** {answer}")

    @app_commands.command(name="atl", description="Describe a situation and get a list of 'At least...'!")
    async def atl(self, interaction: discord.Interaction, situation: str):
        await interaction.response.defer()
        if not GROQ_API_KEY:
            await interaction.followup.send("Groq API key not set.", ephemeral=True)
            return
        try:
            response = await client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an optimism bot. The user will describe a situation. Your job is to respond with a paragraph of sentences starting with 'At least...' statements, each one finding a tiny, funny, or genuine good things in the situation. Answer in at most 3 sentences. Format each one on its own line starting with 'At least'. Be creative, funny, and a little absurd."},
                    {"role": "user", "content": situation}
                ],
                max_tokens=200
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"At least the bot tried its best..."
        await interaction.followup.send(f"**{interaction.user.display_name}:** {situation}\n\n{answer}")

async def setup(bot):
    await bot.add_cog(Happy(bot))
