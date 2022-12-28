import discord
import json
import requests
import os
from datetime import datetime
from math import sqrt
from discord import option
from discord.ext import commands
from dotenv import load_dotenv
from main import bot_start_time

#cfc = 0x2681b4 #<- default color
#cfc = 0xcc8d0e # <- halloween color
cfc = 0x00771d # <- christmas color
errorc = 0xFF0000

load_dotenv()

class UtilityCommands(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    utility = discord.SlashCommandGroup(name="utility", description="Commands related to utility")
    math = utility.create_subgroup(name="math", description="Commands related to math")

    @discord.command(name="report", description="Need help? Use this command to contact the admins!")
    @option("subject",description="What is your report about?",choices=["Misbehaving User", "Spam", "Hacked/Compromised Account", "Raid"])
    @option("priority", description="The priority level of the report", choices=["low", "medium", "high"])
    @option("user", description="The user involved(if more than one mention in comments unless raid)", required=False)
    @option("comments", description="Anything else to say about the report?", required=False)
    async def report(self, ctx, subject ,priority ,user: discord.Member, comments):
        await ctx.defer(ephemeral=True)
        channel = self.bot.get_channel(965655791468183612)
        embed = discord.Embed(title=f"{ctx.author} submitted a report!", color=cfc)
        embed.set_thumbnail(url=ctx.author.avatar.url)
        confirmembed = discord.Embed(title="Report send!", description="The team will come to help you as soon as possible.", color=cfc)
        if user ==None:
            user ="None was given"
        if priority == "low":
            embed.add_field(name="Subject:", value=subject)
            embed.add_field(name="Involved User:", value=f"{user.mention}")
            embed.add_field(name="Comments *if any*:", value=f"""
```
{comments}
```
            """, inline=False)
            await ctx.respond(embed=confirmembed)
            await channel.send("Low priority report", embed=embed)
        if priority == "medium":
            embed.add_field(name="Subject:", value=subject)
            embed.add_field(name="Involved User:", value=user)
            embed.add_field(name="Comments *if any*:", value=f"""
```
{comments}
```
            """, inline=False)
            await ctx.respond(embed=confirmembed)
            await channel.send("<@&965422406036488282> Medium priority report", embed=embed)
        if priority == "high":
            embed.add_field(name="Subject:", value=subject)
            embed.add_field(name="Involved User:", value=user)
            embed.add_field(name="Comments *if any*:", value=f"""
```
{comments}
```
            """, inline=False)
            await ctx.respond(embed=confirmembed)
            await channel.send("<@&965422406036488282> ATTENTION ALL ADMINS", embed=embed)
            await channel.send("<@&965422406036488282> ^ THIS IS A HIGH PRIORITY REPORT")

    @utility.command(name='the-team', description='Shows The ClearFly Team!')
    async def team(self, ctx):
        embed = discord.Embed(title="The ClearFly Team:",color=cfc)
        logo = "https://cdn.discordapp.com/attachments/966077223260004402/1057364736607531128/image0.jpg"
        embed.add_field(name="WolfAir",value="> Founder & Modeler",inline=False)
        embed.add_field(name="Matt3o0",value="> Bot Creator & Admin",inline=False)
        embed.add_field(name="DJ",value="> Admin",inline=False)
        embed.set_thumbnail(url=logo)
        await ctx.respond(embed=embed)

    @utility.command(name="avatar",description="Shows your avatar.")
    @option("user", description="The user you want the avatar of.")
    async def avatar(self, ctx, user: discord.Member = None):
        await ctx.defer()
        if user == None:
            author = ctx.author
            pfp = author.avatar.url
            embed = discord.Embed(title="Your avatar!",description=f"[link]({pfp})", color=cfc)
            embed.set_image(url=pfp)
            await ctx.respond(embed=embed)
        else:
            userAvatarUrl = user.avatar.url    
            embed = discord.Embed(title=f"{user}'s avatar!",description=f"[link]({userAvatarUrl})", color=cfc)
            embed.set_image(url=userAvatarUrl)
            await ctx.respond(embed=embed)

    @discord.user_command(name="User Avatar", description="Get's the avatar from the user")
    async def avatar_app(self, ctx, user:discord.Member):
        await ctx.defer()
        userAvatarUrl = user.avatar.url    
        embed = discord.Embed(title=f"{user}'s avatar!",description=f"[link]({userAvatarUrl})", color=cfc)
        embed.set_image(url=userAvatarUrl)
        await ctx.respond(embed=embed)

    @utility.command(name="who-is", description="Fetches a user profile")
    @option("user", description="The user you want the user profile of.")
    async def whois(self, ctx, user: discord.Member = None):
        await ctx.defer()
        if user == None:
            author = ctx.author
            acccrt = author.created_at
            accjoin = author.joined_at
            acccrtt = discord.utils.format_dt(acccrt)
            accjoint = discord.utils.format_dt(accjoin)
            pfp = author.avatar.url
            emb = discord.Embed(title=f"**Your profile:**", color=cfc)
            emb.add_field(name=f"{author}",value=f"""
**Account created on:**{acccrtt}
**Account joined this server on:**{accjoint}
            """)
            emb.add_field(name="Avatar:", value=f"[link]({pfp})", inline=False)
            emb.set_thumbnail(url=pfp)
            await ctx.respond(embed=emb)
        else:
            acccrte = user.created_at
            accjoine = user.joined_at
            acccrtte = discord.utils.format_dt(acccrte)
            accjointe = discord.utils.format_dt(accjoine)
            pfpe = user.avatar.url
            embed = discord.Embed(title=f"**{user}'s profile:**", color=cfc)
            embed.add_field(name=f"{user}",value=f"""
**Account created on:**{acccrtte}
**Account joined this server on:**{accjointe}
            """)
            embed.add_field(name="Avatar:", value=f"[link]({pfpe})", inline=False)
            embed.set_thumbnail(url=pfpe)
            await ctx.respond(embed=embed)

    @discord.user_command(name="User Profile")
    async def whois_app(self, ctx, user:discord.Member):
        await ctx.defer()
        acccrte = user.created_at
        accjoine = user.joined_at
        acccrtte = discord.utils.format_dt(acccrte)
        accjointe = discord.utils.format_dt(accjoine)
        pfpe = user.avatar.url
        embed = discord.Embed(title=f"**{user}'s profile:**", color=cfc)
        embed.add_field(name=f"{user}",value=f"""
**Account created on:**{acccrtte}
**Account joined this server on:**{accjointe}
        """)
        embed.add_field(name="Avatar:", value=f"[link]({pfpe})", inline=False)
        embed.set_thumbnail(url=pfpe)
        await ctx.respond(embed=embed)

    @utility.command(name="github", description="Shows Clearfy's GitHub repositories.")
    async def github(self, ctx):
        embed = discord.Embed(title="ClearFly GitHub:", description="-[ClearFly](https://github.com/ClearFly-Official/)\n-[ClearBot](https://github.com/ClearFly-Official/ClearBot)\n-[ClearFly Branding](https://github.com/ClearFly-Official/ClearFly-Branding)",color=cfc)
        await ctx.respond(embed=embed)

    @math.command(name="basic", description="Do some basic math.")
    @option("type", description="The type of basic math you want to do.", choices=["Addition","Subtraction","Multiplication","Division"])
    @option("input1", description="The first number.")
    @option("input2", description="The second number.")
    async def basic(self, ctx, type,input1:int, input2:int):
        await ctx.defer()
        if type == "Addition":
            embed = discord.Embed(description=f"{input1} + {input2} = **{input1+input2}**", color=cfc)
            await ctx.respond(embed=embed)
        if type == "Subtraction":
            embed = discord.Embed(description=f"{input1} - {input2} = **{input1-input2}**", color=cfc)
            await ctx.respond(embed=embed)
        if type == "Multiplication":
            embed = discord.Embed(description=f"{input1} x {input2} = **{input1*input2}**", color=cfc)
            await ctx.respond(embed=embed)
        if type == "Division":
            if input2 == 0:
                await ctx.respond("You can't divide by 0!")
            else:
                embed = discord.Embed(description=f"{input1} : {input2} = **{input1/input2}**", color=cfc)
                await ctx.respond(embed=embed)

    @math.command(name="advanced", description="Do some more advanced math.")
    @option("type", description="The type of advanced math you want to do.", choices=["Square root", "Power"])
    @option("input", description="The first number")
    @option("power", description="The exponent (not needed for sqrt)", required=False)
    async def advanced(self, ctx, type, input: int, exponent:int = None):
        await ctx.defer()
        if type == "Square root":
            embed = discord.Embed(title=f"The square root of {input} is", description=f"**{sqrt(input)}**", color=cfc)
            await ctx.respond(embed=embed)
        if type == "Power" and exponent == None:
            await ctx.respond("You need to give a exponent...")
        if type == "Power":
            embed = discord.Embed(title=f"{input} to the power of {exponent} is",description=f"**{input**exponent}**", color=cfc)
            await ctx.respond(embed=embed)

    @utility.command(name="metar", description="Get the metar data of an airport.")
    @option("icao", description="The airport you want the metar data of.")
    async def metar(self, ctx, icao):
        await ctx.defer()
        hdr = {"X-API-Key": os.getenv("CWX_KEY")}
        req = requests.get(f"https://api.checkwx.com/metar/{icao.upper()}/decoded", headers=hdr)
        req.raise_for_status()
        resp = json.loads(req.text)
        class METARViewM(discord.ui.View):
            def __init__(self, bot):
                self.bot = bot
                super().__init__(timeout=120.0)

            @discord.ui.button(label="Change to Metric units", style=discord.ButtonStyle.primary)
            async def button_callback(self, button, interaction):
                if ctx.author == interaction.user:
                    time = str(json.dumps(resp['data'][0]['observed']).replace('"', ""))
                    obstime = discord.utils.format_dt(datetime.fromisoformat(time.replace("Z", "+00:00")), "R")
                    airportn = json.dumps(resp['data'][0]['station']['name']).replace("'", "")
                    embed = discord.Embed(title=f"Metar data for **{airportn}** from **{time}** ({obstime})", color=cfc)
                    embed.add_field(name="Raw Metar Data:", value=f"""
```
{json.dumps(resp['data'][0]['raw_text']).replace('"', "")}
```
            """)
                    embed.add_field(name="Translated Metar Data:", value=f"""
Airport : **{json.dumps(resp['data'][0]['station']['name']).replace('"', "")}**(**{json.dumps(resp['data'][0]['icao']).replace('"', "")}**)
Barometer : **hPa {json.dumps(resp['data'][0]['barometer']['hpa'])}**
Clouds : **{json.dumps(resp['data'][0]['clouds'][0]['text']).replace('"', "")}**(**{json.dumps(resp['data'][0]['clouds'][0]['code']).replace('"', "")}**)
Temperature : **{json.dumps(resp['data'][0]['temperature']['celsius'])}C°**
Dewpoint : **{json.dumps(resp['data'][0]['dewpoint']['celsius'])}C°**
Elevation : **{json.dumps(resp['data'][0]['elevation']['meters']).replace('"', "")} Meters**
Flight Category : **{json.dumps(resp['data'][0]['flight_category']).replace('"', "")}**
Humidity : **{json.dumps(resp['data'][0]['humidity']['percent'])}%**
Visibility : **{json.dumps(resp['data'][0]['visibility']['meters']).replace('"', "")} Meters**
Winds : **{json.dumps(resp['data'][0]['wind']['degrees'])}° at {json.dumps(resp['data'][0]['wind']['speed_kts'])} Knots**
            """, inline=False)
                    await interaction.response.edit_message(embed=embed, view=METARViewI(bot=self.bot))
                else:
                    await interaction.response.send_message("Run the command yourself to use it!", ephemeral=True)
        class METARViewI(discord.ui.View):
            def __init__(self, bot):
                self.bot = bot
                super().__init__(timeout=120.0)

            @discord.ui.button(label="Change to Imperial units", style=discord.ButtonStyle.primary)
            async def button_callback(self, button, interaction):
                if ctx.author == interaction.user:
                    time = str(json.dumps(resp['data'][0]['observed']).replace('"', ""))
                    obstime = discord.utils.format_dt(datetime.fromisoformat(time.replace("Z", "+00:00")), "R")
                    airportn = json.dumps(resp['data'][0]['station']['name']).replace("'", "")
                    embed = discord.Embed(title=f"Metar data for **{airportn}** from **{time}** ({obstime})", color=cfc)
                    embed.add_field(name="Raw Metar Data:", value=f"""
```
{json.dumps(resp['data'][0]['raw_text']).replace('"', "")}
```
            """)
                    embed.add_field(name="Translated Metar Data:", value=f"""
Airport : **{json.dumps(resp['data'][0]['station']['name']).replace('"', "")}**(**{json.dumps(resp['data'][0]['icao']).replace('"', "")}**)
Barometer : **Hg {json.dumps(resp['data'][0]['barometer']['hg'])}**
Clouds : **{json.dumps(resp['data'][0]['clouds'][0]['text']).replace('"', "")}**(**{json.dumps(resp['data'][0]['clouds'][0]['code']).replace('"', "")}**)
Temperature : **{json.dumps(resp['data'][0]['temperature']['fahrenheit']).replace('"', "")}F°**
Dewpoint : **{json.dumps(resp['data'][0]['dewpoint']['fahrenheit'])}F°**
Elevation : **{json.dumps(resp['data'][0]['elevation']['feet']).replace('"', "")} Feet**
Flight Category :**{json.dumps(resp['data'][0]['flight_category']).replace('"', "")}**
Humidity : **{json.dumps(resp['data'][0]['humidity']['percent'])}%**
Visibility : **{json.dumps(resp['data'][0]['visibility']['miles']).replace('"', "")} Miles**
Winds : **{json.dumps(resp['data'][0]['wind']['degrees'])}° at {json.dumps(resp['data'][0]['wind']['speed_kts'])} Knots**
            """, inline=False)
                    await interaction.response.edit_message(embed=embed, view=METARViewM(bot=self.bot))
                else:
                    await interaction.response.send_message("Run the command yourself to use it!", ephemeral=True)
        if resp['results'] == 1:
            time = str(json.dumps(resp['data'][0]['observed']).replace('"', ""))
            obstime = discord.utils.format_dt(datetime.fromisoformat(time.replace("Z", "+00:00")), "R")
            airportn = json.dumps(resp['data'][0]['station']['name']).replace("'", "")
            embed = discord.Embed(title=f"Metar data for **{airportn}** from **{time}** ({obstime})", color=cfc)
            embed.add_field(name="Raw Metar Data:", value=f"""
```
{json.dumps(resp['data'][0]['raw_text']).replace('"', "")}
```
            """)
            embed.add_field(name="Translated Metar Data:", value=f"""
Airport : **{json.dumps(resp['data'][0]['station']['name']).replace('"', "")}**(**{json.dumps(resp['data'][0]['icao']).replace('"', "")}**)
Barometer : **hPa {json.dumps(resp['data'][0]['barometer']['hpa'])}**
Clouds : **{json.dumps(resp['data'][0]['clouds'][0]['text']).replace('"', "")}**(**{json.dumps(resp['data'][0]['clouds'][0]['code']).replace('"', "")}**)
Temperature : **{json.dumps(resp['data'][0]['temperature']['celsius'])}C°**
Dewpoint : **{json.dumps(resp['data'][0]['dewpoint']['celsius'])}C°**
Elevation : **{json.dumps(resp['data'][0]['elevation']['meters']).replace('"', "")} Meters**
Flight Category : **{json.dumps(resp['data'][0]['flight_category']).replace('"', "")}**
Humidity : **{json.dumps(resp['data'][0]['humidity']['percent'])}%**
Visibility : **{json.dumps(resp['data'][0]['visibility']['meters']).replace('"', "")} Meters**
Winds : **{json.dumps(resp['data'][0]['wind']['degrees'])}° at {json.dumps(resp['data'][0]['wind']['speed_kts'])} Knots**
            """, inline=False)
            await ctx.respond(embed=embed, view=METARViewI(bot=self.bot))
        else:
            embed = discord.Embed(title="Error 404!", description="Didn't found metar data for that airport.", color=errorc)
            await ctx.respond(embed=embed)


    @utility.command(name="stats",description="Show statistics about the bot and server.")
    async def stats(self, ctx):
        cogs = [
        "listeners",
        "dev",
        "admin",
        "fun",
        "level",
        "utility",
        "va"
        ]
        loc = 0
        f = open("main.py", "r")
        loc += int(len(f.readlines()))
        for cog in cogs:
            f = open(f"cogs/{cog}.py")
            loc += int(len(f.readlines()))
        delta_uptime = datetime.utcnow() - bot_start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        owner = await self.bot.fetch_user(668874138160594985)
        embed = discord.Embed(title = "**Bot Stats**", description =    f"""
**Creator**
> {owner.mention}

**Uptime:**
> {days}d {hours}h {minutes}m {seconds}s, running on [Lightbulb Hosting](https://discord.gg/nnkKUS4DnV)'s servers

**Latency:**
> **{round(self.bot.latency*1000)}**ms

**Total lines of code:**
> {loc}

**Cogs loaded:**
> ```py
> {cogs}
> ```
        """, color = cfc)
        members = 0
        for guild in self.bot.guilds:
            members += guild.member_count - 1
        memberCount = len(set(self.bot.get_all_members()))
        embed.add_field(
                    name="**Server Stats**",
                    value=f"""
**Members:** 
> {memberCount}
                    """,
                    inline=False
            )
        await ctx.respond(embed = embed)
    
    @discord.command(name="help", description="Need help? This is the right command!")
    async def help(self, ctx):
        class HelpView(discord.ui.View):
                def __init__(self, bot):
                    self.bot = bot
                    super().__init__(timeout=None)
                    
                @discord.ui.select( 
                    placeholder = "Command category", 
                    min_values = 1, 
                    max_values = 1, 
                    options = [ 
                        discord.SelectOption(
                            label="Utility",
                            description="Command that are supposed to be useful.",
                            emoji="🛠️"
                        ),
                        discord.SelectOption(
                            label="Fun",
                            description="Commands to run when you have nothing else to do.",
                            emoji="🧩"
                        ),
                        discord.SelectOption(
                            label="VA",
                            description="Everything needed for the Virtual Airline.",
                            emoji="✈️"
                        ),
                        discord.SelectOption(
                        label="Leveling",
                        description="Commands related to leveling.",
                        emoji="🏆"
                        ),
                        discord.SelectOption(
                        label="Admin",
                        description="Commands for admins only.",
                        emoji="🔒"
                        )
                    ]
                )
                async def select_callback(self, select, interaction):
                    if interaction.user.id == ctx.author.id:
                        guild = self.bot.get_guild(965419296937365514)
                        if select.values[0] == "Utility":
                            embutil = discord.Embed(title = "**Help**",color = cfc)
                            embutil.add_field(name="**Utility commands**", value=f"""
```
/help : Shows this information.
/report : Report a user or situation to the team.
```
```yaml
/utility stats : Show statistics about the bot and server.
/utility who-is : Shows all kind of information about a user.
/utility the-team : Shows The ClearFly Team!
/utility avatar : Shows your avatar.
/utility github : Shows the bot's GitHub repository.
/utility math basic: Do some basic math.
/utility math advanced: Do some advanced math.
/utitlity metar : Get the metar data of an airport.
```
                                    """)
                            await interaction.response.edit_message(embed=embutil)
                        if select.values[0] == "Fun":
                            embfun = discord.Embed(title = "**Help**",color = cfc)
                            embfun.add_field(name="**Fun commands**", value=f"""
```yaml
/fun ascii : Converts text in to ascii.
/fun 8ball : Ask the bot some questions!
/fun dadjoke: Gets you a dadjoke.
/fun roast: Roast whoever you'd like!
/fun buttongame: Play a game with buttons!
```
                                """)
                            await interaction.response.edit_message(embed=embfun)
                        if select.values[0] == "VA":
                            role = guild.get_role(1040918528565444618)
                            embva = discord.Embed(title = "**Help**",color = cfc)
                            if role in interaction.user.roles:
                                embva.add_field(
                                name="**ClearFly Virtual Airline**",
                                value=f"""
```yaml
-------Instructor-------
/va instructor approve : Approve a student's flight and give the required info to them.
/va instructor check-off : Check off a user to end their training
--------Training--------
/va training : Start your career in the ClearFly VA!
-----After Training-----
/va file : File a flight you are gonna do for the ClearFly VA.
/va cancel : Cancels and removes your last filed flight.
/va divert : If you need to divert to another airport you can with this command.
/va report-incident : Something happened on your flight? Run this command and tell us what happened!
/va flights : Fetches information about all flights a user has done.
/va leaderboard : Get the leaderboard of who flew the most flights!
/va liveries : Get all liveries to get your journey started.
```
                                            """, inline=False)
                                await interaction.response.edit_message(embed=embva)
                            else:
                                embva.add_field(
                                name="**ClearFly Virtual Airline**",
                                value=f"""
```yaml
--------Training--------
/va training : Start your career in the ClearFly VA!
-----After Training-----
/va file : File a flight you are gonna do for the ClearFly VA.
/va cancel : Cancels and removes your last filed flight.
/va divert : If you need to divert to another airport you can with this command.
/va report-incident : Something happened on your flight? Run this command and tell us what happened!
/va flights : Fetches information about all flights a user has done.
/va leaderboard : Get the leaderboard of who flew the most flights!
/va liveries : Get all liveries to get your journey started.
```
                                            """, inline=False)
                                await interaction.response.edit_message(embed=embva)
                        if select.values[0] == "Leveling":
                            embva = discord.Embed(title = "**Help**",color = cfc)
                            embva.add_field(
                                name="**Leveling Commands**",
                                value=f"""
```yaml
/level userlevel : Gets the provided user's level.
/level leaderboard : See the leaderboard of the whole server.
```
                                            """, inline=False)
                            await interaction.response.edit_message(embed=embva)
                        if select.values[0] == "Admin":
                            guild = self.bot.get_guild(965419296937365514)
                            adminrole = guild.get_role(965422406036488282)
                            if adminrole in interaction.user.roles:
                                embad = discord.Embed(title = "**Help**",color = cfc)
                                embad.add_field(
                                    name="**Admin Commands**",
                                    value=f"""
```yaml
/admin spam : Spam the channel to oblivion.
/admin purge : Delete messages from a channel.
/admin echo : Send a message as the bot.
/admin slowmode : Set the slow mode of a channel.
/admin embed : Send an embed as the bot.
```
                                                """, inline=False)
                                await interaction.response.edit_message(embed=embad)
                            else:
                                embed = discord.Embed(title="Error 403!", description="You are not an admin, you can't use these commands!", color=errorc)
                                await interaction.response.edit_message(embed=embed)
                    else:
                        embed = discord.Embed(title="Error 403!", description="Run the command yourself to use it!", color=errorc)
                        await interaction.response.send_message(embed=embed, ephemeral=True)
        embed = discord.Embed(title="Help!", description="Select the command category in the drop down for help.", color=cfc)
        await ctx.respond(embed=embed, view=HelpView(bot=self.bot))

def setup(bot):
    bot.add_cog(UtilityCommands(bot))