import discord
from discord.ext import commands

class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("cog is ready")

    @commands.command()
    async def test(self, ctx):
        await ctx.respond('The cog works succesfully!')
        print(ea test works e)

def setup(bot):
    bot.add_cog(Test(bot))