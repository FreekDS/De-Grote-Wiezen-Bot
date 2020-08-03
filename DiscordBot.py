"""
     ---------------------------------------
    | Created by:                           |
    | Thibaut Van Goethem & Freek De Sagher |
     ---------------------------------------
"""

# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# from Donut import Donut

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=',', help_command=None)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


if __name__ == '__main__':
    from bot.WiezenBot import WiezenBot

    bot.add_cog(WiezenBot(bot))
    # Donut is vervallen :(
    # bot.add_cog(Donut(bot))
    bot.run(TOKEN)
