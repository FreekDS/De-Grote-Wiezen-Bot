import discord

from DiscordWiezer import DiscordWiezer
from Game import Game
from discord.ext import commands


class WiezenBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = Game()
        self.players: list = []

    @commands.command(name='wiezen')
    async def wiezen(self, ctx, *spelers):
        if len(spelers) != 3:
            await ctx.send("mateke ge moet wel me vier zijn hé")
        else:
            self.game.add_player(DiscordWiezer(ctx.author,True))
            self.players.append(ctx.author)
            for speler in spelers:
                user = discord.utils.find(lambda m: m.id == int(speler[3:-1]), ctx.guild.members)
                if user:
                    self.game.add_player(DiscordWiezer(user,False))
                    self.players.append(user)
            await self.game.start_game()
            if len(self.players) < 4:
                ctx.send("Mateke, das hier ni koosjer en ni halal zenne, te weinig volk")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return
        if type(msg.channel) is not discord.DMChannel:
            return
        if msg.author not in self.players:
            await msg.author.send("Gij speelt ni mee he vriendschap")
            return
        await self.game.perform_action(self.game.get_wiezen_speler(str(msg.author.id)), msg.content)
