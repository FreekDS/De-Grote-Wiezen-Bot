from discord.ext import commands


class WiezenBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wiezen')
    async def WiezenBot(self, ctx,arg=None):
        await ctx.send("wiezen wiezen wiezen wiezen wis wis wis wis")
