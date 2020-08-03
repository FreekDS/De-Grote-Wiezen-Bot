import discord
from bot.DiscordWiezer import DiscordWiezer
from discord import File
from wiezenlibrary.Game import Game, GameState
from discord.ext import commands


class WiezenBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = Game(bot)
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
        if msg == 'reset':
            self.game.reset()
            await self.game.start_game()
        await self.game.perform_action(self.game.get_wiezen_speler(str(msg.author.id)), msg.content)

    @commands.command(name='hoewiezik')
    async def wiezen(self, ctx,):
        with open("assets/markdowns/HoeTFWiezIk.md",'r') as fileke:
            await ctx.send(fileke.read())

    @commands.command(name='help')
    async def help(self,ctx):
        with open('assets/boei.jpg', 'rb') as fileke:
            await ctx.send("hier is hulp")
            await ctx.send(file=discord.File(fileke))
            with open("assets/markdowns/help.md", 'r') as help:
                await ctx.send(help.read())

