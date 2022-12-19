import discord
from discord import option

#cfc = 0x2681b4 #<- default color
#cfc = 0xcc8d0e # <- halloween color
cfc = 0x00771d # <- christmas color
errorc = 0xFF0000

class DevCommands(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    dev = discord.SlashCommandGroup(name="dev", description="Commands for developers.")

    @dev.command(name="reload_cogs")
    #@option(name="cogs", description="Reload the provided cogs.")
    async def reloadCogs(self, ctx):
        if 668874138160594985 == ctx.author.id:
            cogs = [
            "listeners",
            "dev",
            "admin",
            "fun",
            "level",
            "utility",
            "va"
            ]
            for cog in cogs:
                self.bot.reload_extension(f"cogs.{cog}")
            embed = discord.Embed(title="All cogs reloaded!", description=f"""
Following cogs:
```py
{cogs}
```
            """, color=cfc)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="Error 403!", description="You're not a developer, so you can't use this command!", colour=errorc)
            await ctx.respond(embed=embed)

    @dev.command(name="defertest")
    async def deferTest(self, ctx):
        if 668874138160594985 == ctx.author.id:
            await ctx.defer()
            await ctx.respond("It works. Hallelujah!")
        else:
            embed = discord.Embed(title="Error 403!", description="You're not a developer, so you can't use this command!", colour=errorc)
            await ctx.respond(embed=embed)
    
def setup(bot):
    bot.add_cog(DevCommands(bot))
