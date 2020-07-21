import discord
from discord.ext import commands


class WiezenBot(commands.Cog):
    def __init__(self, bot, client):
        self.bot = bot
        self.players: list = []

    @commands.command(name='wiezen')
    async def wiezen(self, ctx, *spelers):
        if len(spelers) != 3:
            await ctx.send("mateke ge moet wel me vier zijn hé")
        else:
            self.players.append(ctx.author)
            for speler in spelers:
                user = discord.utils.find(lambda m: m.id == int(speler[3:-1]), ctx.guild.members)
                if user:
                    self.players.append(user)
            if len(self.players) < 4:
                ctx.send("Mateke, das hier ni koosjer en ni halal zenne, te weinig volk")

    @commands.command(name='speel')
    async def speel(self, ctx, kaard):
        pass
