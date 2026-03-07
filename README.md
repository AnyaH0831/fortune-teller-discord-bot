## What is it
We made a Discord bot that is a fortune teller. This was based off of our friend who we call "Fortune Teller" (so it basically replaces her as a fortune teller :D). The 8ball has responses based off of her exact texts.

## How to use
The bot uses slash commands:
- birthsign: See the sign associated with your birth month
- compatibility: See your compatability with other birth signs
- horoscope: See your horoscope for today
- matches: See all compability matches with your birth sign
- zodiac: Find out your zodiac birth sign
- 8ball: Ask the 8ball your burning questions (Based off of our friend)
- ask: Ask the magical fortune teller (Groq) your burning questions and get a smarter answer than the 8ball
- happy: Ask the happy bot and be overwhelmed by its optimism.
- atl: Ask the happy bot to find out all the "at least"s
- decide: The fortune teller helps you make decisions
- future: See the future through the crystal ball!
- image: Find out what an image says about you.
- palm: Have the fortune teller read your palm.

## How it was made
We used Python to write the commands, and Oracle to host it. The horoscopes are taken from a database, and the "ask"-type commands use Groq. The 8ball command uses a database of answers taken from our friend's texts (so it basically talks exactly like her).

## ORACLE command
screen -S discordbot
python3 bot.py

## Check it out
Check it out at this server (just go to the channel called hack-club-testing): https://discord.gg/xAuaZXUQtc