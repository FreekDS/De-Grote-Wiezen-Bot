import discord
from discord.ext import commands

from DiscordWiezen import DiscordWiezen
from bot.DiscordWiezer import DiscordWiezer


class WiezenBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = DiscordWiezen(bot,self)
        self.players: list = []
        self.debug=False

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
            self.game.start_game()
        temp= msg.content.split()
        test=len(msg.content.split())
        if not self.debug or not len(msg.content.split())>1:
                self.game.perform_action(self.game.get_wiezen_speler(str(msg.author.id)), msg.content)
        else:
            self.game.perform_action(self.game.get_wiezen_speler(str(msg.author.id), int(msg.content.split()[1])), msg.content.split()[0])

    @commands.command(name='wiezen')
    async def wiezen(self, ctx, *spelers):
        if len(spelers) != 3:
            await ctx.send("mateke ge moet wel me vier zijn hé")
        else:
            self.game = DiscordWiezen(self.bot, self)
            self.game.add_player(DiscordWiezer(ctx.author, True))
            self.players.append(ctx.author)
            for speler in spelers:
                user = discord.utils.find(lambda m: m.id == int(speler[3:-1]), ctx.guild.members)
                if user:
                    self.game.add_player(DiscordWiezer(user, False))
                    self.players.append(user)
            self.game.start_game()
            if len(self.players) < 4:
                ctx.send("Mateke, das hier ni koosjer en ni halal zenne, te weinig volk")

    @commands.command(name='wiezen_debug')
    async def wiezen_debug(self, ctx, *spelers):
        if len(spelers) != 3:
            await ctx.send("mateke ge moet wel me vier zijn hé")
        else:
            self.debug = True
            self.game = DiscordWiezen(self.bot, self)
            self.game.add_player(DiscordWiezer(ctx.author, True))
            self.players.append(ctx.author)
            for speler in spelers:
                user = discord.utils.find(lambda m: m.id == int(speler[3:-1]), ctx.guild.members)
                if user:
                    self.game.add_player(DiscordWiezer(user, False))
                    self.players.append(user)
            self.game.start_game()
            if len(self.players) < 4:
                ctx.send("Mateke, das hier ni koosjer en ni halal zenne, te weinig volk")

    @commands.command(name='hoewiezik')
    async def how_to_wiez(self, ctx):
        with open("assets/markdowns/HoeTFWiezIk1.md",'r') as fileke:
            await ctx.send(fileke.read())
        with open("assets/markdowns/HoeTFWiezIk2.md", 'r') as fileke:
            await ctx.send(fileke.read())

    @commands.command(name='help')
    async def help(self,ctx):
        with open('assets/boei.jpg', 'rb') as fileke:
            await ctx.send("hier is hulp")
            await ctx.send(file=discord.File(fileke))
            with open("assets/markdowns/help.md", 'r') as help:
                await ctx.send(help.read())

    def stop(self,toremove):
        self.game = DiscordWiezen(self.bot, self)

