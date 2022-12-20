import subprocess
import discord
import json
from inspect import cleandoc
from discord import option

#cfc = 0x2681b4 #<- default color
#cfc = 0xcc8d0e # <- halloween color
cfc = 0x00771d # <- christmas color
errorc = 0xFF0000


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
acdevs = [668874138160594985, 871893179450925148, 917477940650971227]

class DevCommands(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    dev = discord.SlashCommandGroup(name="dev", description="Commands for developers.")
    acdev = discord.SlashCommandGroup(name="acdev", description="Commands for aircraft developers.")
    dataref = acdev.create_subgroup(name="datarefs", description="Commands related to X-Plane datarefs.")

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
        if ctx.author.id in devs:
            doc_part, path = await self.convert_attr(doc_part)
            if not doc_part:
                embed = discord.Embed(title=f"Error 404!", description=f"Couldn't find `{doc_part}`.", colour=errorc)
                return await ctx.respond(embed=embed)
            if doc_part.__doc__ is None:
                embed = discord.Embed(title=f"Error 404!", description=f"Couldn't find documentation `{doc_part}`.", colour=errorc)
                return await ctx.respond(embed=embed)
            embed = discord.Embed(title=f"Found the following for {path}", description=f"```\n{cleandoc(doc_part.__doc__)[:1993]}```", colour=cfc)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="Error 403!", description="You're not a developer, so you can't use this command!", colour=errorc)
            await ctx.respond(embed=embed)

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

    
    async def get_datarefs(self, ctx: discord.AutocompleteContext):
        with open("dev/aircraft/datarefs.txt") as f:
            datarefList = []
            datarefLoad = f.readlines()
            for elem in datarefLoad:
                newElem = elem.replace('\n', '')
                datarefList.append(newElem)
        return [dataref for dataref in datarefList if dataref.startswith(ctx.value)]

    @dataref.command(name="search", description="Find the custom dataref you're looking for.")
    @option("dataref", description="The dataref you want information about.", autocomplete=get_datarefs)
    async def datarefs(self, ctx, dataref):
        if ctx.author.id in acdevs:
            await ctx.defer()
            with open("dev/aircraft/datarefs.txt") as f:
                datarefList = []
                datarefLoad = f.readlines()
                for elem in datarefLoad:
                    newElem = elem.replace('\n', '')
                    datarefList.append(newElem)
            if dataref in datarefList:
                with open("dev/aircraft/datarefs.json", "r") as f:
                    datarefJson = json.load(f)
                datarefs = datarefJson["datarefs"]
                embed = discord.Embed(title=f"Found this information for the provided dataref:", colour=cfc)
                embed.add_field(name="Dataref Information:", value=f"""
Path : `{datarefs[dataref]["path"]}`
Type : **{datarefs[dataref]["type"]}**
Description :
> **{datarefs[dataref]["description"]}**
Range : **{datarefs[dataref]["range"]}**
                """)
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="Error 404!", description=f"Didn't found the dataref `{dataref}`", colour=errorc)
        else:
            embed = discord.Embed(title="Error 403!", description="You're not a developer, so you can't use this command!", colour=errorc)
            await ctx.respond(embed=embed)

    @dataref.command(name="add", description="Add a new dataref to the list of datarefs.")
    @option("path", description="The path of the new dataref(e.g: ClearFly/731/foo/bar).")
    @option("type", description="The type of dateref the new dataref will be.", choices=["int", "float", "double", "string", "int array", "float array"])
    @option("description", description="The description of the new dataref.")
    @option("range", description="The range of the dataref's values(e.g: 0.0 -> 1.0), 'N/A' for string types.")
    async def drefadd(self, ctx, path, type, description, range):
        if ctx.author.id in acdevs:
            if path.startswith("ClearFly/731"):
                await ctx.defer()
                with open("dev/aircraft/datarefs.json", "r") as f:
                    datarefs = json.load(f)
                if type == "string":
                    range = "N/A"
                newDrefPath = f"{path}"
                newtype = f"{type}"
                newDrefDesc = f"{description}"
                newrange = f"{range}"
                newDref = {
                        f"{newDrefPath}":{
                            "path":f"{newDrefPath}",
                            "type":f"{newtype}",
                            "description":f"{newDrefDesc}",
                            "range":f"{newrange}"
                        }
                }

                datarefs["datarefs"].update(newDref)

                with open("dev/aircraft/datarefs.json", "w") as f:
                    json.dump(datarefs, f, indent=4)
                with open("dev/aircraft/datarefs.txt", "a") as f:
                    f.write(f"\n{path}")
                embed = discord.Embed(title=f"Added new dataref `{path}` to dataref list successfully.", color=cfc)
                embed.set_footer(text="Don't forget to make the dateref with SASL if you didn't already do so.")
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="Error 422!", description="All custom dataref paths should start with `ClearFly/731`. This is to keep the dataref structure organized. \n\n Example dataref: `ClearFly/731/foo/bar`", colour=errorc)
                await ctx.respond(embed=embed)

        else:
            embed = discord.Embed(title="Error 403!", description="You're not a developer, so you can't use this command!", colour=errorc)
            await ctx.respond(embed=embed)

    @dataref.command(name="edit", description="Edit an existing dataref.")
    @option("dataref", description="The path of the dataref you want to edit.")
    @option("type", description="The type of dateref the dataref is.", choices=["int", "float", "double", "string", "int array", "float array"])
    @option("description", description="The description of the dataref.")
    @option("range", description="The range of the dataref's values(e.g: 0.0 -> 1.0), 'N/A' for string types.")
    async def drefadd(self, ctx, dataref, type, description, range):
        if ctx.author.id in acdevs:
            with open("dev/aircraft/datarefs.txt") as f:
                datarefList = []
                datarefLoad = f.readlines()
                for elem in datarefLoad:
                    newElem = elem.replace('\n', '')
                    datarefList.append(newElem)
            if dataref in datarefList:
                await ctx.defer()
                with open("dev/aircraft/datarefs.json", "r") as f:
                    datarefs = json.load(f)
                if type == "string":
                    range = "N/A"
                newDrefPath = f"{dataref}"
                newtype = f"{type}"
                newDrefDesc = f"{description}"
                newrange = f"{range}"
                newDref = {
                            "path":f"{newDrefPath}",
                            "type":f"{newtype}",
                            "description":f"{newDrefDesc}",
                            "range":f"{newrange}"
                }
                datarefs["datarefs"][dataref].update(newDref)

                with open("dev/aircraft/datarefs.json", "w") as f:
                    json.dump(datarefs, f, indent=4)
                embed = discord.Embed(title=f"Edited dataref `{dataref}` successfully.", colour=cfc)
                embed.set_footer(text="Don't forget to edit the dateref with SASL if you didn't already do so.")
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="Error 404!", description=f"Didn't found the dataref `{dataref}`. I can't edit a dataref when it doesn't exist!", colour=errorc)
                await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="Error 403!", description="You're not a developer, so you can't use this command!", colour=errorc)
            await ctx.respond(embed=embed)



def setup(bot):
    bot.add_cog(DevCommands(bot))
