import discord
from discord import app_commands
from discord.ext import commands
from data.horoscopes import ZODIAC_DATA
from data.compatibility import get_compatibility
from utils.zodiac_helpers import get_zodiac_sign, get_sign_emoji
from utils.embeds import error_embed
import aiohttp

ALL_SIGNS = list(ZODIAC_DATA.keys())

SIGN_CHOICES = [
    app_commands.Choice(name=sign.capitalize(), value=sign)
    for sign in ALL_SIGNS
]


class Astrology(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="zodiac", description="Get info about a zodiac sign.")
    @app_commands.describe(sign="The zodiac sign to look up.")
    @app_commands.choices(sign=SIGN_CHOICES)
    async def zodiac(self, interaction: discord.Interaction, sign: str):
        sign = sign.lower().strip()
        if sign not in ZODIAC_DATA:
            await interaction.response.send_message(embed=error_embed(f"Unknown sign `{sign}`. Try one of: {', '.join(ALL_SIGNS)}"), ephemeral=True)
            return
        data = ZODIAC_DATA[sign]
        embed = discord.Embed(
            title=f"{data['symbol']} {sign.capitalize()}",
            description=data["description"],
            color=discord.Color.dark_purple()
        )
        embed.add_field(name="Dates", value=data["dates"], inline=True)
        embed.add_field(name="Element", value=data["element"], inline=True)
        embed.add_field(name="Ruling Planet", value=data["ruling_planet"], inline=True)
        await interaction.response.send_message(embed=embed)
                    
    @app_commands.command(name="birthsign", description="Get your zodiac sign from your birthday.")
    @app_commands.describe(month="Your birth month (1-12)", day="Your birth day (1-31)")
    async def birthsign(self, interaction: discord.Interaction, month: int, day: int):
        try:
            sign = get_zodiac_sign(month, day)
        except Exception:
            await interaction.response.send_message(embed=error_embed("Invalid date. Please provide a valid month (1-12) and day (1-31)."), ephemeral=True)
            return
        emoji = get_sign_emoji(sign)
        data = ZODIAC_DATA[sign.lower()]
        embed = discord.Embed(
            title=f"{emoji} Your Sign: {sign}",
            description=data["description"],
            color=discord.Color.purple()
        )

        embed.add_field(name="Dates", value=data["dates"], inline=True)
        embed.add_field(name="Element", value=data["element"], inline=True)
        embed.add_field(name="Ruling Planet", value=data["ruling_planet"], inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="compatibility", description="Check compatibility between two zodiac signs.")
    @app_commands.describe(sign1="The first zodiac sign.", sign2="The second zodiac sign.")
    @app_commands.choices(sign1=SIGN_CHOICES, sign2=SIGN_CHOICES)
    async def compatibility(self, interaction: discord.Interaction, sign1: str, sign2: str):
        sign1, sign2 = sign1.lower().strip(), sign2.lower().strip()

        if sign1 not in ZODIAC_DATA:
            await interaction.response.send_message(embed=error_embed(f"Unknown sign `{sign1}`."), ephemeral=True)
            return
        if sign2 not in ZODIAC_DATA:
            await interaction.response.send_message(embed=error_embed(f"Unknown sign `{sign2}`."), ephemeral=True)
            return

        score, reason = get_compatibility(sign1, sign2)
        stars = "⭐" * score + "🌑" * (10 - score)

        d1, d2 = ZODIAC_DATA[sign1], ZODIAC_DATA[sign2]
        embed = discord.Embed(
            title=f"{d1['symbol']} {sign1.capitalize()} + {d2['symbol']} {sign2.capitalize()}",
            description=reason,
            color=discord.Color.magenta()
        )
        embed.add_field(name="Compatibility Score", value=f"{stars} **{score}/10**", inline=False)
        embed.add_field(name="Elements", value=f"{d1['element']} + {d2['element']}", inline=True)
        embed.add_field(name="Planets", value=f"{d1['ruling_planet']} + {d2['ruling_planet']}", inline=True)
        embed.set_footer(text="Use /zodiac to learn more about each sign.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="horoscope", description="Get today's horoscope reading.")
    @app_commands.describe(sign="Your zodiac sign.")
    @app_commands.choices(sign=SIGN_CHOICES)
    async def horoscope(self, interaction: discord.Interaction, sign: str):
        sign = sign.lower().strip()
        if sign not in ZODIAC_DATA:
            await interaction.response.send_message(embed=error_embed(f"Unknown sign `{sign}`. Try: {', '.join(ALL_SIGNS)}"), ephemeral=True)
            return

        await interaction.response.defer()

        url = f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign={sign}&day=today"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        await interaction.followup.send(embed=error_embed("Couldn't fetch today's horoscope. Try again later."))
                        return
                    json_data = await resp.json(content_type=None)
                    horoscope_text = json_data.get("horoscope", "The stars are silent today.")
        except Exception:
            await interaction.followup.send(embed=error_embed("Failed to connect to the horoscope service. Try again later."))
            return

        data = ZODIAC_DATA[sign]
        embed = discord.Embed(
            title=f"{data['symbol']} Daily Horoscope: {sign.capitalize()}",
            description=horoscope_text,
            color=discord.Color.blurple()
        )
        embed.add_field(name="Element",       value=data["element"],       inline=True)
        embed.add_field(name="Ruling Planet", value=data["ruling_planet"], inline=True)
        embed.set_footer(text="The stars speak — will you listen?")
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Astrology(bot))