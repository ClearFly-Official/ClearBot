import discord
import psutil
import urllib.parse
from datetime import datetime
from math import sqrt
from discord import option
from discord.ext import commands
from dotenv import load_dotenv
from main import cogs
from main import cfc, errorc


load_dotenv()


class UtilityCommands(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    utility = discord.SlashCommandGroup(
        name="utility", description="🛠️ Commands that are supposed to be useful."
    )
    math = utility.create_subgroup(name="math", description="Commands related to math")

    @commands.Cog.listener()
    async def on_ready(self):
        print("| Utility cog loaded sucessfully")

    @discord.command(
        name="report",
        description="⛑️ Someone is misbehaving? Use this command to contact the admins!",
    )
    @option(
        "subject",
        description="What is your report about?",
        choices=["Misbehaving User", "Spam", "Hacked/Compromised Account", "Raid"],
    )
    @option(
        "priority",
        description="The priority level of the report",
        choices=["low", "medium", "high"],
    )
    @option(
        "user",
        description="The user involved(if more than one mention in comments unless raid)",
        required=False,
    )
    @option(
        "comments", description="Anything else to say about the report?", required=False
    )
    @commands.cooldown(2, 120)
    async def report(
        self,
        ctx: discord.ApplicationContext,
        subject: str,
        priority: str,
        user: discord.Member,
        comments: str,
    ):
        await ctx.defer(ephemeral=True)
        channel = self.bot.get_channel(965655791468183612)
        embed = discord.Embed(title=f"{ctx.author} submitted a report!", color=cfc)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        confirmembed = discord.Embed(
            title="Report send!",
            description="The team will come to help you as soon as possible.",
            color=cfc,
        )
        if user == None:
            user = "None was given"
        if priority == "low":
            embed.add_field(name="Subject:", value=subject)
            embed.add_field(name="Involved User:", value=f"{user.mention}")
            embed.add_field(
                name="Comments *if any*:",
                value=f"""
```
{comments}
```
            """,
                inline=False,
            )
            await ctx.respond(embed=confirmembed)
            await channel.send("Low priority report", embed=embed)
        if priority == "medium":
            embed.add_field(name="Subject:", value=subject)
            embed.add_field(name="Involved User:", value=user)
            embed.add_field(
                name="Comments *if any*:",
                value=f"""
```
{comments}
```
            """,
                inline=False,
            )
            await ctx.respond(embed=confirmembed)
            await channel.send(
                "<@&965422406036488282> Medium priority report", embed=embed
            )
        if priority == "high":
            embed.add_field(name="Subject:", value=subject)
            embed.add_field(name="Involved User:", value=user)
            embed.add_field(
                name="Comments *if any*:",
                value=f"""
```
{comments}
```
            """,
                inline=False,
            )
            await ctx.respond(embed=confirmembed)
            await channel.send(
                "<@&965422406036488282> ATTENTION ALL ADMINS", embed=embed
            )
            await channel.send(
                "<@&965422406036488282> ^ THIS IS A HIGH PRIORITY REPORT"
            )

    @utility.command(name="the-team", description="🧑‍🤝‍🧑 Shows The ClearFly Team!")
    async def team(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title="The ClearFly Team:", color=cfc)
        logo = "https://cdn.discordapp.com/attachments/966077223260004402/1057364736607531128/image0.jpg"
        embed.add_field(name="WolfAir", value="> Founder & Modeler", inline=False)
        embed.add_field(
            name="Matt3o0", value="> Bot and SASL developer & Admin", inline=False
        )
        embed.add_field(name="DJ", value="> Admin & Advisor", inline=False)
        embed.set_thumbnail(url=logo)
        await ctx.respond(embed=embed)

    @utility.command(name="avatar", description="🌌 Shows your avatar.")
    @option("user", description="The user you want the avatar of.")
    async def avatar(
        self, ctx: discord.ApplicationContext, user: discord.Member = None
    ):
        await ctx.defer()
        if user == None:
            user = ctx.author
            embed = discord.Embed(
                title="Your avatar", url=user.display_avatar.url, colour=cfc
            )
        else:
            embed = discord.Embed(
                title=f"{user.name}'s avatar", url=user.display_avatar.url, colour=cfc
            )

        embed.set_image(url=user.display_avatar.url)
        await ctx.respond(embed=embed)

    @discord.user_command(
        name="User Avatar", description="Get's the avatar from the user"
    )
    async def avatar_app(self, ctx, user: discord.Member):
        await ctx.defer()
        embed = discord.Embed(
            title=f"{user.name}'s avatar", url=user.display_avatar.url, colour=cfc
        )
        embed.set_image(url=user.display_avatar.url)
        await ctx.respond(embed=embed)

    @utility.command(name="who-is", description="📰 Fetches a user profile.")
    @option("user", description="The user you want the user profile of.")
    async def whois(self, ctx: discord.ApplicationContext, user: discord.Member = None):
        await ctx.defer()
        if user == None:
            user = ctx.author
        roles = []
        status = str(user.status)
        if status == "dnd":
            status = "Do Not Disturb"
        for role in user.roles:
            roles.append(f"<@&{role.id}>")
        roles = "\n".join(reversed(roles))
        if user.is_on_mobile():
            device = "Mobile"
        else:
            if status == "offline":
                device = "User is offline"
            else:
                device = "Desktop/Web"
        embed = discord.Embed(
            title=f"**{user}'s profile:**",
            color=cfc,
            description=f"""
{user.mention}
**Created on:** {discord.utils.format_dt(user.created_at)}
**Status:** `{status.title()}`
**Activity:** {user.activity}
**Device:** `{device}`

**Joined ClearFly:** {discord.utils.format_dt(user.joined_at)}
**Nickname:** {user.nick}
**Roles:** 
{roles}
        """,
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        await ctx.respond(embed=embed)

    @discord.user_command(name="User Profile")
    async def whois_app(self, ctx: discord.ApplicationContext, user: discord.Member):
        await ctx.defer()
        roles = []
        status = str(user.status)
        for role in user.roles:
            roles.append(f"<@&{role.id}>")
        roles = "\n".join(reversed(roles))
        if status == "dnd":
            status = "Do Not Disturb"
        if user == None:
            user = ctx.author
        if user.is_on_mobile():
            device = "Mobile"
        else:
            if status == "offline":
                device = "User is offline"
            else:
                device = "Desktop/Web"
        embed = discord.Embed(
            title=f"**{user}'s profile:**",
            color=cfc,
            description=f"""
{user.mention}
**Created on:** {discord.utils.format_dt(user.created_at)}
**Status:** `{status.title()}`
**Activity:** {user.activity}
**Device:** `{device}`

**Joined ClearFly:** {discord.utils.format_dt(user.joined_at)}
**Nickname:** {user.nick}
**Roles:** 
{roles}
        """,
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        await ctx.respond(embed=embed)

    @utility.command(
        name="github", description="🗄️ Shows ClearFly's GitHub repositories."
    )
    async def github(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="ClearFly GitHub:",
            description="- [ClearFly](https://github.com/ClearFly-Official/)\n- [ClearBot](https://github.com/ClearFly-Official/ClearBot)\n- [ClearFly-Branding](https://github.com/ClearFly-Official/ClearFly-Branding)",
            color=cfc,
        )
        await ctx.respond(embed=embed)

    @math.command(name="basic", description="🧮 Do some basic math.")
    @option(
        "type",
        description="The type of basic math you want to do.",
        choices=["Addition", "Subtraction", "Multiplication", "Division"],
    )
    @option("input1", description="The first number.")
    @option("input2", description="The second number.")
    async def basic(
        self, ctx: discord.ApplicationContext, type, input1: int, input2: int
    ):
        await ctx.defer()
        if type == "Addition":
            embed = discord.Embed(
                description=f"{input1} + {input2} = **{input1+input2}**", color=cfc
            )
            await ctx.respond(embed=embed)
        if type == "Subtraction":
            embed = discord.Embed(
                description=f"{input1} - {input2} = **{input1-input2}**", color=cfc
            )
            await ctx.respond(embed=embed)
        if type == "Multiplication":
            embed = discord.Embed(
                description=f"{input1} x {input2} = **{input1*input2}**", color=cfc
            )
            await ctx.respond(embed=embed)
        if type == "Division":
            if input2 == 0:
                await ctx.respond("You can't divide by 0!")
            else:
                embed = discord.Embed(
                    description=f"{input1} : {input2} = **{input1/input2}**", color=cfc
                )
                await ctx.respond(embed=embed)

    @math.command(name="advanced", description="♾️ Do some more advanced math.")
    @option(
        "type",
        description="The type of advanced math you want to do.",
        choices=["Square root", "Power"],
    )
    @option("input", description="The first number")
    @option("power", description="The exponent (not needed for sqrt)", required=False)
    async def advanced(
        self,
        ctx: discord.ApplicationContext,
        type: str,
        input: int,
        exponent: int = None,
    ):
        await ctx.defer()
        if type == "Square root":
            embed = discord.Embed(
                title=f"The square root of {input} is",
                description=f"**{sqrt(input)}**",
                color=cfc,
            )
            await ctx.respond(embed=embed)
        if type == "Power" and exponent == None:
            await ctx.respond("You need to give a exponent...")
        if type == "Power":
            embed = discord.Embed(
                title=f"{input} to the power of {exponent} is",
                description=f"**{input**exponent}**",
                color=cfc,
            )
            await ctx.respond(embed=embed)

    @utility.command(description="🔎 Search the web!")
    @option("query", description="The content you want to search for.")
    async def search(self, ctx: discord.ApplicationContext, query: str):
        convquery = urllib.parse.quote_plus(query)
        view = discord.ui.View()
        google = discord.ui.Button(
            label="Google", url=f"https://google.com/search?q={convquery}"
        )
        bing = discord.ui.Button(
            label="Microsoft Bing", url=f"https://bing.com/search?q={convquery}"
        )
        duckduckgo = discord.ui.Button(
            label="DuckDuckGo", url=f"https://duckduckgo.com/?q={convquery}"
        )
        ecosia = discord.ui.Button(
            label="Ecosia", url=f"https://ecosia.org/search?q={convquery}"
        )
        yahoo = discord.ui.Button(
            label="Yahoo! Search", url=f"https://search.yahoo.com/search?p={convquery}"
        )
        view.add_item(google)
        view.add_item(bing)
        view.add_item(duckduckgo)
        view.add_item(ecosia)
        view.add_item(yahoo)
        embed = discord.Embed(
            title=f"Click the links below to view the results of your search: '**{query}**'.",
            colour=cfc,
        )
        embed.set_author(
            name=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.respond(view=view, embed=embed)

    @utility.command(
        name="stats", description="📈 Show statistics about the bot and server."
    )
    @commands.cooldown(1, 5)
    async def stats(self, ctx: discord.ApplicationContext):
        loc = 0
        f = open("main.py", "r")
        loc += int(len(f.readlines()))
        for cog in cogs:
            f = open(f"cogs/{cog}.py")
            loc += int(len(f.readlines()))
        cogsList = "\n".join(cogs)
        delta_uptime = datetime.utcnow() - self.bot.start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        owner = await self.bot.fetch_user(668874138160594985)
        embed = discord.Embed(
            title="**Bot Stats**",
            description=f"""
**Creator:** {owner.mention}

**Uptime:** {days}d {hours}h {minutes}m {seconds}s, running on [Diva Hosting](https://divahosting.net/)'s servers.
**Latency:** {round(self.bot.latency*1000)}ms
**CPU usage:** {psutil.cpu_percent(interval=0.1)}%
**RAM usage:** {psutil.virtual_memory()[2]}%
**Total lines of code:** {loc}

**Cogs loaded:**
```
{cogsList}
```
        """,
            color=cfc,
        )
        members = 0
        for guild in self.bot.guilds:
            members += guild.member_count - 1
        memberCount = len(set(self.bot.get_all_members()))
        embed.add_field(
            name="**Server Stats**",
            value=f"""
**Members:** {memberCount}
                    """,
            inline=False,
        )
        await ctx.respond(embed=embed)

    async def get_commands(self, ctx: discord.AutocompleteContext):
        cmds = []
        for cmd in self.bot.walk_application_commands():
            if isinstance(cmd, discord.commands.SlashCommand):
                cmds.append(str(cmd))
        return [cmd for cmd in cmds if ctx.value in cmd]

    @discord.command(name="help", description="❓ Need help? This is the right command!")
    @option(
        "command",
        description="Get information for a specific command by inputting this option.",
        autocomplete=get_commands,
    )
    async def help(self, ctx: discord.ApplicationContext, command: str = None):
        if command != None:
            cmds = []
            for cmd in self.bot.walk_application_commands():
                if isinstance(cmd, discord.commands.SlashCommand):
                    cmds.append(str(cmd))
            if command in cmds:
                cmd = self.bot.get_application_command(command)
                if cmd.options == []:
                    opts = ["`No options`"]
                else:
                    opts = []
                    for opt in cmd.options:
                        opts.append(f"`{opt.name}`")
                if cmd.cooldown == None:
                    cd = "`No cooldown`"
                else:
                    cd = f"`{cmd.cooldown.rate}` run(s) every `{round(cmd.cooldown.per)}s`"
                embed = discord.Embed(
                    title=f"`/{command}` info",
                    description=f"""
**Name**: {cmd.mention}
**Description**: {cmd.description}
**Options**: {", ".join(opts)}
**Cooldown**: {cd}
                """,
                    colour=cfc,
                )
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(
                    title="Error 404!",
                    description=f"I didn't found the command `{command}`.",
                    colour=errorc,
                )
                await ctx.respond(embed=embed)
        else:
            groups = []
            group_names = []
            for cmd in self.bot.walk_application_commands():
                if isinstance(cmd, discord.commands.SlashCommandGroup):
                    if (cmd.parent is None):
                        group_names.append(cmd.name)
                        groups.append(cmd)

            cmds = {"other": []}
            for cmd in self.bot.walk_application_commands():
                if isinstance(cmd, discord.commands.SlashCommand):
                    if str(cmd).split(" ")[0] in group_names:
                        cmds.setdefault(str(cmd).split(" ")[0], []).append(cmd)
                    else:
                        cmds["other"].append(cmd)

            select_groups = []
            for group in groups:
                select_groups.append(
                    discord.SelectOption(
                        label=group.name.title(), description=group.description
                    )
                )
            select_groups.append(
                discord.SelectOption(
                    label="Other", description="❓ Commands not in a group."
                )
            )

            class HelpView(discord.ui.View):
                def __init__(self, bot):
                    self.bot = bot
                    super().__init__(timeout=120, disable_on_timeout=True)

                @discord.ui.select(
                    placeholder="Select command group...",
                    min_values=1,
                    max_values=1,
                    options=select_groups,
                )
                async def select_callback(self, select, interaction):
                    listed_cmds = []
                    for cmd in cmds[select.values[0].lower()]:
                        if cmd.options == []:
                            opts = ["`No options`"]
                        else:
                            opts = []
                            for opt in cmd.options:
                                opts.append(f"`{opt.name}`")
                        listed_cmds.append(
                            f"{cmd.mention}({', '.join(opts)}) - {cmd.description}"
                        )
                    embed = discord.Embed(
                        title=f"{select.values[0]} Commands",
                        description="\n".join(listed_cmds),
                        colour=cfc,
                    )
                    await interaction.response.edit_message(embed=embed)

            embed = discord.Embed(
                title="Help!",
                description="Select a command group below to view all the available commands inside it.",
                colour=cfc,
            )
            await ctx.respond(embed=embed, view=HelpView(self.bot))


def setup(bot):
    bot.add_cog(UtilityCommands(bot))
