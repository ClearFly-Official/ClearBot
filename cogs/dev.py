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
    async def reloadCogs(self, ctx):
        if 668874138160594985 == ctx.author.id:
            cogs = [
            "admin",
            "dev",
            "fun",
            "level",
            "listeners",
            "utility",
            "va"
            ]
            class CogSelectView(discord.ui.View):
                def __init__(self, bot):
                    self.bot = bot
                    super().__init__(timeout=20.0)

                @discord.ui.select(
                    placeholder="Cogs",
                    min_values=1,
                    max_values=7,
                    options = [
                        discord.SelectOption(
                            label=cogs[0],
                            emoji="🔒"
                        ),
                        discord.SelectOption(
                            label=cogs[1],
                            emoji="💻"
                        ),
                        discord.SelectOption(
                            label=cogs[2],
                            emoji="🧩"
                        ),
                        discord.SelectOption(
                            label=cogs[3],
                            emoji="🏆"
                        ),
                        discord.SelectOption(
                            label=cogs[4],
                            emoji="🛠️"
                        ),
                        discord.SelectOption(
                            label=cogs[5],
                            emoji="✈️"
                        )
                    ]
                )
                async def select_callback(self, select, interaction):
                    if 668874138160594985 == ctx.author.id:
                        for cog in select.values:
                            self.bot.reload_extension(f"cogs.{cog}")
                        embed = discord.Embed(title="Selected cogs have been reloaded!", description=f"""
Reloaded cogs:
```py
{cogs}
```
                        """, color=cfc)
                        await ctx.respond(embed=embed, view=CogSelectView(bot=self.bot))
                    else:
                        embed = discord.Embed(title="Error 403!", description="You're not a developer, so you can't use this command!", colour=errorc)
                        await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="Error 403!", description="You're not a developer, so you can't use this command!", colour=errorc)
            await ctx.respond(embed=embed)

    
def setup(bot):
    bot.add_cog(DevCommands(bot))
