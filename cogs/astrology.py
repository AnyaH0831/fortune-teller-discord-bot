import discord
from discord.ext import commands
from data.horoscopes import ZODIAC_DATA
from data.compatibility import get_compatibility 
from utils.zodiac_helpers import get_zodiac_sign, get_sign_emoji
from utils.embeds import error_embed
import random

ALL_SIGNS = list(ZODIAC_DATA.keys())

class Astrology(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="zodiac")
    async def zodiac(self, ctx, *, sign:str):
        """Get info about a zodiac sign. Usage: !zodiac scorpio"""
        sign = sign.lower().strip()
        if sign not in ZODIAC_DATA:
            await ctx.send(embed=error_embed(f"Unknown sign `{sign}`. Try one of: {', '.join(ALL_SIGNS)}"))
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
        await ctx.send(embed=embed)
    
    @commands.command(name="birthsign")
    async def birthsign(self, ctx, month: int, day: int):
        """Get your zodiac sign from your birthday. Usage: !birthsign 10 31"""
        try:
            sign = get_zodiac_sign(month, day)
        except Exception:
            await ctx.send(embed=error_embed("Invalid date. Usage: `!birthsign <month> <day>` e.g. `!birthsign 10 31`"))
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
        await ctx.send(embed=embed)

    @commands.command(name="compatibility")
    async def compatibility(self, ctx, sign1: str, sign2: str):
        """Check compatibility between two signs. Usage: !compatibility aries scorpio"""
        sign1, sign2 = sign1.lower().strip(), sign2.lower().strip()

        if sign1 not in ZODIAC_DATA:
            await ctx.send(embed=error_embed(f"Unknown sign `{sign1}`."))
            return
        if sign2 not in ZODIAC_DATA:
            await ctx.send(embed=error_embed(f"Unknown sign `{sign2}`."))
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
        embed.set_footer(text="Use !zodiac <sign> to learn more about each sign.")
        await ctx.send(embed=embed)
    
    @commands.command(name="horoscope")
    async def horoscope(self, ctx, *, sign: str):
        """Get a mystical horoscope reading. Usage: !horoscope pisces"""
        sign = sign.lower().strip()
        if sign not in ZODIAC_DATA:
            await ctx.send(embed=error_embed(f"Unknown sign `{sign}`. Try: {', '.join(ALL_SIGNS)}"))
            return 
        
        data = ZODIAC_DATA[sign]
        readings = [
            f"The stars align in your favor today, {sign.capitalize()}. Trust your instincts — a new opportunity is closer than you think.",
            f"Mercury's energy surrounds you, {sign.capitalize()}. It's a powerful day to speak your truth and let go of what no longer serves you.",
            f"The cosmos are asking you to slow down, {sign.capitalize()}. Reflection will reveal the answer you've been searching for.",
            f"A unexpected connection may shift your path today, {sign.capitalize()}. Stay open to what the universe is sending your way.",
            f"Your ruling planet {data['ruling_planet']} is working in your favor. Bold moves made today will ripple far into your future.",
            f"The moon whispers of transformation, {sign.capitalize()}. What you release now will make space for something beautiful.",
            f"Pay attention to your dreams and gut feelings today, {sign.capitalize()}. The universe is communicating something important.",
            f"Creativity flows through you like a current, {sign.capitalize()}. Channel that {data['element']} energy into something that matters.",
        
        ]
        
        embed = discord.Embed(
            title=f"{data['symbol']} Daily Horoscope: {sign.capitalize()}",
            description=random.choice(readings),
            color=discord.Color.blurple()
        )

        embed.add_field(name="Element",       value=data["element"],       inline=True)
        embed.add_field(name="Ruling Planet", value=data["ruling_planet"], inline=True)
        embed.set_footer(text="The stars speak — will you listen?")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Astrology(bot))