import inspect
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

    dev = discord.SlashCommandGroup(name="dev", description="💻 Commands for (bot) developers only.")
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

    async def get_types(self, ctx: discord.AutocompleteContext):
        types = [
            "byte[1024]",
            "byte[150]",
            "byte[240]",
            "byte[24]",
            "byte[250]",
            "byte[256]",
            "byte[260]",
            "byte[2920]",
            "byte[40]",
            "byte[500]",
            "byte[512]",
            "byte[8]",
            "byte[96]",
            "byte[]",
            "double",
            "float",
            "float[10]",
            "float[128]",
            "float[12]",
            "float[14]",
            "float[16]",
            "float[16][10]",
            "float[16][12]",
            "float[16][3]",
            "float[1]",
            "float[20]",
            "float[24]",
            "float[25]",
            "float[2]",
            "float[32]",
            "float[3]",
            "float[480]",
            "float[48]",
            "float[4]",
            "float[500]",
            "float[50]",
            "float[56]",
            "float[56][10]",
            "float[56][10][4]",
            "float[56][2]",
            "float[56][2][2]",
            "float[56][2][2][721]",
            "float[56][4]",
            "float[5]",
            "float[64]",
            "float[6]",
            "float[730]",
            "float[73]",
            "float[8]",
            "float[95]",
            "float[9]",
            "int",
            "int[10]",
            "int[12]",
            "int[16]",
            "int[19]",
            "int[200]",
            "int[20]",
            "int[24]",
            "int[25]",
            "int[2]",
            "int[3200]",
            "int[3]",
            "int[4]",
            "int[500]",
            "int[50]",
            "int[56]",
            "int[56][10]",
            "int[64]",
            "int[667]",
            "int[6]",
            "int[73]",
            "int[8]",
            "int[9]",
        ]
        return [type for type in types if ctx.value in type]

    async def get_units(self, ctx: discord.AutocompleteContext):
        units = [
            "-1..1",
            "0-1",
            "0..1",
            "0..8",
            "1",
            "10Hz",
            "10hertz",
            "-1,0,1",
            "???",
            "Celsius",
            "Deg",
            "Degrees",
            "EPR",
            "GLenum",
            "Gs",
            "HWND",
            "Knots",
            "Matrix4x4",
            "Mhz",
            "Newton",
            "OGLcoords",
            "PSI",
            "Pixels",
            "RGB",
            "Read:",
            "TODOV11",
            "V11TODO",
            "[-0.5..1]",
            "[-1..1]",
            "[0..1.5]",
            "[0..1]",
            "ampere",
            "amps",
            "any",
            "bhp",
            "bitfield",
            "bool",
            "boolean",
            "byte[8]",
            "celsius",
            "channel",
            "code",
            "count",
            "day",
            "days",
            "deg",
            "deg/meter",
            "deg/sec",
            "deg/sec2",
            "degC",
            "degc_or_f",
            "degm",
            "degree",
            "degrees",
            "degrees(true)",
            "degreesC",
            "degreesF",
            "degrees_C",
            "degrees_C_or_F",
            "degrees_magnetic",
            "degs",
            "degt",
            "dots",
            "enum",
            "enums",
            "failure_enum",
            "feet",
            "feet/min",
            "feet/minute",
            "flags",
            "float",
            "fpm",
            "ft-lbs",
            "ftmsl",
            "gal/hr_or_lb/hr",
            "hertz",
            "hours",
            "hz",
            "inHg",
            "inches_hg",
            "index",
            "inhg",
            "int",
            "integer",
            "ip",
            "keas",
            "kg",
            "kg/Wattsecond",
            "kg/h",
            "kg/kg",
            "kg/s",
            "kgs",
            "khz",
            "kias",
            "kilograms/second",
            "knots",
            "knots/mach",
            "knots/second",
            "knots_mach",
            "kts",
            "lb/in2",
            "lbs",
            "light",
            "liter",
            "liters",
            "m/s",
            "m/s^2",
            "m^3/s^2",
            "mach",
            "meter",
            "meter/s",
            "meters",
            "meters/second",
            "meters^2",
            "mins",
            "minutes",
            "mode",
            "month",
            "mtr/sec2",
            "multiplier",
            "nautical_miles",
            "newton_meters",
            "newtonmeters",
            "newtons",
            "offset",
            "pascals",
            "percent",
            "percentMAC",
            "pixels",
            "pos",
            "pounds/square_inch",
            "prcnt",
            "psf",
            "psi",
            "quaternion",
            "rad/sec",
            "radians",
            "radians/second",
            "ratio",
            "revolutions/minute",
            "scalar",
            "second",
            "seconds",
            "secs",
            "square_meters",
            "string",
            "string[40]",
            "strings",
            "todo",
            "transponder_code",
            "vector",
            "volt",
            "voltage",
            "volts",
            "watt/hours",
            "watts",
        ]
        return [unit for unit in units if ctx.value in unit]

    @dataref.command(name="list", description="📂 List all the custom datarefs.")
    @commands.has_role(965422406036488282)
    async def dreflist(self, ctx: discord.ApplicationContext):
        await ctx.defer()
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
                        colour=cfc,
                    ).set_footer(
                        text=f"Showing 25/page, total of {len(drefs)} DataRefs"
                    )
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
        autocomplete=get_types,
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
        "dataref_type",
        description="The type of dataref the edited dataref will be.",
        autocomplete=get_types,
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

    @dataref.command(name="delete", description="⛔️ Delete a dataref.")
    @option(
        "dataref",
        description="The dataref you want to delete.",
        autocomplete=get_custom_datarefs,
    )
    async def drefdel(self, ctx: discord.ApplicationContext, dataref):
        await ctx.defer()
        if dataref in customDatarefList:
            drefcol.delete_one({"path": dataref})
            embed = discord.Embed(
                title=f"Dataref `{dataref}` successfully deleted.", colour=cfc
            )
        else:
            embed = discord.Embed(
                title=f"Error 404!",
                description=f"Didn't found the dateref `{dataref}`. I can't delete a dataref if it doesn't exist!",
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

    def get_code_attrs(obj_str):
        try:
            module, _, obj = obj_str.rpartition(".")
            if not module:
                # No module specified, assume built-in module
                module = obj_str
                obj = None
            elif not obj:
                # Module specified, but no object
                return dir(__import__(module))
            else:
                # Module and object specified
                module = __import__(module, fromlist=[obj])
                obj = getattr(module, obj)
            if inspect.ismodule(obj):
                return dir(obj)
            else:
                return [
                    attr
                    for attr in dir(obj)
                    if not inspect.isroutine(getattr(obj, attr))
                ]
        except (ImportError, AttributeError):
            return ["No attributes found, check your spelling and try again!"]

    async def code_autocomplete(self, ctx: discord.AutocompleteContext):
        attrs = self.get_code_attrs(ctx.value)
        return [attr for attr in attrs if ctx.value in attr]

    @dev.command(name="eval", description="💻 Execute some code.")
    @option(
        "code",
        description="The code you want to execute.",
        autocomplete=code_autocomplete,
    )
    @commands.is_owner()
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

    @dev.command(name="run_cmd", description="🖲️ Run a terminal command.")
    @option("command", description="The command you want to run.")
    @commands.is_owner()
    async def run_cmd(self, ctx: discord.ApplicationContext, command: str):
        await ctx.defer()
        embed = discord.Embed(
            description=f"""
```
{subprocess.check_output(command.split(" "))}
```
""",
            colour=cfc,
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(DevCommands(bot))
