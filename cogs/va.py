import glob
import re
import discord
import os
import configparser
from PIL import Image, ImageDraw, ImageFont
from discord import option
from discord.ui import Button, View
from discord.ext import commands
from datetime import datetime
from main import cfc, errorc

airports = [
    "KDCA",
    "KIAD",
    "KLGA",
    "KMSP",
    "KORD",
    "KMDW",
    "KMKE",
    "KSFO",
    "KLAX",
    "KPHX",
    "KSEA",
    "KPDX",
    "KRIC",
    "KMIA",
    "KSTL",
    "KBOS",
    "KIND",
    "KIAH",
    "KAUS",
    "KDFW",
    "KPIT",
    "KSAN",
    "KATL",
    "CYVR",
    "CYYQ",
    "CYVO",
    "CYUL",
    "CYQB",
    "CYYZ",
    "CYOW",
    "CYYJ",
    "CYYC",
    "PANC",
    "PAFA",
    "PHOG",
    "PHNL",
    "PHMK",
    "PHTO",
    "EDDF",
    "EGGL",
    "EBBR",
    "EGGW",
    "EGSS",
    "EGKK",
    "EDHI",
    "EDDB",
    "EGGP",
    "EIDW",
    "EGCC",
    "EGPF",
    "EBCI",
    "ENGM",
    "EPWA",
    "ESSA",
    "EFHK",
    "LEMD",
    "LFPG",
    "LIRF",
    "LROP",
    "LIPE",
    "LIRA",
    "LIML",
    "LGEL",
    "LDZA",
    "LOWI",
    "LPPT",
    "KCLE",
    "LOWW",
    "LOWS"
    ]

class InfoB4training(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Continue to flight training", style=discord.ButtonStyle.green, custom_id="vastudent")
    async def first_button_callback(self, button, interaction):
        author = interaction.user
        guild = self.bot.get_guild(965419296937365514)
        role = guild.get_role(1040918463763468369)
        if role in author.roles:
            author = interaction.user
            guild = self.bot.get_guild(965419296937365514)
            role = guild.get_role(1040918463763468369)
            await author.remove_roles(role)
            await interaction.response.send_message("You are no longer a student in the ClearFly VA.",ephemeral=True)
        else:
            author = interaction.user
            guild = self.bot.get_guild(965419296937365514)
            role = guild.get_role(1040918463763468369)
            await author.add_roles(role)
            await interaction.response.send_message("You are now part of the ClearFly VA, get ready for some training!",ephemeral=True)
            channel = self.bot.get_channel(1038062843808972850)
            await channel.send(f"{interaction.user.mention} continue here, run </va training:1016059999056826479> and input your desired destination and origin.")

class VACommands(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(InfoB4training(bot=self.bot))

    
    va = discord.SlashCommandGroup(name="va",description="Commands related to the ClearFly Virtual Airline")
    instructor = va.create_subgroup(name="instructor", description="Commands for the ClearFly Instructors")

    async def get_airports_o(self, ctx: discord.AutocompleteContext):
        return [origin for origin in airports if origin.startswith(ctx.value.upper())]

    async def get_airports_d(self, ctx: discord.AutocompleteContext):
        return [destination for destination in airports if destination.startswith(ctx.value.upper())]

    @va.command(name="setup", description="Sends the required message.")
    @commands.has_role(965422406036488282)
    async def vasetup(self, ctx):
        embed = discord.Embed(title="The ClearFly VA", description="""

        -Click the button below

        ======**GENERAL TRAINING**======

        {-Run the command </va training:1016059999056826479>
        {-Enter your desired origin and destination
        {-Wait for an instructor to approve and assign you required information
        {-Do the flight witht the C172(steam gauges)
        {-Share screenshots of the flight, in one of those screenshots there should be the G430 with the flightplan __clearly visible__
        ⌞______**2X**______⌟
        -------------------------------------------------------------------
        {-Run the command </va training:1016059999056826479> again
        {-Enter your desired origin and destination
        {-Wait for an instructor to approve and assign you required information
        {-Do the flight witht the C172(G1000)
        {-Share screenshots of the flight, let us see that you can use the autopilot
        ⌞______**2X**______⌟
        -------------------------------------------------------------------
        -An instructor will check you off, so you're ready to go to the next phase, type rating!

        ======**TYPE RATING**======

        -Run the command </va training:1016059999056826479>
        -Choose the aircraft you want in the dropdown menu
        {-Run the command </va training:1016059999056826479> again
        {-Enter your desired origin and destination
        {-Wait for an instructor to approve and assign you required information
        {-Share screenshots of the flight were we can see that you are able to use the plane(this includes autopilot except if you're fitted without any navigation system on the B732)
        ⌞______**2X**______⌟
        -An instructor will check you off once again for the final time, you can then fly as much as you want for the VA!""", color=cfc)
        channel1 = self.bot.get_channel(1040927466975404054)
        channel2 = self.bot.get_channel(1041057335449227314)
        await channel1.send(embed=embed, view=InfoB4training
        (bot=self.bot))
        embed = discord.Embed(title="Required plugin: StableApproach", description="""
        Download [here](https://forums.x-plane.org/index.php?/files/file/76763-stableapproach-flight-data-monitoring-for-x-plane/)

        **Setup:**
        **1.** Open the StableApproach settings in the plugins menu.
        **2.** Open the “Virtual Airline” category.
        **3.** Put the text in the box labeled “Virtual Airline”: “ClearFly-Official/StableApproach”.
        **4.** Go to the “Aircraft” tab. Click “Download VA Profile”, and click “Apply + Save”. This will enable StableApproach to use our profile for that aircraft whenever you fly it.
        **5.** That’s it! StableApproach will now download our custom aircraft profiles.
        """, color=cfc)
        await channel2.send(embed=embed)
        await ctx.respond("Done", ephemeral=True)
    
    @va.command(name="training", description="Start your career in the ClearFly VA!")
    @option("origin", description="The airport(ICAO) you will fly from.")
    @option("destination", description="The airport(ICAO) you will fly to.")
    async def vatrain(self,ctx, origin, destination):
        class TypeView(discord.ui.View):
            def __init__(self, bot):
                self.bot = bot
                super().__init__(timeout=None)
                
            @discord.ui.select( 
                placeholder = "Aircraft type", 
                min_values = 1, 
                max_values = 1, 
                options = [ 
                    discord.SelectOption(
                        label="Boeing 737-200",
                        description="By FlyJSim"
                    ),
                    discord.SelectOption(
                        label="Boeing 737-800",
                        description="By Zibo"
                    ),
                    discord.SelectOption(
                        label="Boeing 757-200",
                        description="By Flight Factor"
                    ),
                    discord.SelectOption(
                        label="Airbus A300-600",
                        description="By iniSimulations"
                    ),
                    discord.SelectOption(
                        label="Airbus A300-600F",
                        description="By iniSimulations"
                    ),
                ]
            )
            async def select_callback(self, select, interaction):
                config = configparser.ConfigParser()

                if select.values[0] == "Boeing 737-200":
                    embed = discord.Embed(title="You have selected the Boeing 737-200 as your type rating.", description="Run  </va training:1016059999056826479> again to file your first flight.", color=cfc)
                    await interaction.response.send_message(embed=embed)
                    config.read(f"ClearFly_VA/users/{interaction.user.id}/student.ini")
                    config.set("Student","typed", "1")
                    config.set("Student","type", "B732")
                    with open(f"ClearFly_VA/users/{interaction.user.id}/student.ini", "w") as configfile:
                        config.write(configfile)
                
                if select.values[0] == "Boeing 737-800":
                    embed = discord.Embed(title="You have selected the Boeing 737-800 as your type rating.", description="Run  </va training:1016059999056826479> again to file your first flight.", color=cfc)
                    await interaction.response.send_message(embed=embed)
                    config.read(f"ClearFly_VA/users/{interaction.user.id}/student.ini")
                    config.set("Student","typed", "1")
                    config.set("Student","type", "B738")
                    with open(f"ClearFly_VA/users/{interaction.user.id}/student.ini", "w") as configfile:
                        config.write(configfile)

                if select.values[0] == "Boeing 757-200":
                    embed = discord.Embed(title="You have selected the Boeing 757-200 as your type rating.", description="Run  </va training:1016059999056826479> again to file your first flight.", color=cfc)
                    await interaction.response.send_message(embed=embed)
                    config.read(f"ClearFly_VA/users/{interaction.user.id}/student.ini")
                    config.set("Student","typed", "1")
                    config.set("Student","type", "B752")
                    with open(f"ClearFly_VA/users/{interaction.user.id}/student.ini", "w") as configfile:
                        config.write(configfile)
                
                if select.values[0] == "Airbus A300-600":
                    embed = discord.Embed(title="You have selected the Airbus A300-600 as your type rating.", description="Run  </va training:1016059999056826479> again to file your first flight.", color=cfc)
                    await interaction.response.send_message(embed=embed)
                    config.read(f"ClearFly_VA/users/{interaction.user.id}/student.ini")
                    config.set("Student","typed", "1")
                    config.set("Student","hasAccess", "0")
                    config.set("Student","type", "A306")
                    with open(f"ClearFly_VA/users/{interaction.user.id}/student.ini", "w") as configfile:
                        config.write(configfile)
                
                if select.values[0] == "Airbus A300-600F":
                    embed = discord.Embed(title="You have selected the Airbus A300-600F as your type rating.", description="Run  </va training:1016059999056826479> again to file your first flight.", color=cfc)
                    await interaction.response.send_message(embed=embed)
                    config.read(f"ClearFly_VA/users/{interaction.user.id}/student.ini")
                    config.set("Student","typed", "1")
                    config.set("Student","type", "A306F")
                    with open(f"ClearFly_VA/users/{interaction.user.id}/student.ini", "w") as configfile:
                        config.write(configfile)
        await ctx.defer()
        origin = origin.upper()
        destination = destination.upper()
        user = ctx.author
        config = configparser.ConfigParser()
        guild = self.bot.get_guild(965419296937365514)
        role = guild.get_role(1040918463763468369)
        if os.path.exists(f"ClearFly_VA/users/{user.id}/student.ini"):
            config.read(f"ClearFly_VA/users/{user.id}/student.ini")
            if config.get("Student", "hasAccess") == "1":
                if config.get("Student", "typed") == "0":
                    embed = discord.Embed(title="Choose the aircraf you want to fly!", description="In order to fly for the VA you will need to get a type rating too, to do this select the aircraft you want below and you will be prompted to give origin and a destination. An instructor will approve your flight(just like in your general training), you will need to do 2 flights and then an instructor will check you off once again and then you're good to go to do as many flights for the VA as you want!", color=cfc)
                    await ctx.respond(embed=embed,view=TypeView(bot=self.bot))
                else:
                    if config.get("Student", "ready") == "1":
                        if os.path.exists(f"ClearFly_VA/users/{user.id}/type.txt"):
                            with open(f"ClearFly_VA/users/{user.id}/type.txt", "r") as f:
                                lines = len(f.readlines())
                            if lines == 3:
                                await ctx.respond("You have flown 2 times already, wait to get checked off!")
                                return
                        actype = config.get("Student", "type")
                        embed = discord.Embed(title="Flight Filed!",description="**Wait for a <@&1040918528565444618> to assign you the required information before flying!**\n\n Show screenshots of you doing the flight for confirmation too!", color=cfc)
                        embed.add_field(name="Flight information:", value=f"""
```
Departure:{origin}
Arrival:{destination}
Aircraft: {actype}
```
Have a nice and safe flight!
                                    """)
                        if os.path.exists(f"ClearFly_VA/users/{user.id}/type.txt"):
                            f = open(f"ClearFly_VA/users/{user.id}/type.txt","a")
                            f.write(f"\nType Training {actype} {origin}-{destination}")
                            f.close()
                        else:
                            f = open(f"ClearFly_VA/users/{user.id}/type.txt","a")
                            f.write(f"\nType Training {actype} {origin}-{destination}")
                            f.close()
                        config.set("Student", "ready", "0")
                        with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                            config.write(configfile)
                        await ctx.respond(embed=embed)
                        await ctx.send(f"<@&1040918528565444618> someone needs to get in the air for their flight, give them the required info!")
                    else:
                        await ctx.respond("Wait for an instructor to approve your current flight and after you have done that one you can do another one.")
                        return
            else:
                if role in ctx.author.roles:
                    icaoprefix = ["K", "E", "L", "P", "T", "C"]
                    origin.capitalize()
                    destination.capitalize()
                    if not len(origin) == 4:
                        await ctx.respond("That doesn't seem to be a valid ICAO")
                        return
                    if not len(destination) == 4:
                        await ctx.respond("That doesn't seem to be a valid ICAO")
                        return
                    if origin.startswith(tuple(icaoprefix)) == False:
                        await ctx.respond("You can only fly in Canada, Hawaii, the U.S, and Europe")
                        return
                    if origin.startswith(tuple(icaoprefix)) == False:
                        await ctx.respond("You can only fly in Canada, Hawaii, the U.S, and Europe")
                        return
                    await ctx.respond("Filing flight.")
                    if os.path.exists(f"ClearFly_VA/users/{user.id}/student.ini"):
                        config.read(f"ClearFly_VA/users/{user.id}/student.ini")
                        with open(f"ClearFly_VA/users/{user.id}/student.txt", "r") as f:
                            lines = len(f.readlines())
                        if lines == 5:
                            await ctx.respond("You have flown 4 times already, wait to get checked off!")
                            return
                        if config.get("Student", "ready") == "0":
                            await ctx.respond("Wait for an instructor to approve your current flight and after you have done that one you can do another one.")
                            return
                        else:
                            phase = config.get("Student","phase")
                            config.set("Student","ready", "0")
                            with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                                config.write(configfile)
                    else:
                        os.mkdir(f"ClearFly_VA/users/{user.id}")
                        config.add_section("Student")
                        config.set("Student","phase", "1")
                        config.set("Student","ready", "0")
                        config.set("Student","hasAccess", "0")
                        config.set("Student","typed", "0")
                        config.set("Student","end", "0")
                        phase = "1"
                        with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                            config.write(configfile)
                    if phase == "1":
                        phasetxt = "Your first flight has been filed, welcome!"
                        phasen = "first"
                        paneltype = "Steam Gauges"
                        config.read(f"ClearFly_VA/users/{user.id}/student.ini")
                        config.set("Student","phase", "2")
                        with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                            config.write(configfile)
                    if phase == "2":
                        phasetxt = "Your second flight has been filed"
                        phasen = "second"
                        paneltype = "Steam Gauges"
                        config.read(f"ClearFly_VA/users/{user.id}/student.ini")
                        config.set("Student","phase", "3")
                        with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                            config.write(configfile)
                    if phase == "3":
                        phasetxt = "Your third flight has been filed"
                        phasen = "third"
                        paneltype = "G1000"
                        config.read(f"ClearFly_VA/users/{user.id}/student.ini")
                        config.set("Student","phase", "4")
                        with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                            config.write(configfile)
                    if phase == "4":
                        phasetxt = "Your last training flight has been filed"
                        phasen = "fourth"
                        paneltype = "G1000"
                        with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                            config.write(configfile)
                    embed = discord.Embed(title="Flight Filed!",description="**Wait for a <@&1040918528565444618> to assign you the required information before flying!**\n\n Show screenshots of you doing the flight for confirmation too!", color=cfc)
                    embed.add_field(name=phasetxt, value=f"""
```
Departure:{origin}
Arrival:{destination}
```
Have a nice and safe flight!
                                """)
                    if os.path.exists(f"ClearFly_VA/users/{user.id}"):
                        f = open(f"ClearFly_VA/users/{user.id}/student.txt","a")
                        f.write(f"\nTraining {phase}({paneltype}) {origin}-{destination}")
                        f.close()
                    else:
                        os.mkdir(f"ClearFly_VA/users/{user.id}")
                        f = open(f"ClearFly_VA/users/{user.id}/student.txt","a")
                        f.write(f"\nTraining {phase}({paneltype}) {origin}-{destination}")
                        f.close()
                    await ctx.respond(embed=embed)
                    await ctx.send(f"<@&1040918528565444618> someone needs to get in the air for their {phasen} flight, give them the required info!")
                else:
                    embed = discord.Embed(title="Error 403!", description="You do not have the CF student role. \nGet it in {channel here} before using this command!", color=errorc)
                    await ctx.respond(embed=embed)

        else:
            if role in ctx.author.roles:
                icaoprefix = ["K", "E", "L", "P", "T", "C"]
                origin.capitalize()
                destination.capitalize()
                if not len(origin) == 4:
                    await ctx.respond("That doesn't seem to be a valid ICAO")
                    return
                if not len(destination) == 4:
                    await ctx.respond("That doesn't seem to be a valid ICAO")
                    return
                if origin.startswith(tuple(icaoprefix)) == False:
                    await ctx.respond("You can only fly in Canada, Hawaii, the U.S, and Europe")
                    return
                if origin.startswith(tuple(icaoprefix)) == False:
                    await ctx.respond("You can only fly in Canada, Hawaii, the U.S, and Europe")
                    return
                if os.path.exists(f"ClearFly_VA/users/{user.id}/student.ini"):
                    config.read(f"ClearFly_VA/users/{user.id}/student.ini")
                    if config.get("Student", "ready") == "0":
                        await ctx.respond("Wait for an instructor to approve your current flight and after you have done that one you can do another one.")
                        return
                    else:
                        phase = config.get("Student","phase")
                        config.set("Student","ready", "0")
                        with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                            config.write(configfile)
                else:
                    os.mkdir(f"ClearFly_VA/users/{user.id}")
                    config.add_section("Student")
                    config.set("Student","phase", "1")
                    config.set("Student","ready", "0")
                    config.set("Student","hasAccess", "0")
                    config.set("Student","typed", "0")
                    config.set("Student","end", "0")
                    phase = "1"
                    with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                        config.write(configfile)
                if phase == "1":
                    phasetxt = "Your first flight has been filed, welcome!"
                    phasen = "first"
                    paneltype = "Steam Gauges"
                    config.read(f"ClearFly_VA/users/{user.id}/student.ini")
                    config.set("Student","phase", "2")
                    with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                        config.write(configfile)
                if phase == "2":
                    phasetxt = "Your second flight has been filed"
                    phasen = "second"
                    paneltype = "Steam Gauges"
                    config.read(f"ClearFly_VA/users/{user.id}/student.ini")
                    config.set("Student","phase", "3")
                    with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                        config.write(configfile)
                if phase == "3":
                    phasetxt = "Your third flight has been filed"
                    phasen = "third"
                    paneltype = "G1000"
                    config.read(f"ClearFly_VA/users/{user.id}/student.ini")
                    config.set("Student","phase", "4")
                    with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                        config.write(configfile)
                if phase == "4":
                    phasetxt = "Your last training flight has been filed"
                    phasen = "last"
                    paneltype = "G1000"
                    with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                        config.write(configfile)
                    embed = discord.Embed(title="Flight Filed!",description="**Wait for a <@&1040918528565444618> to assign you the required information before flying!**\n\n Show screenshots of you doing the flight for confirmation too!", color=cfc)
                    embed.add_field(name=phasetxt, value=f"""
```
Departure:{origin}
Arrival:{destination}
```
Have a nice and safe flight!
                            """)
                    if os.path.exists(f"ClearFly_VA/users/{user.id}"):
                        f = open(f"ClearFly_VA/users/{user.id}/student.txt","a")
                        f.write(f"\nTraining {phase}({paneltype}) {origin}-{destination}")
                        f.close()
                else:
                    os.mkdir(f"ClearFly_VA/users/{user.id}")
                    f = open(f"ClearFly_VA/users/{user.id}/student.txt","a")
                    f.write(f"\nTraining {phase}({paneltype}) {origin}-{destination}")
                    f.close()
                    await ctx.respond(embed=embed)
                    await ctx.send(f"<@&1040918528565444618> someone needs to get in the air for their {phasen} flight, give them the required info!")
            else:
                embed = discord.Embed(title="Error 403!", description="You do not have the <@&1040918463763468369> role. \nGet it in <#965686982304997466> before using this command!", color=errorc)
                await ctx.respond(embed=embed)

    @instructor.command(name="approve", description="Approve a student's flight and give the required info to them.")
    @option("comments", required=False)
    async def vaapprove(self, ctx, user: discord.Member, route, crzalt, comments):
        guild = self.bot.get_guild(965419296937365514)
        role = guild.get_role(1040918528565444618)
        if role in ctx.author.roles:
            config = configparser.ConfigParser()
            config.read(f"ClearFly_VA/users/{user.id}/student.ini")
            if config.get("Student", "typed") == "1":
                with open(f'ClearFly_VA/users/{user.id}/type.txt', 'a') as f:
                    f.write(f" - Approved - rte {route.upper()}, crz {crzalt}, cmnts {comments}")
                config.set("Student","ready", "1")
                with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                        config.write(configfile)
                embed = discord.Embed(title="Flight Approved!", description=f"{user.mention}'s flight has been approved and they can take off now.", color=cfc)
                embed.add_field(name="Approved with following data:", value=f"""
```
Route : {route.upper()}
Cruise Altidude : FL{crzalt}
Comments : {comments}
```
                """)
                await ctx.respond(embed=embed)
            else:
                with open(f'ClearFly_VA/users/{user.id}/student.txt', 'a') as f:
                    f.write(f" - Approved - rte {route.upper()}, crz {crzalt}, cmnts {comments}")
                config.set("Student","ready", "1")
                with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                        config.write(configfile)
                embed = discord.Embed(title="Flight Approved!", description=f"{user.mention}'s flight has been approved and they can take off now.", color=cfc)
                embed.add_field(name="Approved with following data:", value=f"""
```
Route : {route.upper()}
Cruise Altidude : FL{crzalt}
Comments : {comments}
```
                """)
                await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="Error 503!", description=f"You are not a {role.mention}!", color=errorc)
            await ctx.respond(embed=embed)

    @instructor.command(name="check-off", description="Check off a user to end their training")
    async def vacheckoff(self, ctx, user: discord.Member):
        guild = self.bot.get_guild(965419296937365514)
        role = guild.get_role(1040918528565444618)
        if role in ctx.author.roles:
            config = configparser.ConfigParser()
            config.read(f"ClearFly_VA/users/{user.id}/student.ini")
            
            role = guild.get_role(1040918463763468369)
            role2 = guild.get_role(1013933799777783849)
            channel = self.bot.get_channel(1013934267966967848)
            if config.get("Student", "typed") == "0":
                with open(f"ClearFly_VA/users/{user.id}/student.txt", "r") as f:
                    lines = len(f.readlines())
                if lines == 5:
                    if config.get("Student", "hasAccess") == "0":
                        await user.remove_roles(role)
                        await user.add_roles(role2)
                        config.set("Student","hasAccess","1")
                        with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                                config.write(configfile)
                        embed = discord.Embed(title=f"{user} has been checked off.", color=cfc)
                        await ctx.respond(embed=embed, ephemeral=True)
                        embed = discord.Embed(title=f"{user} has finished training!", description=f"Congratulations {user.mention}!\n Now you can do your type rating training and then fly as much as you want for the VA.", colour=cfc, timestamp=datetime.now())
                        embed.add_field(name="_ _", value=f"Checked off by {ctx.author.mention}")
                        await channel.send(f"{user.mention}",embed=embed)
                    else:
                        embed = discord.Embed(title="The user has been checked off already.", color=errorc)
                        await ctx.respond(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title="The user hasn't completed enough flights.", color=errorc)
                    await ctx.respond(embed=embed, ephemeral=True)
            else:
                with open(f"ClearFly_VA/users/{user.id}/type.txt", "r+") as f:
                    lines = len(f.readlines())
                if lines == 3:
                    if config.get("Student", "end") == "0":
                        config.set("Student", "end", "1")
                        await user.remove_roles(role)
                        await user.add_roles(role2)
                        actype = config.get("Student", "type")
                        if actype == "B732":
                            role3 = guild.get_role(1040918288525438996)
                        if actype == "B738":
                            role3 = guild.get_role(1040918323573047366)
                        if actype == "A306":
                            role3 = guild.get_role(1040918215188037633)
                        if actype == "A306F":
                            role3 = guild.get_role(1040918248100737054)
                        if actype == "B752":
                            role3 = guild.get_role(1040936249474695229)
                        await user.add_roles(role3)
                        config.set("Student","hasAccess","1")
                        with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                                config.write(configfile)
                        embed = discord.Embed(title=f"{user} has been checked off.", color=cfc)
                        await ctx.respond(embed=embed, ephemeral=True)
                        embed = discord.Embed(title=f"{user} has fully finished training for the {actype}!", description=f"Congratulations {user.mention}!\n Now you can fly as much as you want for the VA!", colour=cfc, timestamp=datetime.now())
                        embed.add_field(name="_ _", value=f"Checked off by {ctx.author.mention}")
                        await channel.send(f"{user.mention}",embed=embed)
                    else:
                        embed = discord.Embed(title="The user has been checked off already.", color=errorc)
                        await ctx.respond(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title="The user hasn't completed enough flights.", color=errorc)
                    await ctx.respond(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Error 503!", description=f"You are not a {role.mention}!", color=errorc)
            await ctx.respond(embed=embed)

    @va.command(name="file", description="File a flight that you will do for the Clearfly VA.")
    @option("aircraft", description="The aircraft you will use for the flight.", choices=["B732", "B738", "B752","A306", "A306F"])
    @option("origin", description="The airport(ICAO) you will fly from.", autocomplete=get_airports_o)
    @option("destination", description="The airport(ICAO) you will fly to.", autocomplete=get_airports_d)
    async def file(self, ctx, aircraft, origin, destination):
        await ctx.defer()
        config = configparser.ConfigParser()
        if os.path.exists(f"ClearFly_VA/users/{ctx.author.id}/student.ini"):
            config.read(f"ClearFly_VA/users/{ctx.author.id}/student.ini")
            if config.get("Student", "end") == "1":
                if (origin in airports) and (destination in airports):
                    dest = 1
                    ori = 1
                    if dest == 1:
                        if destination == "KDCA":
                            cf1 = 1
                        if destination == "KIAD":
                            cf1 = 2
                        if destination == "KLGA":
                            cf1 = 3
                        if destination == "KMSP":
                            cf1 = 4
                        if destination == "KORD":
                            cf1 = 5
                        if destination == "KMDW":
                            cf1 = 6
                        if destination == "KMKE":
                            cf1 = 7
                        if destination == "KSFO":
                            cf1 = 8
                        if destination == "KLAX":
                            cf1 = 9
                        if destination == "KPHX":
                            cf1 = 10
                        if destination == "KSEA":
                            cf1 = 11
                        if destination == "KPDX":
                            cf1 = 12
                        if destination == "KRIC":
                            cf1 = 13
                        if destination == "KMIA":
                            cf1 = 14
                        if destination == "KSTL":
                            cf1 = 15
                        if destination == "KBOS":
                            cf1 = 16
                        if destination == "KIND":
                            cf1 = 17
                        if destination == "KIAH":
                            cf1 = 18
                        if destination == "KAUS":
                            cf1 = 19
                        if destination == "KDFW":
                            cf1 = 20
                        if destination == "KPIT":
                            cf1 = 21
                        if destination == "KATL":
                            cf1 = 22
                        if destination == "KSAN":
                            cf1 = 23
                        if destination == "CYVR":
                            cf1 = 24
                        if destination == "CYYQ":
                            cf1 = 25
                        if destination == "CYVO":
                            cf1 = 26
                        if destination == "CYUL":
                            cf1 = 27
                        if destination == "CYQB":
                            cf1 = 28
                        if destination == "CYYZ":
                            cf1 = 29
                        if destination == "CYOW":
                            cf1 = 30
                        if destination == "CYYJ":
                            cf1 = 31
                        if destination == "PANC":
                            cf1 = 32
                        if destination == "PAFA":
                            cf1 = 33
                        if destination == "PHOG":
                            cf1 = 34
                        if destination == "PHNL":
                            cf1 = 35
                        if destination == "PHMK":
                            cf1 = 36
                        if destination == "PHTO":
                            cf1 = 37
                        if destination == "EDDF":
                            cf1 = 38
                        if destination == "EGGL":
                            cf1 = 39
                        if destination == "EBBR":
                            cf1 = 40
                        if destination == "EGGW":
                            cf1 = 41
                        if destination == "EGSS":
                            cf1 = 42
                        if destination == "EGKK":
                            cf1 = 43
                        if destination == "EDHI":
                            cf1 = 44
                        if destination == "EDDB":
                            cf1 = 45
                        if destination == "EGGP":
                            cf1 = 46
                        if destination == "EIDW":
                            cf1 = 47
                        if destination == "EGCC":
                            cf1 = 48
                        if destination == "EGPF":
                            cf1 = 49
                        if destination == "EBCI":
                            cf1 = 50
                        if destination == "ENGM":
                            cf1 = 51
                        if destination == "EPWA":
                            cf1 = 52
                        if destination == "ESSA":
                            cf1 = 53
                        if destination == "EFHK":
                            cf1 = 54
                        if destination == "LEMD":
                            cf1 = 55
                        if destination == "LFPG":
                            cf1 = 56
                        if destination == "LIRF":
                            cf1 = 57
                        if destination == "LROP":
                            cf1 = 58
                        if destination == "LIPE":
                            cf1 = 59
                        if destination == "LIRA":
                            cf1 = 60
                        if destination == "LIML":
                            cf1 = 61
                        if destination == "LGEL":
                            cf1 = 62
                        if destination == "LDZA":
                            cf1 = 63
                        if destination == "LOWI":
                            cf1 = 64
                        if destination == "LPPT":
                            cf1 = 65
                        if destination == "KCLE":
                            cf1 = 66
                        if destination == "LOWW":
                            cf1 = 67
                        if destination == "LOWS":
                            cf1 = 68
                    if ori == 1:
                        if origin == "KDCA":
                            cf2 = 23
                        if origin == "KIAD":
                            cf2 = 22
                        if origin == "KLGA":
                            cf2 = 21
                        if origin == "KMSP":
                            cf2 = 20
                        if origin == "KORD":
                            cf2 = 19
                        if origin == "KMDW":
                            cf2 = 18
                        if origin == "KMKE":
                            cf2 = 17
                        if origin == "KSFO":
                            cf2 = 16
                        if origin == "KLAX":
                            cf2 = 15
                        if origin == "KPHX":
                            cf2 = 14
                        if origin == "KSEA":
                            cf2 = 13
                        if origin == "KPDX":
                            cf2 = 12
                        if origin == "KRIC":
                            cf2 = 11
                        if origin == "KMIA":
                            cf2 = 10
                        if origin == "KSTL":
                            cf2 = 9
                        if origin == "KBOS":
                            cf2 = 8
                        if origin == "KIND":
                            cf2 = 7
                        if origin == "KIAH":
                            cf2 = 6
                        if origin == "KAUS":
                            cf2 = 5
                        if origin == "KDFW":
                            cf2 = 4
                        if origin == "KPIT":
                            cf2 = 3
                        if origin == "KSAN":
                            cf2 = 2
                        if origin == "KATL":
                            cf2 = 1
                        if origin == "CYVR":
                            cf2 = 65
                        if origin == "CYYQ":
                            cf2 = 64
                        if origin == "CYVO":
                            cf2 = 63
                        if origin == "CYUL":
                            cf2 = 62
                        if origin == "CYQB":
                            cf2 = 61
                        if origin == "CYYZ":
                            cf2 = 60
                        if origin == "CYOW":
                            cf2 = 59
                        if origin == "CYYJ":
                            cf2 = 58
                        if origin == "PANC":
                            cf2 = 57
                        if origin == "PAFA":
                            cf2 = 56
                        if origin == "PHOG":
                            cf2 = 55
                        if origin == "PHNL":
                            cf2 = 54
                        if origin == "PHMK":
                            cf2 = 53
                        if origin == "PHTO":
                            cf2 = 52
                        if origin == "EDDF":
                            cf2 = 51
                        if origin == "EGGL":
                            cf2 = 50
                        if origin == "EBBR":
                            cf2 = 49
                        if origin == "EGGW":
                            cf2 = 48
                        if origin == "EGSS":
                            cf2 = 47
                        if origin == "EGKK":
                            cf2 = 46
                        if origin == "EDHI":
                            cf2 = 45
                        if origin == "EDDB":
                            cf2 = 44
                        if origin == "EGGP":
                            cf2 = 43
                        if origin == "EIDW":
                            cf2 = 42
                        if origin == "EGCC":
                            cf2 = 41
                        if origin == "EGPF":
                            cf2 = 40
                        if origin == "EBCI":
                            cf2 = 39
                        if origin == "ENGM":
                            cf2 = 38
                        if origin == "EPWA":
                            cf2 = 37
                        if origin == "ESSA":
                            cf2 = 36
                        if origin == "EFHK":
                            cf2 = 35
                        if origin == "LEMD":
                            cf2 = 34
                        if origin == "LFPG":
                            cf2 = 33
                        if origin == "LIRF":
                            cf2 = 32
                        if origin == "LROP":
                            cf2 = 31
                        if origin == "LIPE":
                            cf2 = 30
                        if origin == "LIRA":
                            cf2 = 29
                        if origin == "LIML":
                            cf2 = 28
                        if origin == "LGEL":
                            cf2 = 27
                        if origin == "LDZA":
                            cf2 = 26
                        if origin == "LOWI":
                            cf2 = 25
                        if origin == "LPPT":
                            cf2 = 24
                        if origin == "KCLE":
                            cf2 = 23
                        if origin == "LOWW":
                            cf2 = 22
                        if origin == "LOWS":
                            cf2 = 21
                    if aircraft == "B732":
                        cf3 = 1
                    if aircraft == "B738":
                        cf3 = 2
                    if aircraft == "A306":
                        cf3 = 3
                    if aircraft == "A306F":
                        cf3 = 4
                    if aircraft == "B752":
                        cf3 = 5
                    if not aircraft == config.get("Student", "type"):
                        embed=discord.Embed(title="Error 503!", description="You need to have a type rating of this aircraft if you want to fly it!", color=errorc)
                        await ctx.respond(embed=embed)
                        return
                    user = ctx.author
                    embed = discord.Embed(title="Flight Filed!", color=cfc)
                    flightnumber = f"{int(cf1+cf2)}"+str(cf3)
                    embed.add_field(name="Your flight has been filed with the following data:", value=f"""
    ```
    Aircraft:{aircraft}
    Departure:{origin}
    Arrival:{destination}
    Flight Number: CF{flightnumber}
    ```
    Have a nice and safe flight!
                                """)
                    if os.path.exists(f"ClearFly_VA/users/{user.id}"):
                            f = open(f"ClearFly_VA/users/{user.id}/data.txt","a")
                            f.write(f"\nCF{flightnumber}, {aircraft}, {origin}-{destination}")
                            f.close()
                    else:
                            os.mkdir(f"ClearFly_VA/users/{user.id}")
                            f = open(f"ClearFly_VA/users/{user.id}/data.txt","a")
                            f.write(f"\nCF{flightnumber}, {aircraft}, {origin}-{destination}")
                            f.close()
                    if aircraft == "B732":
                        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1038060095902330952/1038065978019430430/FJS_732_TwinJet_icon11_thumb.png")
                    if aircraft == "B738":
                        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1038060053896364063/1038065018983432242/b738_4k_icon11_thumb.png")
                    if aircraft == "A300":
                        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1013239106198835300/1015290004001542164/A300_P_V2_-_2022-08-31_00.37.05.PNG")
                    if aircraft == "A300F":
                        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1038063084733997178/1038065483234164837/A300_F_V2_icon11_thumb.png")
                    await ctx.respond(embed=embed)
                else:
                    embed=discord.Embed(title="Error 422!", description="The origin/destination you provided are airports we do not fly to, please choose an airport that comes up while using the command.", color=errorc)
                    await ctx.respond(embed=embed)
            else:
                embed=discord.Embed(title="Error 503!", description="You need to train before using this command", color=errorc)
                await ctx.respond(embed=embed)
        else:
                embed=discord.Embed(title="Error 503!", description="You need to train before using this command", color=errorc)
                await ctx.respond(embed=embed)

    
    @va.command(name="report-incident", description="Something happened on your flight? Run this command and tell us what happened!")
    @option("flightnumber", description="The flight number of the flight where the accident happened.")
    @option("report", description="A short text that explained what happened.")
    async def vareport(self, ctx, flightnumber,report):
        config = configparser.ConfigParser()
        if os.path.exists(f"ClearFly_VA/users/{ctx.author.id}/student.ini"):
            config.read(f"ClearFly_VA/users/{ctx.author.id}/student.ini")
            if config.get("Student", "end") == "1":
                with open(f"ClearFly_VA/users/{ctx.author.id}/data.txt", 'a') as f:
                    f.write(f"/Incident")
                embed = discord.Embed(title=f"Report submitted!", color=cfc)
                await ctx.respond(embed=embed)
                if os.path.exists(f"ClearFly_VA/users/{ctx.author.id}/reports.txt"):
                    with open(f"ClearFly_VA/users/{ctx.author.id}/reports.txt", 'a') as f:
                        f.write(f"\n # {datetime.now()} | {flightnumber} # \n\n{report}\n")
                else:
                    with open(f"ClearFly_VA/users/{ctx.author.id}/reports.txt", 'w') as f:
                        f.write(f"# {datetime.now()} | {flightnumber} # \n\n{report}\n")
            else:
                embed=discord.Embed(title="Error 503!", description="You need to train before using this command", color=errorc)
                await ctx.respond(embed=embed)
        else:
                embed=discord.Embed(title="Error 503!", description="You need to train before using this command", color=errorc)
                await ctx.respond(embed=embed)
            
    @va.command(name="divert", description="If you need to divert to another airport you can with this command.")
    @option("divert", description="The airport you will divert/have diverted to.")
    async def divert(self, ctx, airport):
        config = configparser.ConfigParser()
        if os.path.exists(f"ClearFly_VA/users/{ctx.author.id}/student.ini"):
            config.read(f"ClearFly_VA/users/{ctx.author.id}/student.ini")
            if config.get("Student", "end") == "1":
                if not len(airport) == 4:
                    embed=discord.Embed(title="Error 404!", description="That doesn't seem to be a valid ICAO code", color=errorc)
                    await ctx.respond(embed=embed)
                else:
                    with open(f"ClearFly_VA/users/{ctx.author.id}/data.txt", 'a') as f:
                        f.write(f"/Divert2({airport})")
                    embed = discord.Embed(title=f"Flight diverted to {airport}!", color=cfc)
                    await ctx.respond(embed=embed)
            else:
                embed=discord.Embed(title="Error 503!", description="You need to train before using this command", color=errorc)
                await ctx.respond(embed=embed)
        else:
                embed=discord.Embed(title="Error 503!", description="You need to train before using this command", color=errorc)
                await ctx.respond(embed=embed)

    @va.command(name="cancel", description="Cancels and removes your last filed flight.")
    async def cancel(self, ctx):
        config = configparser.ConfigParser()
        if os.path.exists(f"ClearFly_VA/users/{ctx.author.id}/student.ini"):
            config.read(f"ClearFly_VA/users/{ctx.author.id}/student.ini")
            if config.get("Student", "end") == "1":
                if os.path.exists(f"ClearFly_VA/users/{ctx.author.id}/data.txt"):
                    with open(f"ClearFly_VA/users/{ctx.author.id}/data.txt", "r+", encoding = "utf-8") as f:
                        f.seek(0, os.SEEK_END)
                        pos = f.tell() - 1
                        while pos > 0 and f.read(1) != "\n":
                            pos -= 1
                            f.seek(pos, os.SEEK_SET)
                        if pos > 0:
                            f.seek(pos, os.SEEK_SET)
                            f.truncate()
                    embed = discord.Embed(title="Flight canceled!", color=cfc)
                    await ctx.respond(embed=embed)
                else:
                    embed=discord.Embed(title="Error 404!", description="Didn't found any flights, you should file at least one flight to use this command!", color=errorc)
                    await ctx.respond(embed=embed)
            else:
                embed=discord.Embed(title="Error 503!", description="You need to train before using this command", color=errorc)
                await ctx.respond(embed=embed)
        else:
                embed=discord.Embed(title="Error 503!", description="You need to train before using this command", color=errorc)
                await ctx.respond(embed=embed)

    @va.command(name="flights", description="Fetches flights a user has done.")
    @option("user", description="The user you want flight(s) information about.")
    async def flights(self, ctx, user: discord.Member = None):
        await ctx.defer()
        if user == None:
            author = ctx.author
            if os.path.exists(f"ClearFly_VA/users/{author.id}/data.txt"):
                with open(f"ClearFly_VA/users/{author.id}/data.txt","r") as f:
                    datar = f.read()
                with open(rf"ClearFly_VA/users/{author.id}/data.txt") as f:
                    no = len(f.readlines())
                    nof = no-1
                embed = discord.Embed(title=f"Your flights:", color=cfc, description=f"""
```
{datar}
```
Number of flights: **{nof}**
            """)
                if os.path.exists(f"ClearFly_VA/users/{author.id}/reports.txt"):
                    with open(f"ClearFly_VA/users/{author.id}/reports.txt") as f:
                        reports = f.read()
                    embed.add_field(name="Incidents:", value=f"""
```md
{reports}
```
                        """)
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="Error 404!", description=f"No flights were found for {author.mention}, make sure they have flights filed!", color=errorc)
                await ctx.respond(embed=embed)
        else:
            if os.path.exists(f"ClearFly_VA/users/{user.id}/data.txt"):
                with open(f"ClearFly_VA/users/{user.id}/data.txt","r") as f:
                    datar = f.read()
                with open(rf"ClearFly_VA/users/{user.id}/data.txt") as f:
                    no = len(f.readlines())
                    nof = no-1
                embed = discord.Embed(title=f"{user}'s flights:", color=cfc, description=f"""
```
{datar}
```
Number of flights: **{nof}**
            """)
                if os.path.exists(f"ClearFly_VA/users/{user.id}/reports.txt"):
                    with open(f"ClearFly_VA/users/{user.id}/reports.txt") as f:
                        reports = f.read()
                    embed.add_field(name="Incidents:", value=f"""
```md
{reports}
```
                    """)
                    await ctx.respond(embed=embed)
                else:
                    await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="Error 404!", description=f"No flights were found for {user.mention}, make sure they have flights filed!", color=errorc)
                await ctx.respond(embed=embed)

    @discord.user_command(name="User VA Flights")
    async def flights_app(self, ctx, user: discord.Member):
        await ctx.defer()
        if os.path.exists(f"ClearFly_VA/users/{user.id}/data.txt"):
            with open(f"ClearFly_VA/users/{user.id}/data.txt","r") as f:
                datar = f.read()
            with open(rf"ClearFly_VA/users/{user.id}/data.txt") as f:
                no = len(f.readlines())
                nof = no-1
            embed = discord.Embed(title=f"{user}'s flights:", color=cfc, description=f"""
```
{datar}
```
Number of flights: **{nof}**
        """)
            if os.path.exists(f"ClearFly_VA/users/{user.id}/reports.txt"):
                with open(f"ClearFly_VA/users/{user.id}/reports.txt") as f:
                    reports = f.read()
                embed.add_field(name="Incidents:", value=f"""
```md
{reports}
```
                """)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="Error 404!", description=f"No flights were found for {user.mention}, make sure they have flights filed!", color=errorc)
            await ctx.respond(embed=embed)

    @va.command(name="stats", description="Show general statistics about the whole VA.")
    async def vastats(self, ctx):
        cmnac = []
        output = 0
        cmndestoutput = []
        index = 0
        cmndest = []
        for index, filename in enumerate(glob.glob('ClearFly_VA/users/*/data.txt')):
            with open(os.path.join(os.getcwd(), filename), 'r') as f:
                lines = f.readlines()
                cmnac = cmnac+lines
                cmndest = cmndest+lines
                nof = int(len(lines))
                index = index+1
                output = output+nof-1
        def delstr2(lst):
            return [
                f"{''.join(elem.split()[2:]).rstrip()}"
                for elem in lst
            ]

        
        cmndest = delstr2(cmndest)
        for x in cmndest:
            x = re.sub(r'.', '', x, count = 5)
            cmndestoutput.append(x)
        def movestr(lst):
                return [
                    f"{' '.join(elem.split()[2:]).rstrip()} {' '.join(elem.split()[:2])}\n"
                    for elem in lst
                ]
        def delstr(lst):
                    return [
                        f"{' '.join(elem.split()[1:]).rstrip()}"
                        for elem in lst
                    ]
        cmnac = movestr(cmnac)
        cmnac = delstr(cmnac)
        cmnac = delstr(cmnac)
        while ("" in cmnac):
            cmnac.remove("")
        def most_frequent(List):
                    return max(set(List), key = List.count)
        cmndestoutput = list(filter(None, cmndestoutput))
        cmndest = most_frequent(cmndestoutput)
        cmnac = f"{most_frequent(cmnac)}".replace(",","")
        embed = discord.Embed(title="ClearFly VA Statistics", color=cfc)
        embed.add_field(name="Total Flights:", value=f" {output}")
        embed.add_field(name="Most Common Aircraft:", value=f" {cmnac}")
        embed.add_field(name="Most Common Destination:", value=f" {cmndest[:4]}")
        embed.add_field(name="_ _", value="\n*Notice: Both 'Most Common Aircraft' and 'Most Common Destination' will have a random selected value of 2 or more elements with the same frequency if that is the case.*", inline=True)
        await ctx.respond(embed=embed)

    @va.command(name="leaderboard", description="Get the leaderboard of who flew the most flights!")
    async def valb(self, ctx):
        await ctx.defer()
        if os.path.exists(".onpc"):
            output = []
            nameoutput = []
            img = Image.open(f"images/lbClear.png")
            for index, filename in enumerate(glob.glob('ClearFly_VA/users/*/data.txt')):
                with open(os.path.join(os.getcwd(), filename), 'r') as f:
                    nof = f"{int(len(f.readlines()))-1}"
                    filen = filename.replace("ClearFly_VA/users/", f"")
                    id=os.path.dirname(filen)
                    user = self.bot.get_user(int(id))
                    line = f"{nof} Flights flown: \n"
                    line2 = f"{nof} {user.name}"
                    output.append(line)
                    nameoutput.append(line2)
            output.sort(reverse=True)
            nameoutput.sort(reverse=True)
            def movestr(lst):
                return [
                    f"{' '.join(elem.split()[1:]).rstrip()} {' '.join(elem.split()[:1])}\n"
                    for elem in lst
                ]
                
            output = movestr(output)
            def delstr(lst):
                return [
                    f"{' '.join(elem.split()[1:]).rstrip()}"
                    for elem in lst
                ]
                
            nameoutput = delstr(nameoutput)
            nameoutput = [f'{index}       {i}' for index, i in enumerate(nameoutput, 1)]
            output = [direction + '\n' for direction in output]
            nameoutput = [direction + '\n\n' for direction in nameoutput]
            embed = discord.Embed(title="ClearFly VA Leaderboard", color=cfc)
            I1 = ImageDraw.Draw(img)
            font = ImageFont.truetype("fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf", size=44, layout_engine=ImageFont.Layout.BASIC)
            I1.text((790, 30), "".join(output[:10]), fill=(255, 255, 255), font=font)
            I1.text((27,30), "".join(nameoutput[:10]), fill=(255, 255, 255), font=font)
            img.save(f"images/valb.png")
            file = discord.File(f"images/valb.png", filename="valb.png")
            embed.set_image(url=f"attachment://valb.png")
            await ctx.respond(embed=embed, file=file)
        else:
            output = []
            for index, filename in enumerate(glob.glob('ClearFly_VA/users/*/data.txt')):
                with open(os.path.join(os.getcwd(), filename), 'r') as f:
                    nof = f"{int(len(f.readlines()))-1}"
                    filen = filename.replace("ClearFly_VA/users/", f"")
                    id=os.path.dirname(filen)
                    user = self.bot.get_user(int(id))
                    line = f"| Flights flown:{nof} {user.name}\n"
                    output.append(line)
            output.sort(reverse=True)
            def movestr(lst):
                return [
                    f"{' '.join(elem.split()[3:]).rstrip()} {' '.join(elem.split()[:3])}\n"
                    for elem in lst
                ]
                
            output = movestr(output)
            foutput = [f'{index} | {i}' for index, i in enumerate(output, 1)]
            embed = discord.Embed(title="ClearFly VA Leaderboard", description=f"""
```
{"".join(foutput)}
```
            """, color=cfc)
            await ctx.respond(embed=embed)


    @va.command(name="liveries", description="Looking to fly for the ClearFly VA? Here are the liveries to get you started!")
    @option("noauth", description="Makes the bot respond or send the output.")
    async def valivs(self, ctx, noauth:bool = False):
        if noauth == False:
            button1 = Button(label="Boeing 737-800 by Zibo", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/1bNXkHHlItE-MhfM6Nc-l5-W75zW9thYP/view?usp=share_link")
            button2 = Button(label="Boeing 737-200 by FlyJSim", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/1o1vQk_HG1iJhJH1t_Z8cLBimDwxG90-C/view?usp=share_link")
            button3 = Button(label="Airbus A300-600 by IniSimulations", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/1vdIOYlcM_2kNhooD_CTDE8UpoJ7mIvkk/view?usp=share_link")
            button4 = Button(label="Airbus A300-600F by IniSimulations", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/1w6kd3H0VBiWoTlmcvvvyte5wbqHE7i5k/view?usp=share_link")
            button5 = Button(label="Cessna 172SP by Laminar Research", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/17FqPHGWHXyG8jgXhJBSgDEbKZMWtOqmc/view?usp=share_link")
            view = View()
            view.add_item(button1)
            view.add_item(button2)
            view.add_item(button3)
            view.add_item(button4)
            view.add_item(button5)
            embed=discord.Embed(title="ClearFly VA Official Liveries:",color=cfc)
            await ctx.respond(embed=embed, view=view)
        else:
            button1 = Button(label="Boeing 737-800 by Zibo", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/1bNXkHHlItE-MhfM6Nc-l5-W75zW9thYP/view?usp=share_link")
            button2 = Button(label="Boeing 737-200 by FlyJSim", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/1o1vQk_HG1iJhJH1t_Z8cLBimDwxG90-C/view?usp=share_link")
            button3 = Button(label="Airbus A300-600 by IniSimulations", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/1vdIOYlcM_2kNhooD_CTDE8UpoJ7mIvkk/view?usp=share_link")
            button4 = Button(label="Airbus A300-600F by IniSimulations", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/1w6kd3H0VBiWoTlmcvvvyte5wbqHE7i5k/view?usp=share_link")
            button5 = Button(label="Cessna 172SP by Laminar Research", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/17FqPHGWHXyG8jgXhJBSgDEbKZMWtOqmc/view?usp=share_link")
            view = View()
            view.add_item(button1)
            view.add_item(button2)
            view.add_item(button3)
            view.add_item(button4)
            view.add_item(button5)
            embed=discord.Embed(title="ClearFly VA Official Liveries:",color=cfc)
            await ctx.respond("See below", ephemeral=True)
            await ctx.send(embed=embed, view=view)
            
def setup(bot):
    bot.add_cog(VACommands(bot))