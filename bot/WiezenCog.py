from discord.ext import commands
import discord
from discord.client import Member
from wiezenlibrary.Player import Player
from wiezenlibrary.BaseGame import BaseGame
import re


class WiezenCog(commands.Cog):
    def __init__(self, bot):
        self.game = BaseGame()
        self.bot = bot

    @commands.command("wiezen")
    async def start_game(self, ctx, *players):
        print(players, ctx)
        players = list(players)
        wiezen_players = list()
        first: Member or None = None
        if len(players) == 3:
            first = ctx.author
        elif len(players) == 4:
            first = players.pop(0)
        else:
            pass

        name = first.nick if first.nick is not None else first.name
        wiezen_players.append(Player(name, first.id, True))

        for player in players:
            pass

    def get_member_object(self, player: str, members) -> Member:
        check = re.match('<@![0-9]+>', player)
        if not check:
            raise Exception("No")
        user: Member
        user = discord.utils.get(members, id=int(player[3:-1]))
        if user:
            return user
        else:
            raise Exception("No 2")
