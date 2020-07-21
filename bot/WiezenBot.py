import discord
from discord.ext import commands


class WiezenBot(commands.Cog):
    def __init__(self, bot,client):
        self.bot = bot

    @commands.command(name='wiezen')
    async def wiezen(self, ctx, *spelers):
        if (len(spelers) != 3):
            await ctx.send("mateke ge moet wel me vier zijn hé")
        else:
            for speler in spelers:
                user=discord.utils.find(lambda m:m.id==int(speler[3:-1]),ctx.guild.members)
                # user = discord.utils.get(ctx.guild.members, id=speler)
                await user.send("wiezen wiezen wiezen wis wis wis")
            await ctx.author.send("wiezen wiezen wiezen wis wis wis")

    @commands.command(name='speel')
    async def speel(self,ctx, kaard):
        pass

