import discord
import psutil
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
        name="utility", description="Commands related to utility"
    )
    math = utility.create_subgroup(name="math", description="Commands related to math")

    @commands.Cog.listener()
    async def on_ready(self):
        print("| Utility cog loaded sucessfully")

    @discord.command(
        name="report",
        description="⛑️ Need help? Use this command to contact the admins!",
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

    @utility.command(
        name="the-team", description="🧑‍🤝‍🧑 Shows The ClearFly Team!"
    )
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
            embed = discord.Embed(title="Your avatar", url=user.display_avatar.url,colour=cfc)
        else:
            embed = discord.Embed(title=f"{user.name}'s avatar", url=user.display_avatar.url, colour=cfc)

        embed.set_image(url=user.display_avatar.url)
        await ctx.respond(embed=embed)

    @discord.user_command(
        name="User Avatar", description="Get's the avatar from the user"
    )
    async def avatar_app(self, ctx, user: discord.Member):
        await ctx.defer()
        embed = discord.Embed(title=f"{user.name}'s avatar", url=user.display_avatar.url,colour=cfc)
        embed.set_image(url=user.display_avatar.url)
        await ctx.respond(embed=embed)

    @utility.command(name="who-is", description="📰 Fetches a user profile.")
    @option("user", description="The user you want the user profile of.")
    async def whois(self, ctx: discord.ApplicationContext, user: discord.Member = None):
        await ctx.defer()
        if user == None:
            user = ctx.author
        acccrte = user.created_at
        accjoine = user.joined_at
        acccrtte = discord.utils.format_dt(acccrte)
        accjointe = discord.utils.format_dt(accjoine)
        pfpe = user.display_avatar.url
        embed = discord.Embed(title=f"**{user}'s profile:**", color=cfc)
        embed.add_field(
            name=f"{user}",
            value=f"""
**Account created on:**{acccrtte}
**Account joined this server on:**{accjointe}
        """,
        )
        embed.set_thumbnail(url=pfpe)
        await ctx.respond(embed=embed)

    @discord.user_command(name="User Profile")
    async def whois_app(self, ctx: discord.ApplicationContext, user: discord.Member):
        await ctx.defer()
        acccrte = user.created_at
        accjoine = user.joined_at
        acccrtte = discord.utils.format_dt(acccrte)
        accjointe = discord.utils.format_dt(accjoine)
        pfpe = user.display_avatar.url
        embed = discord.Embed(title=f"**{user}'s profile:**", color=cfc)
        embed.add_field(
            name=f"{user}",
            value=f"""
**Account created on:**{acccrtte}
**Account joined this server on:**{accjointe}
        """,
        )
        embed.set_thumbnail(url=pfpe)
        await ctx.respond(embed=embed)

    @utility.command(
        name="github", description="🗄️ Shows Clearfy's GitHub repositories."
    )
    async def github(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="ClearFly GitHub:",
            description="- [ClearFly](https://github.com/ClearFly-Official/)\n- [ClearBot](https://github.com/ClearFly-Official/ClearBot)\n- [ClearFly Branding](https://github.com/ClearFly-Official/ClearFly-Branding)",
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

    @utility.command(
        name="stats", description="📈 Show statistics about the bot and server."
    )
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
**CPU usage:** {psutil.cpu_percent(interval=0.1)}
**RAM usage:** {psutil.virtual_memory()[2]}({psutil.virtual_memory()[3]/1000000}MB)
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

    @discord.command(
        name="help", description="❓ Need help? This is the right command!"
    )
    async def help(self, ctx: discord.ApplicationContext):
        class HelpView(discord.ui.View):
            def __init__(self, bot):
                self.bot = bot
                super().__init__(timeout=None)

            @discord.ui.select(
                placeholder="Command category",
                min_values=1,
                max_values=1,
                options=[
                    discord.SelectOption(
                        label="Utility",
                        description="Command that are supposed to be useful.",
                        emoji="🛠️",
                    ),
                    discord.SelectOption(
                        label="Aviation",
                        description="Command that are related to aviation.",
                        emoji="🛫",
                    ),
                    discord.SelectOption(
                        label="Fun",
                        description="Commands to run when you have nothing else to do.",
                        emoji="🧩",
                    ),
                    discord.SelectOption(
                        label="VA",
                        description="Everything needed for the Virtual Airline.",
                        emoji="✈️",
                    ),
                    discord.SelectOption(
                        label="Leveling",
                        description="Commands related to leveling.",
                        emoji="🏆",
                    ),
                    discord.SelectOption(
                        label="Tags",
                        description="Commands related to tags.",
                        emoji="🏷️",
                    ),
                    discord.SelectOption(
                        label="Admin",
                        description="Commands for admins only.",
                        emoji="🔒",
                    ),
                ],
            )
            async def select_callback(self, select, interaction):
                if interaction.user.id == ctx.author.id:
                    guild = self.bot.get_guild(965419296937365514)
                    if select.values[0] == "Utility":
                        embutil = discord.Embed(title="**Help**", color=cfc)
                        embutil.add_field(
                            name="**Utility commands**",
                            value=f"""
</help:1002512441873281085> : Shows this information.
</report:1018970055972757506> : Report a user or situation to the team.

</utility stats:1018089106267451432> : Show statistics about the bot and server.
</utility who-is:1018089106267451432> : Shows all kind of information about a user.
</utility the-team:1018089106267451432> : Shows The ClearFly Team!
</utility avatar:1018089106267451432> : Shows your avatar.
</utility github:1018089106267451432> : Shows the bot's GitHub repository.
</utility math basic:1018089106267451432> : Do some basic math.
</utility math advanced:1018089106267451432> : Do some advanced math.
                                    """,
                        )
                        await interaction.response.edit_message(embed=embutil)
                    if select.values[0] == "Aviation":
                        embutil = discord.Embed(title="**Help**", color=cfc)
                        embutil.add_field(
                            name="**Aviation commands**",
                            value=f"""
</aviation metar:1059269616494460938> : Get the metar data of an airport.
</aviation charts:1059269616494460938> : Fetches charts of the provided airport.
                                    """,
                        )
                        await interaction.response.edit_message(embed=embutil)
                    if select.values[0] == "Fun":
                        embfun = discord.Embed(title="**Help**", color=cfc)
                        embfun.add_field(
                            name="**Fun commands**",
                            value=f"""
</fun ascii:1016057999195910276> : Converts text in to big ascii characters.
</fun bigtext:1016057999195910276> : Converts text in to big emoji text.
</fun 8ball:1016057999195910276> : Ask the bot some questions!
</fun dadjoke:1016057999195910276> : Gets you a dadjoke.
</fun roast:1016057999195910276> : Roast whoever you'd like!
</fun button-game:1016057999195910276> : Play a game with buttons!
</fun flag-game:1016057999195910276> : Guess a sentence where country codes get replace by flags(e.g. after -> 🇦🇫ter).
</fun meme:1016057999195910276> : Get a fresh meme from r/aviationmemes.
                                """,
                        )
                        await interaction.response.edit_message(embed=embfun)
                    if select.values[0] == "VA":
                        role = guild.get_role(1040918528565444618)
                        embva = discord.Embed(title="**Help**", color=cfc)
                        if role in interaction.user.roles:
                            embva.add_field(
                                name="**ClearFly Virtual Airline**",
                                value=f"""
**-------Instructor-------**
</va instructor approve:1016059999056826479> : Approve a student's flight and give the required info to them.
</va instructor check-off:1016059999056826479> : Check off a user to end their training.
**--------Training--------**
</va training:1016059999056826479> : Start your career in the ClearFly VA!
**-----After Training-----**
</va file:1016059999056826479> : File a flight you are gonna do for the ClearFly VA.
</va cancel:1016059999056826479> : Cancels and removes your last filed flight.
</va divert:1016059999056826479> : If you need to divert to another airport you can with this command.
</va report-incident:1016059999056826479> : Something happened on your flight? Run this command and tell us what happened!
</va flights:1016059999056826479> : Fetches information about all flights a user has done.
</va leaderboard:1016059999056826479> : Get the leaderboard of who flew the most flights!
</va liveries:1016059999056826479> : Get all liveries to get your journey started.
                                            """,
                                inline=False,
                            )
                            await interaction.response.edit_message(embed=embva)
                        else:
                            embva.add_field(
                                name="**ClearFly Virtual Airline**",
                                value=f"""
**--------Training--------**
</va training:1016059999056826479> : Start your career in the ClearFly VA!
**-----After Training-----**
</va file:1016059999056826479> : File a flight you are gonna do for the ClearFly VA.
</va cancel:1016059999056826479> : Cancels and removes your last filed flight.
</va divert:1016059999056826479> : If you need to divert to another airport you can with this command.
</va report-incident:1016059999056826479> : Something happened on your flight? Run this command and tell us what happened!
</va flights:1016059999056826479> : Fetches information about all flights a user has done.
</va leaderboard:1016059999056826479> : Get the leaderboard of who flew the most flights!
</va liveries:1016059999056826479> : Get all liveries to get your journey started.
                                            """,
                                inline=False,
                            )
                            await interaction.response.edit_message(embed=embva)
                    if select.values[0] == "Leveling":
                        embva = discord.Embed(title="**Help**", color=cfc)
                        embva.add_field(
                            name="**Leveling Commands**",
                            value=f"""
</level userlevel:1032273658305069086> : Gets the provided user's level.
</level leaderboard:1032273658305069086> : See the leaderboard of the whole server.
                                            """,
                            inline=False,
                        )
                        await interaction.response.edit_message(embed=embva)
                    if select.values[0] == "Tags":
                        guild = self.bot.get_guild(965419296937365514)
                        adminrole = guild.get_role(965422406036488282)
                        if adminrole in interaction.user.roles:
                            embed = discord.Embed(title="**Help**", color=cfc)
                            embed.add_field(
                                name="**Tag Commands**",
                                value=f"""
</tag view:1058747272596299796> : View a tag.
</tag list:1058747272596299796> : List all the tags.
</tag add:1058747272596299796> : Add a new tag.
</tag edit:1058747272596299796> : Edit a tag.
</tag delete:1058747272596299796> : Deleta a tag.
                                                """,
                                inline=False,
                            )
                            await interaction.response.edit_message(embed=embed)
                        else:
                            embed = discord.Embed(title="**Help**", color=cfc)
                            embed.add_field(
                                name="**Tag Commands**",
                                value=f"""
</tag view:1058747272596299796> : View a tag.
</tag list:1058747272596299796> : List all the tags.
                                                """,
                                inline=False,
                            )
                            await interaction.response.edit_message(embed=embed)
                    if select.values[0] == "Admin":
                        guild = self.bot.get_guild(965419296937365514)
                        adminrole = guild.get_role(965422406036488282)
                        if adminrole in interaction.user.roles:
                            embad = discord.Embed(title="**Help**", color=cfc)
                            embad.add_field(
                                name="**Admin Commands**",
                                value=f"""
</admin spam:1018056894394409021> : Spam the channel to oblivion.
</admin purge:1018056894394409021> : Delete messages from a channel.
</admin echo:1018056894394409021> : Send a message as the bot.
</admin slowmode:1018056894394409021> : Set the slow mode of a channel.
</admin embed:1018056894394409021> : Send an embed as the bot.
                                                """,
                                inline=False,
                            )
                            await interaction.response.edit_message(embed=embad)
                        else:
                            embed = discord.Embed(
                                title="Error 403!",
                                description="You are not an admin, you can't use these commands!",
                                color=errorc,
                            )
                            await interaction.response.edit_message(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error 403!",
                        description="Run the command yourself to use it!",
                        color=errorc,
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = discord.Embed(
            title="Help!",
            description="Select the command category in the drop down for help.",
            color=cfc,
        )
        await ctx.respond(embed=embed, view=HelpView(bot=self.bot))


def setup(bot):
    bot.add_cog(UtilityCommands(bot))
