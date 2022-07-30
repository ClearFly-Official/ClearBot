import discord
from discord.ext import commands

class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("cog is ready")

def setup(bot):
    bot.add_cog(Test(bot))