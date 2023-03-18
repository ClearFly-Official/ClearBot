import subprocess
import discord
import json
import os
import sys
import pymongo
from inspect import cleandoc
from discord import option
from discord.ext import commands
from main import cfc, errorc
from discord.ext.pages import Page, Paginator

client = pymongo.MongoClient(os.environ["MONGODB_URI"])
db = client["ClearBotDB"]
drefcol = db["datarefs"]


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
            return [f"{path}.{x}" for x in dir(doc_part) if ctx.value in x][:25]


async def getattrs2(ctx):
    input = ctx.options["variable"]
    variable = discord
    path = "discord"
    for attr in input.split("."):
        try:
            if attr == "discord":
                continue
            variable = getattr(variable, attr)
            path += f".{attr}"
            return [f"{path}.{x}" for x in dir(variable) if not x.startswith("_")][:25]
        except AttributeError:
            return [f"{path}.{x}" for x in dir(variable) if ctx.value in x][:25]


class DevCommands(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    dev = discord.SlashCommandGroup(name="dev", description="Commands for developers.")
    acdev = discord.SlashCommandGroup(
        name="acdev", description="Commands for aircraft developers."
    )
    dataref = acdev.create_subgroup(
        name="datarefs", description="Commands related to X-Plane datarefs."
    )

    @commands.Cog.listener()
    async def on_ready(self):
        print("| Dev cog loaded sucessfully")

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

    @dev.command(name="docs", description="🗃️ Get information from the Pycord docs.")
    @commands.has_role(965422406036488282)
    @option(
        "doc_part",
        autocomplete=getattrs,
        description="The part of the doc you want to search for.",
    )
    async def get_doc(self, ctx: discord.ApplicationContext, doc_part):
        raw_part = doc_part
        doc_part, path = await self.convert_attr(doc_part)
        if not doc_part:
            embed = discord.Embed(
                title=f"Error 404!",
                description=f"Couldn't find `{raw_part}`.",
                colour=errorc,
            )
            return await ctx.respond(embed=embed)
        if doc_part.__doc__ is None:
            embed = discord.Embed(
                title=f"Error 404!",
                description=f"Couldn't find documentation `{raw_part}`.",
                colour=errorc,
            )
            return await ctx.respond(embed=embed)
        embed = discord.Embed(
            title=f"Found the following for `{path}`",
            description=f"""
```py
{cleandoc(doc_part.__doc__)[:1993]}
```
            """,
            colour=cfc,
        )
        await ctx.respond(embed=embed)

    @dev.command(name="reload_cogs", description="🔄 Reload the Cogs you want.")
    @commands.has_role(965422406036488282)
    async def reloadCogs(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        cogs = [
            "admin",
            "dev",
            "fun",
            "level",
            "listeners",
            "utility",
            "va",
            "tags",
            "aviation",
        ]

        class CogSelectView(discord.ui.View):
            def __init__(self, bot):
                self.bot = bot
                super().__init__(timeout=20.0)

            @discord.ui.select(
                placeholder="Cogs",
                min_values=1,
                max_values=9,
                options=[
                    discord.SelectOption(
                        label=cogs[0].capitalize(),
                        emoji="🔒",
                        value=cogs[0],
                        description="Contains all admin commands.",
                    ),
                    discord.SelectOption(
                        label=cogs[1].capitalize(),
                        emoji="💻",
                        value=cogs[1],
                        description="Contains all commands for aircraft & bot developers.",
                    ),
                    discord.SelectOption(
                        label=cogs[2].capitalize(),
                        emoji="🧩",
                        value=cogs[2],
                        description="Contains all commands that are supposed to be fun.",
                    ),
                    discord.SelectOption(
                        label=cogs[3].capitalize(),
                        emoji="🏆",
                        value=cogs[3],
                        description="Contains all leveling commands.",
                    ),
                    discord.SelectOption(
                        label=cogs[4].capitalize(),
                        emoji="👂",
                        value=cogs[4],
                        description="Contains all listeners, for logs & more.",
                    ),
                    discord.SelectOption(
                        label=cogs[5].capitalize(),
                        emoji="🛠️",
                        value=cogs[5],
                        description="Contains all 'useful' commands.",
                    ),
                    discord.SelectOption(
                        label=cogs[6].upper(),
                        emoji="✈️",
                        value=cogs[6],
                        description="Contains all VA related commands.",
                    ),
                    discord.SelectOption(
                        label=cogs[7].capitalize(),
                        emoji="🏷️",
                        value=cogs[7],
                        description="Contains all tag related commands.",
                    ),
                    discord.SelectOption(
                        label=cogs[8].capitalize(),
                        emoji="🛫",
                        value=cogs[8],
                        description="Contains all aviation commands.",
                    ),
                ],
            )
            async def select_callback(self, select, interaction):
                for cog in select.values:
                    self.bot.reload_extension(f"cogs.{cog}")
                embed = discord.Embed(
                    title="Selected cogs have been reloaded!",
                    description=f"""
Reloaded cogs:
```py
{select.values}
```
                        """,
                    color=cfc,
                )
                await interaction.response.edit_message(
                    embed=embed, view=CogSelectView(bot=self.bot)
                )

        embed = discord.Embed(title="Select the cogs you want to reload:", color=cfc)
        await ctx.respond(embed=embed, view=CogSelectView(bot=self.bot))

    @dev.command(name="restart", description="🔁 Restarst the bot.")
    @commands.is_owner()
    async def restart(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title="Restarting bot...", color=cfc)
        await ctx.respond(embed=embed)
        os.execv(sys.executable, ["python"] + sys.argv)

    @dev.command(
        name="update",
        description="⬇️ Pull the latest version of the bot from the GitHub repo.",
    )
    @commands.is_owner()
    async def gitupdate(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        embed = discord.Embed(
            description=f"""
```
{subprocess.check_output(['git','pull', 'https://github.com/ClearFly-Official/ClearBot'])}
```
""",
            colour=cfc,
        )
        await ctx.respond(embed=embed)

    async def get_datarefs(self, ctx: discord.AutocompleteContext):
        datarefList1 = []
        for dref in drefcol.find():
            datarefList1.append(dref.get("path"))
        with open("dev/aircraft/defaultDatarefsCommands.json") as f:
            datarefLoad = json.load(f)
            datarefList2 = list(datarefLoad["datarefs"].keys())
        global datarefList
        datarefList = datarefList1 + datarefList2
        return [dataref for dataref in datarefList if ctx.value in dataref]

    async def get_custom_datarefs(self, ctx: discord.AutocompleteContext):
        global customDatarefList
        customDatarefList = []
        for dref in drefcol.find():
            customDatarefList.append(dref.get("path"))
        return [dataref for dataref in customDatarefList if ctx.value in dataref]

    async def get_units(self, ctx: discord.AutocompleteContext):
        units = [
            "boolean",
            "count",
            "days",
            "degrees",
            "enum",
            "feet",
            "gallons",
            "hours",
            "IATA",
            "ICAO",
            "index",
            "kilometers",
            "kts",
            "liters",
            "meters",
            "miles",
            "minutes",
            "mps",
            "nauticalmiles",
            "percent",
            "psi",
            "ratio",
            "seconds",
            "string",
            "tons",
            "x",
            "y",
            "yards",
            "z",
        ]
        return [unit for unit in units if ctx.value in unit]

    @dataref.command(name="list", description="📂 List all the custom datarefs.")
    @commands.has_role(965422406036488282)
    async def dreflist(self, ctx: discord.ApplicationContext):
        drefs = []
        for dref in drefcol.find():
            drefs.append(dref.get("path"))
        var = 0
        var2 = 1
        for i in drefs:
            drefs[var] = f"{var2}: " + f"`{drefs[var]}`"
            var += 1
            var2 += 1

        chunks = [drefs[i : i + 25] for i in range(0, len(drefs), 25)]

        pages = [
            Page(
                embeds=[
                    discord.Embed(
                        title=f"DataRefs {i+1}-{i+len(chunk)}",
                        description="\n".join(chunk),
                        colour=cfc
                    ).set_footer(text=f"Showing 25/page, total of {len(drefs)} DataRefs")
                ]
            )
            for i, chunk in enumerate(chunks)
        ]
        paginator = Paginator(pages)
        await paginator.respond(ctx.interaction)

    @dataref.command(
        name="search", description="🔎 Find the dataref/command you're looking for."
    )
    @option(
        "dataref",
        description="The dataref you want information about.",
        autocomplete=get_datarefs,
    )
    @commands.has_role(965422406036488282)
    async def drefsearch(self, ctx: discord.ApplicationContext, dataref: str):
        await ctx.defer()
        if dataref in datarefList:
            if dataref.startswith("ClearFly"):
                dref = drefcol.find_one({"path": dataref})
                embed = discord.Embed(
                    title=f"Found this information for the provided dataref:",
                    colour=cfc,
                )
                embed.add_field(
                    name="Dataref Information:",
                    value=f"""
Path : `{dref.get('path', 'N/A')}`
Type : **{dref.get('type', 'N/A')}**
Unit : **{dref.get('unit', 'N/A')}**
Description :

> {dref.get('description', 'N/A')}
                    """,
                )
                await ctx.respond(embed=embed)
            else:
                with open("dev/aircraft/defaultDatarefsCommands.json", "r") as f:
                    datarefJson = json.load(f)
                datarefs = datarefJson["datarefs"]
                embed = discord.Embed(
                    title=f"Found this information for the provided dataref:",
                    colour=cfc,
                )
                embed.add_field(
                    name="Dataref Information:",
                    value=f"""
Path : `{datarefs[dataref].get("path", "N/A")}`
Type : **{datarefs[dataref].get("type", "N/A")}**
Writable : **{datarefs[dataref].get("writable", "N/A")}**
Unit : **{datarefs[dataref].get("unit", "N/A")}**
Description :

> {datarefs[dataref].get("description", "N/A")}
                    """,
                )
                await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
                title="Error 404!",
                description=f"Didn't found the dataref `{dataref}`",
                colour=errorc,
            )
            await ctx.respond(embed=embed)

    @dataref.command(
        name="add", description="➕ Add a new dataref to the list of datarefs."
    )
    @option(
        "path", description="The path of the new dataref(e.g: ClearFly/731/foo/bar)."
    )
    @option(
        "dataref_type",
        description="The type of dataref the new dataref will be.",
        choices=[
            "double",
            "float",
            "float array",
            "int",
            "int array",
            "string",
            "command",
        ],
    )
    @option(
        "unit", description="The unit type of the new dataref.", autocomplete=get_units
    )
    @option("description", description="The description of the new dataref.")
    @commands.has_role(965422406036488282)
    async def drefadd(
        self,
        ctx: discord.ApplicationContext,
        path: str,
        dataref_type: str,
        unit: str,
        description: str,
    ):
        if path.startswith("ClearFly/731"):
            await ctx.defer()
            drefcol.insert_one(
                {
                    "_id": path,
                    "path": path,
                    "type": dataref_type,
                    "unit": unit,
                    "description": description,
                }
            )
            embed = discord.Embed(
                title=f"Added new dataref `{path}` to dataref list successfully.",
                color=cfc,
            )
            embed.set_footer(
                text="Don't forget to make the dataref with SASL if you didn't already do so."
            )
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
                title="Error 422!",
                description="All custom dataref paths should start with `ClearFly/731`. This is to keep the dataref structure organized. \n\n Example dataref: `ClearFly/731/foo/bar`",
                colour=errorc,
            )
            await ctx.respond(embed=embed)

    @dataref.command(name="edit", description="✍️ Edit an existing dataref.")
    @option(
        "dataref",
        description="The dataref you want to edit.",
        autocomplete=get_custom_datarefs,
    )
    @option(
        "type",
        description="The type of dataref the edited dataref will be.",
        choices=["double", "float", "float array", "int", "int array", "string"],
    )
    @option(
        "unit",
        description="The unit type of the edited dataref.",
        autocomplete=get_units,
    )
    @option(
        "range",
        description="The range of the dataref's values(e.g: 0.0 -> 1.0), 'N/A' for string types.",
    )
    @option("description", description="The description of the edited dataref.")
    @option(
        "path",
        description="The path that the edited dataref will have(defaults to old one).",
        required=False,
    )
    @commands.has_role(965422406036488282)
    async def drefedit(
        self,
        ctx: discord.ApplicationContext,
        dataref: str,
        dataref_type: str,
        unit: str,
        description: str,
        path: str,
    ):
        if dataref in customDatarefList:
            await ctx.defer()
            oldDref = drefcol.find_one({"path": dataref})
            if path == None:
                path = oldDref.get("path", "N/A: Please report this to Matt3o0.")
            drefcol.update_one(
                {"path": dataref},
                {
                    "$set": {
                        "_id": path,
                        "path": path,
                        "type": dataref_type,
                        "unit": unit,
                        "description": description,
                    }
                },
            )
            embed = discord.Embed(
                title=f"Edited dataref `{dataref}` successfully.", colour=cfc
            )
            embed.set_footer(
                text="Don't forget to edit the type of the dataref with SASL, if it changed and if you didn't already do so."
            )
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
                title="Error 404!",
                description=f"Didn't found the dataref `{dataref}`. I can't edit a dataref when it doesn't exist!",
                colour=errorc,
            )
            await ctx.respond(embed=embed)

    @discord.message_command(name="Message Info")
    @commands.has_role(965422406036488282)
    async def msginfo(self, ctx: discord.ApplicationContext, message: discord.Message):
        await ctx.respond(
            f"""
ID: **{message.id}**

Content:
```md
#Normal

{message.content}

#Clean

{message.clean_content}
```

Attachments: `{message.attachments}`
Reactions: `{message.reactions}`
Embeds: `{message.embeds}`
Mentions: `{message.mentions}`
Pinned: **{message.pinned}**
Type: **{message.type}**
Author: **{message.author.mention}**
Interaction: {message.interaction}
Thread: {message.thread}
Channel: {message.channel.mention}
        """,
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @dev.command(name="eval", description="💻 Execute some code.")
    @option("code", description="The code you want to execute", autocomplete=getattrs2)
    @commands.has_role(965422406036488282)
    async def evalcmd(self, ctx: discord.ApplicationContext, code: str):
        out = eval(code)
        embed = discord.Embed(
            title=f"`{code}` gives the following output:",
            description=f"""
```
{out}
```
                """,
            colour=cfc,
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(DevCommands(bot))
