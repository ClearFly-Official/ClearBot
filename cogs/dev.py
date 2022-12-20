import subprocess
import discord
import re
from inspect import cleandoc
from discord import option

#cfc = 0x2681b4 #<- default color
#cfc = 0xcc8d0e # <- halloween color
cfc = 0x00771d # <- christmas color
errorc = 0xFF0000

PASTEBIN_RE = re.compile(r"(https?://pastebin.com)/([a-zA-Z0-9]{8})")


async def getattrs(ctx):
    input = ctx.options["doc_part"]
    doc_part = discord
    path = "discord"
    for attr in input.split("."):
        try:
            if attr == "discord":
                continue
            doc_part = getattr(doc_part, attr)
            path += f".{attr}"
            return [f"{path}.{x}" for x in dir(doc_part) if not x.startswith("_")][:25]
        except AttributeError:
            return [f"{path}.{x}" for x in dir(doc_part) if x.startswith(attr)][:25]

devs = [668874138160594985, 871893179450925148]#Matt3o0#7010 & WolfAir#2755

class DevCommands(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    dev = discord.SlashCommandGroup(name="dev", description="Commands for developers.")

    async def convert_attr(self, path):
        doc_part = discord
        for attr in path.split("."):
            if attr == "discord":
                continue
            try:
                doc_part = getattr(doc_part, attr)
            except AttributeError:
                return None, None
        return doc_part, path

    @dev.command(name="docs", description="Get information from the Pycord docs.")
    @option("doc_part", autocomplete=getattrs)
    async def get_doc(self, ctx, doc_part):
        doc_part, path = await self.convert_attr(doc_part)
        if not doc_part:
            return await ctx.respond("Item not found.")
        if doc_part.__doc__ is None:
            return await ctx.respond(f"Couldn't find documentation for `{path}`.")

        await ctx.respond(f"```\n{cleandoc(doc_part.__doc__)[:1993]}```")


    @dev.command(name="reload_cogs", description="Reload the Cogs you want.")
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

    @dev.command(name="update", description="Pull the latest version of the bot from the GitHub repo.")
    async def gitupdate(self, ctx):
        if ctx.author.id in devs:
            await ctx.defer()
            try:
                embed = discord.Embed(description=f"""
```
{subprocess.check_output(['git','pull', 'https://github.com/ClearFly-Official/ClearBot'])}
```
""", colour=cfc)
                await ctx.respond(embed=embed)
            except Exception as error:
                embed = discord.Embed(title=f"While pulling I had the following error:", description=f"""
```
{error}
```
                """, colour=errorc)
                await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="Error 403!", description="You're not a developer, so you can't use this command!", colour=errorc)
            await ctx.respond(embed=embed)


    
def setup(bot):
    bot.add_cog(DevCommands(bot))
