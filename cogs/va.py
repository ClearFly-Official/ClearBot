import discord
from discord.ext import commands
from discord.est import Option

class VAcommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    va = SlashCommandGroup(name="va",description="Commands related to the ClearFly Virtual Airline")

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
        "KATL"
    ]

    async def get_airports_o(ctx: discord.AutocompleteContext):
        return [origin for origin in airports if origin.startswith(ctx.value.upper())]

    async def get_airports_d(ctx: discord.AutocompleteContext):
        return [destination for destination in airports if destination.startswith(ctx.value.upper())]

    @va.command(name="file", descriprion="File a flight that you will do for the Clearfly VA.")
    @option("aircraft", description="The aircraft you will use for the flight.(for more aircraft send a dm to WolfAir)", choices=["B732", "B738", "A300"])
    @option("origin", description="The airport(ICAO) you will fly from.", autocomplete=get_airports_o)
    @option("destination", description="The airport(ICAO) you will fly to.", autocomplete=get_airports_d)
    async def file(ctx, aircraft, origin, destination):
        if ctx.author == 668874138160594985:
            guild = bot.get_guild(965419296937365514)
            cfpilot = guild.get_role(1013933799777783849)
            if cfpilot in ctx.author.roles:
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
            if ori == 1:
                if origin == "KDCA":
                cf2 = 1
                if origin == "KIAD":
                cf2 = 2
                if origin == "KLGA":
                cf2 = 3
                if origin == "KMSP":
                cf2 = 4
                if origin == "KORD":
                cf2 = 5
                if origin == "KMDW":
                cf2 = 6
                if origin == "KMKE":
                cf2 = 7
                if origin == "KSFO":
                cf2 = 8
                if origin == "KLAX":
                cf2 = 9
                if origin == "KPHX":
                cf2 = 10
                if origin == "KSEA":
                cf2 = 11
                if origin == "KPDX":
                cf2 = 12
                if origin == "KRIC":
                cf2 = 13
                if origin == "KMIA":
                cf2 = 14
                if origin == "KSTL":
                cf2 = 15
                if origin == "KBOS":
                cf2 = 16
                if origin == "KIND":
                cf2 = 17
                if origin == "KIAH":
                cf2 = 18
                if origin == "KAUS":
                cf2 = 19
                if origin == "KDFW":
                cf2 = 20
                if origin == "KPIT":
                cf2 = 21
                if origin == "KSAN":
                cf2 = 22
                if origin == "KATL":
                cf2 = 22
            user = ctx.author
            await ctx.respond("Filing flight.")
            sleep(0.1)
            await ctx.edit(content="Filing flight..")
            embed = discord.Embed(title="Flight Filed!", color=cfc)
            flightnumber = cf1+cf2
            embed.add_field(name="Your flight has been filed with the following data:", value=f"""
            ```
            Aircraft:{aircraft}
            Departure:{origin}
            Arrival:{destination}
            Flight Number: CF{flightnumber}
            ```
            Have a nice and safe flight!
                        """)
            await ctx.edit(content="Filing flight...")
            await ctx.edit(content="Filing flight.")
            if os.path.exists(f"ClearFly_VA/users/{user.id}"):
                f = open(f"ClearFly_VA/users/{user.id}/data.txt","a")
                f.write(f"\nCF{flightnumber}, {aircraft}, {origin}-{destination}")
                f.close()
            else:
                os.mkdir(f"ClearFly_VA/users/{user.id}")
                f = open(f"ClearFly_VA/users/{user.id}/data.txt","a")
                f.write(f"\nCF{flightnumber}, {aircraft}, {origin}-{destination}")
                f.close()
            await ctx.edit(content="Uploading to database.")
            await ctx.edit(content="Uploading to database..")
            await ctx.edit(content="Uploading to database...")
            if aircraft == "B732":
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1013239106198835300/1015310203832516731/FJS_732_TwinJet_-_2022-09-02_13.20.01.png")
            if aircraft == "B738":
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1013239106198835300/1015290133601320980/b738_4k_-_2022-08-29_16.09.22.PNG")
            if aircraft == "A300":
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1013239106198835300/1015290004001542164/A300_P_V2_-_2022-08-31_00.37.05.PNG")
            await ctx.edit(content=None, embed=embed)
            else:
            embed = discord.Embed(title="Error 403!", description="You do not have the <@&1013933799777783849> role. \nGet it in <#965686982304997466> before using this command!", color=errorc)
            await ctx.respond(embed=embed)
        else:
            embed=discord.Embed(title="Error 503!", description="Most ClearFly VA commands are disabled at the moment, read <#1013934267966967848> for more information.", color=cfc)
            await ctx.respond(embed=embed)

    @va.command(name="flights", descripiton="Fetches flights a user has done.")
    async def flights(ctx, user: discord.Member = None):
    if ctx.author == 668874138160594985:
        guild = bot.get_guild(965419296937365514)
        cfpilot = guild.get_role(1013933799777783849)
        if cfpilot in ctx.author.roles:
        if user == None:
            author = ctx.author.id
            await ctx.respond(f"loading your filed flights.")
            sleep(0.5)
            await ctx.edit(content=f"loading your filed flights..")
            sleep(0.5)
            await ctx.edit(content=f"loading your filed flights...")
            if os.path.exists(f"ClearFly_VA/users/{author}"):
                f = open(f"ClearFly_VA/users/{author}/data.txt","r")
                with open(rf"ClearFly_VA/users/{author}/data.txt") as fp:
                    no = len(fp.readlines())
                    nof = no-1
                datar = f.read()
                embed = discord.Embed(title=f"Your Flights:", color=cfc, description=f"""
                ```
                {datar}
                ```
                Number of Flights: {nof}
                """)
                await ctx.edit(content=None,embed=embed)
                f.close()
            else:
                embed = discord.Embed(title="Error 404!", description=f"No flights we're found for you, make sure you have flights filed!", color=errorc)
                await ctx.edit(content=None, embed=embed)
        else:
                await ctx.respond(f"Loading {user}'s Filed Flights.")
                sleep(0.5)
                await ctx.edit(content=f"Loading {user}'s Filed flights..")
                sleep(0.5)
                await ctx.edit(content=f"Loading {user}'s Filed flights...")
                if os.path.exists(f"ClearFly_VA/users/{user.id}"):
                    f = open(f"ClearFly_VA/users/{user.id}/data.txt","r")
                    with open(rf"ClearFly_VA/users/{user.id}/data.txt") as fp:
                        no = len(fp.readlines())
                        nof = no-1
                    datar = f.read()
                    embed = discord.Embed(title=f"{user}'s Flights:", color=cfc, description=f"""
                    ```
                    {datar}
                    ```
                    Number of Flights: {nof}
                    """)
                    await ctx.edit(content=None,embed=embed)
                    f.close()
                else:
                    embed = discord.Embed(title="Error 404!", description=f"No flights we're found for {user.mention}, make sure they have flights filed!", color=errorc)
                    await ctx.edit(content=None, embed=embed)
        else:
        embed = discord.Embed(title="Error 403!", description="You do not have the <@&1013933799777783849> role. \nGet it in <#965686982304997466> before using this command!", color=errorc)
        await ctx.respond(embed=embed)
    else:
        embed=discord.Embed(title="Error 503!", description="Most ClearFly VA commands are disabled at the moment, read <#1013934267966967848> for more information.", color=errorc)
        await ctx.respond(embed=embed)

    @bot.user_command(name="User VA Flights")
    async def flights_app(ctx, user: discord.Member):
        if ctx.author == 668874138160594985:
        guild = bot.get_guild(965419296937365514)
        cfpilot = guild.get_role(1013933799777783849)
        if cfpilot in ctx.author.roles:
            await ctx.respond(f"Loading {user}'s Filed Flights.")
            sleep(0.5)
            await ctx.edit(content=f"Loading {user}'s Filed flights..")
            sleep(0.5)
            await ctx.edit(content=f"Loading {user}'s Filed flights...")
            if os.path.exists(f"ClearFly_VA/users/{user.id}"):
                    f = open(f"ClearFly_VA/users/{user.id}/data.txt","r")
                    with open(rf"ClearFly_VA/users/{user.id}/data.txt") as fp:
                        no = len(fp.readlines())
                        nof = no-1
                    datar = f.read()
                    embed = discord.Embed(title=f"{user}'s Flights:", color=cfc, description=f"""
                    ```
                    {datar}
                    ```
                    Number of Flights: {nof}
                    """)
                    await ctx.edit(content=None,embed=embed)
                    f.close()
            else:
                    embed = discord.Embed(title="Error 404!", description=f"No flights we're found for {user.mention}, make sure they have flights filed!", color=errorc)
                    await ctx.edit(content=None, embed=embed)
        else:
            embed = discord.Embed(title="Error 403!", description="You do not have the <@&1013933799777783849> role. \nGet it in <#965686982304997466> before using this command!", color=errorc)
            await ctx.respond(embed=embed)
        else:
        embed=discord.Embed(title="Error 503!", description="Most ClearFly VA commands are disabled at the moment, read <#1013934267966967848> for more information.", color=errorc)
        await ctx.respond(embed=embed)

            @va.command(name="overview", description="Get an overview over all flights in the va.")
                async def overview(ctx):
                embed=discord.Embed(title="Error 503!", description="Most ClearFly VA commands are disabled at the moment, read <#1013934267966967848> for more information.", color=errorc)
                await ctx.respond(embed=embed)

            @va.command(name="liveries", description="Looking to fly for the ClearFly VA? Here are the liveries to get you started!")
            async def valivs(ctx):
                embed=discord.Embed(title="ClearFly VA Official Liveries:", description="[Boeing 737-800 by Zibo](https://drive.google.com/drive/u/1/folders/1DEzn_jPgyME-U1FrUs3eX4QTwsgwbfpD)\n[Airbus A300-600 by IniSimulations](https://drive.google.com/drive/u/1/folders/16n0cnwkTeGWBhUQJZhXtNz4oq4n4Pe86)\n[Boeing 737-200 by FlyJSim](https://drive.google.com/drive/u/1/folders/1g-vZsECHyHQMbjwnasxHwj0TXjxfLQ0P)", color=cfc)
                await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(VAcommands(bot))