import discord
from discord import option

#cfc = 0x2681b4 #<- default color
#cfc = 0xcc8d0e # <- halloween color
cfc = 0x00771d # <- christmas color
errorc = 0xFF0000

devs = [668874138160594985, 871893179450925148]#Matt3o0#7010 & WolfAir#2755

class DevCommands(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    dev = discord.SlashCommandGroup(name="dev", description="Commands for developers.")

    @dev.command(name="reload_cogs")
    async def reloadCogs(self, ctx):
        if ctx.author.id in devs:
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
                            label=cogs[0].capitalize(),
                            emoji="🔒",
                            value=cogs[0]
                        ),
                        discord.SelectOption(
                            label=cogs[1].capitalize(),
                            emoji="💻",
                            value=cogs[1]
                        ),
                        discord.SelectOption(
                            label=cogs[2].capitalize(),
                            emoji="🧩",
                            value=cogs[2]
                        ),
                        discord.SelectOption(
                            label=cogs[3].capitalize(),
                            emoji="🏆",
                            value=cogs[3]
                        ),
                        discord.SelectOption(
                            label=cogs[4].capitalize(),
                            emoji="👂",
                            value=cogs[4]
                        ),
                        discord.SelectOption(
                            label=cogs[5].capitalize(),
                            emoji="🛠️",
                            value=cogs[5]
                        ),
                        discord.SelectOption(
                            label=cogs[6].upper(),
                            emoji="✈️",
                            value=cogs[6]
                        )
                    ]
                )
                async def select_callback(self, select, interaction):
                    if ctx.author.id in devs:
                        for cog in select.values:
                            self.bot.reload_extension(f"cogs.{cog}")
                        embed = discord.Embed(title="Selected cogs have been reloaded!", description=f"""
Reloaded cogs:
```py
{select.values}
```
                        """, color=cfc)
                        await interaction.response.edit_message(embed=embed, view=CogSelectView(bot=self.bot))
                    else:
                        embed = discord.Embed(title="Error 403!", description="You're not a developer, so you can't use this command!", colour=errorc)
                        await ctx.respond(embed=embed)
                
            embed = discord.Embed(title="Select the cogs you want to reload:", color=cfc)
            await ctx.respond(embed=embed, view=CogSelectView(bot=self.bot))
        else:
            embed = discord.Embed(title="Error 403!", description="You're not a developer, so you can't use this command!", colour=errorc)
            await ctx.respond(embed=embed)

    
def setup(bot):
    bot.add_cog(DevCommands(bot))
