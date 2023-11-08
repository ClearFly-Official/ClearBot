import asyncio
import datetime
import io
import json
import math
import sqlite3
import textwrap
from typing import List, Literal
import aiohttp
import discord
import aiosqlite
import os
import random
import plotly.graph_objects as go
from io import BytesIO
import time
from discord.ext import commands, tasks
from discord.ext.pages import Paginator, Page
import pymongo
from main import ClearBot, UserVABanned
from airports import airports, airports_icao
from PIL import Image, ImageFont
from pilmoji import Pilmoji


async def get_users(get_type: Literal["id", "full"] = "id"):
    out = []
    async with aiosqlite.connect("va.db") as db:
        cur = await db.execute("SELECT * FROM users")
        out = await cur.fetchall()
    if (get_type == "full") or (get_type is None):
        return out
    elif get_type == "id":
        return [usr[1] for usr in out]
    else:
        raise ValueError(f"Didn't found get_type '{get_type}'")


def is_banned_check():
    def predicate(ctx: discord.ApplicationContext):
        if isinstance(ctx.author, discord.Member):
            db = sqlite3.connect("va.db")
            cur = db.execute(
                "SELECT is_ban FROM users WHERE user_id=?", (str(ctx.author.id),)
            )
            is_ban = cur.fetchone()

            if (is_ban == ()) or (is_ban is None):
                status = False
            elif is_ban[0] == 1:
                status = True
            else:
                status = False
        else:
            status = False

        if not status:
            raise UserVABanned()
        else:
            return True

    return commands.check(predicate)  # type: ignore


async def get_airports(ctx: discord.AutocompleteContext):
    if ctx.value == "":
        return ["Start typing the name of an airport for results to appear(e.g. KJFK)"]
    return [airport for airport in airports if airport.startswith(ctx.value.upper())]


async def get_aircraft(ctx: discord.AutocompleteContext):
    async with aiosqlite.connect("va.db") as db:
        cur = await db.execute("SELECT icao FROM aircraft")
        aircraft = await cur.fetchall()
        aircraft = [aircraft[0] for aircraft in aircraft]

    return [craft for craft in aircraft if craft.startswith(ctx.value.upper())]


async def has_flights(user: discord.User | discord.Member):
    async with aiosqlite.connect("va.db") as db:
        cur = await db.execute(
            "SELECT id FROM flights WHERE user_id=?", (str(user.id),)
        )
        flights = await cur.fetchall()

    if (flights == []) or (flights is None):
        return False
    else:
        return True


async def generate_flight_number(
    aircraft_icao, origin_icao, destination_icao, prefix="CF"
):
    async with aiosqlite.connect("va.db") as db:
        cur = await db.execute("SELECT icao FROM aircraft")
        aircraft = await cur.fetchall()
        aircraft = [aircraft[0] for aircraft in aircraft]
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

    org_num = 0
    for l in list(origin_icao):
        org_num = org_num + list(abc).index(l)

    des_num = 0
    for l in list(destination_icao):
        des_num = des_num + list(abc).index(l)

    if len(str(aircraft.index(aircraft_icao))) > 2:
        ac_incode = str(aircraft.index(aircraft_icao))[:2]
        org_num += 1
        des_num += 1
    else:
        ac_incode = aircraft.index(aircraft_icao)

    flight_number = prefix + str(ac_incode) + str(org_num) + str(des_num)

    return flight_number


async def get_aircraft_from_type(aircraft_type: str = "All", output_type: str = "list"):
    aircraft_types = ["Airliner", "GA", "All"]
    if aircraft_type not in aircraft_types:
        aircraft_type = "All"
    async with aiosqlite.connect("va.db") as db:
        if aircraft_type != "All":
            cur = await db.execute(
                "SELECT * FROM aircraft WHERE type=?",
                (aircraft_type,),
            )
            aircraft = await cur.fetchall()
        else:
            cur = await db.execute("SELECT * FROM aircraft")
            aircraft = await cur.fetchall()
    if output_type == "list":
        aircraft = [ac[1] for ac in aircraft]
    elif output_type == "IN_SQL":
        aircraft = "(" + ", ".join([f"'{ac[1]}'" for ac in aircraft]) + ")"

    return aircraft


def get_flights_from_user(user: discord.Member | discord.User) -> list[tuple]:
    db = sqlite3.connect("va.db")
    cur = db.execute("SELECT * FROM flights WHERE user_id=?", (str(user.id),))
    flights = cur.fetchall()
    return flights


def calculate_distance(
    loc1: tuple[float, float], loc2: tuple[float, float], unit: str = "NM"
) -> float:
    lat1 = math.radians(loc1[0])
    lon1 = math.radians(loc1[1])
    lat2 = math.radians(loc2[0])
    lon2 = math.radians(loc2[1])

    radius_values = {
        "NM": 3634.4492440605,
        "KM": 6371.0,
        "MI": 3958.7558657441,
        "FT": 20902230.97,
        "YD": 6974076.11549,
    }

    radius = radius_values.get(unit.upper())
    if radius is None:
        raise ValueError("Invalid unit")

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance


def calculate_time(
    origin_coords: tuple[float, float],
    dest_coords: tuple[float, float],
    speed: float | int,
) -> float:
    return calculate_distance(origin_coords, dest_coords) / speed


class VAStartView(discord.ui.View):
    def __init__(self, bot: ClearBot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Start", style=discord.ButtonStyle.green, custom_id="VA:start_button"
    )
    async def start_button_callback(
        self, button: discord.Button, interaction: discord.Interaction
    ):
        user_ids = await get_users("id")
        if not interaction.user or isinstance(interaction.user, discord.User):
            return
        if str(interaction.user.id) in list(user_ids):
            embed = discord.Embed(
                title="You're already part of the VA!",
                colour=self.bot.color(1),
                description="Joining the VA when you're already in it, is not possible. Flying two aircraft in different parts of the world at the same time is impossible after all.",
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            guild = self.bot.get_guild(self.bot.server_id)
            if guild:
                role = guild.get_role(self.bot.roles.get("clearfly-pilot", 0))
                if role:
                    await interaction.user.add_roles(role)
            fbo = self.bot.get_channel(self.bot.channels.get("fbo", 0))
            if not isinstance(fbo, discord.TextChannel):
                return

            embed = discord.Embed(
                title="Thanks for joining our VA!",
                colour=self.bot.color(),
                description=f"""
Head over to {fbo.mention} to file your first flight!
*Don't know how to file your first flight? Check the message above!*

**NOTE**: *If you don't file a flight within 24 hours you will be kicked from the VA*""",
            )
            user = {
                "user_id": str(interaction.user.id),
                "sign_time": round(time.time()),
                "is_trial": True,
                "is_ban": False,
            }
            async with aiosqlite.connect("va.db") as db:
                await db.execute(
                    "INSERT INTO users (user_id, sign_time, is_trial, is_ban) VALUES (:user_id, :sign_time, :is_trial, :is_ban)",
                    user,
                )
                await db.commit()
            await interaction.response.send_message(embed=embed, ephemeral=True)


class VAReportModal(discord.ui.Modal):
    def __init__(self, bot: ClearBot, title: str):
        self.bot = bot
        super().__init__(title=title)
        self.add_item(
            discord.ui.InputText(
                label="Title",
                placeholder="Engine 2 failed on approach",
                min_length=7,
                style=discord.InputTextStyle.short,
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Content",
                placeholder="Engine 2 failed at FL050 on approach to RWY03L",
                min_length=40,
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user:
            return

        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute(
                "SELECT id FROM flights WHERE user_id=?", (str(interaction.user.id),)
            )
            flights = await cur.fetchall()

            report = {
                "user_id": str(interaction.user.id),
                "flight_id": flights[-1][0],  # type: ignore
                "time": round(time.time()),
                "title": self.children[0].value,
                "content": self.children[1].value,
            }

            await db.execute(
                "INSERT INTO reports (user_id, flight_id, time, title, content) VALUES (:user_id, :flight_id, :time, :title, :content)",
                report,
            )
            await db.execute(
                "UPDATE flights SET incident=' **__INCIDENT__**' WHERE id=?",
                (flights[-1][0],),  # type: ignore
            )
            await db.commit()
            embed = discord.Embed(
                title="Successfully reported incident!",
                description="You may view it with </va user view_report:1016059999056826479>.\n**Don't forget to complete your flight, otherwise it will be __deleted__!**",
                colour=self.bot.color(),
            )
            await interaction.response.send_message(embed=embed)


class VACommands(discord.Cog):
    def __init__(self, bot: ClearBot):
        self.bot = bot

        self.client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.client["ClearFly"]
        self.col = self.db["SAReportUsers"]

    va = discord.SlashCommandGroup(
        name="va", description="🛬 All commands related to the ClearFly Virtual Airline."
    )

    vadmin = va.create_subgroup(
        name="admin", description="🔒 All commands for ClearFly's VAdmins."
    )

    flight = va.create_subgroup(
        name="flight",
        description="⚙️ All commands to manage your own flights in the VA.",
    )

    user = va.create_subgroup(
        name="user", description="⚙️ All commands to view public user data in the VA."
    )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(VAStartView(self.bot))
        if not self.trial_check.is_running():
            self.trial_check.start()
        if not self.completed_flight_check.is_running():
            self.completed_flight_check.start()
        print("\033[34m|\033[0m \033[96;1mVA\033[0;36m cog loaded sucessfully\033[0m")

    @commands.Cog.listener("on_message")
    async def auto_complete_flight(self, message: discord.Message):
        if message.channel.id != self.bot.channels.get("fbo"):
            return
        if message.author.id != self.bot.bot_id and len(message.embeds) != 0:
            embed = message.embeds[0]

            lines = str(embed.description).split("\n")

            title = (
                lines[0]
                .replace("### <@", "")
                .replace(">", "")
                .replace("!", "")
                .split(" ")
            )
            data = (title[0], title[3], title[6])

            async with aiosqlite.connect("va.db") as db:
                cur = await db.execute(
                    "SELECT id FROM flights WHERE user_id=? AND is_completed=0 AND destination=? AND aircraft=?",
                    data,
                )
                flight_ids = await cur.fetchall()
                cur2 = await db.execute(
                    "SELECT * FROM flights WHERE user_id=? AND is_completed=0 AND destination=? AND aircraft=?",
                    data,
                )
                flight_id2 = await cur2.fetchall()

                if flight_ids == []:
                    embed = discord.Embed(
                        title="I couldn't find any non-completed flights",
                        colour=self.bot.color(2),
                        description="""
- You may have marked your flight as completed before landing (which you shouldn't do).
- You were not flying for the VA, but still had it enabled. To disable, go to settings and change the VA name (`ClearFly-Official/StableApproach`) to something else.
- You needed to divert to another airport, use </va flight divert:1016059999056826479> if so. *This warning might appear when landing at the diverted airport even if you ran the command*
""",
                    )
                    await message.reply(f"<@{data[0]}>", embed=embed)
                    return
                else:
                    await db.execute(
                        "UPDATE flights SET is_completed=1 WHERE id=?",
                        (flight_ids[0][0],),  # type: ignore
                    )
                    await db.commit()

                flight_id2 = flight_id2[0]  # type: ignore
                embed = discord.Embed(
                    title="Flight automatically completed!",
                    colour=self.bot.color(),
                    description="I have marked your flight as completed, and it has been permantly logged.",
                ).add_field(
                    name="Flight Details",
                    value=f"""
Flight number: **{flight_id2[2]}**
Aircraft: **{flight_id2[3]}**
Origin: **{flight_id2[4]}**
Destination: **{flight_id2[5]}**
                """,
                )
            await message.reply(embed=embed)

    @tasks.loop(minutes=10)
    async def trial_check(self):
        users = await get_users()
        for user in users:
            if ((round(time.time()) - int(user[2])) > 86_400) and (user[3] == 1):
                try:
                    user_dm = self.bot.get_user(int(user[1]))
                    guild = self.bot.get_guild(self.bot.server_id)
                    if not guild:
                        return
                    user_role = guild.get_member(int(user[1]))
                    role = guild.get_role(self.bot.roles.get("clearfly-pilot", 0))
                    if role and user_role:
                        await user_role.remove_roles(role)
                    if user_dm is not None:
                        user_embed = discord.Embed(
                            title="You have been kicked from the ClearFly VA.",
                            colour=self.bot.color(),
                            description=f"""
Hi there {user_dm.name},

We noticed that you did not file a flight within 24 hours of signing up for the ClearFly VA, and unfortunately we had to remove you from the VA. 
However, if you're still interested in flying with us, we invite you to sign up again and file a flight within the previously mentioned time frame. 
We'd love to have you back as a member of our Virtual Airline!

Best regards,
The ClearFly Team
                            """,
                        )
                        await user_dm.send(embed=user_embed)
                except discord.Forbidden:
                    raise
                async with aiosqlite.connect("va.db") as db:
                    await db.execute("DELETE FROM users WHERE user_id=?", (user[1],))
                    await db.commit()

    @tasks.loop(minutes=10)
    async def completed_flight_check(self):
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute("SELECT * FROM flights WHERE is_completed=0")
            flights = await cur.fetchall()

            for flight in flights:
                if (round(time.time() - int(flight[6])) >= 82_800) and (
                    round(time.time() - int(flight[6])) <= 83_400
                ):
                    user = self.bot.get_user(int(flight[1]))
                    if not user:
                        return
                    fbo = self.bot.sendable_channel(
                        self.bot.get_channel(self.bot.channels.get("fbo", 0))
                    )
                    embed = discord.Embed(
                        title=f"Your last filed flight will be cancelled <t:{int(flight[6])+86_400}:R>.",
                        colour=self.bot.color(2),
                        description=f"""
Hey {user.name}! 

We have noticed that you have not completed your last flight yet. Please remember to mark your flight as completed with the command </va flight complete:1016059999056826479>.
Your flight will be cancelled if you fail to do so <t:{int(flight[6])+86_400}:R>. 

**THIS IS YOUR __LAST__ REMINDER**
                                """,
                    )
                    if fbo:
                        await fbo.send(user.mention, embed=embed)

                if (round(time.time() - int(int(flight[6]))) >= 64_800) and (
                    round(time.time() - int(flight[6])) <= 65_400
                ):
                    user = self.bot.get_user(int(flight[1]))
                    if not user:
                        return
                    fbo = self.bot.sendable_channel(
                        self.bot.get_channel(self.bot.channels.get("fbo", 0))
                    )
                    embed = discord.Embed(
                        title=f"Your last filed flight will be cancelled <t:{int(flight[6])+86_400}:R>.",
                        colour=self.bot.color(2),
                        description=f"""
Hey {user.name}! 

We have noticed that you have not completed your last flight yet. Please remember to mark your flight as completed with the command </va flight complete:1016059999056826479>.
Your flight will be cancelled if you fail to do so <t:{int(flight[6])+86_400}:R>. You will be reminded one last time before it's too late <t:{int(flight[6])+82_800}:R>
                                """,
                    )
                    if fbo:
                        await fbo.send(user.mention, embed=embed)

                if (round(time.time() - int(flight[6])) >= 43_200) and (
                    round(time.time() - int(flight[6])) <= 43_800
                ):
                    user = self.bot.get_user(int(flight[1]))
                    if not user:
                        return
                    fbo = self.bot.sendable_channel(
                        self.bot.get_channel(self.bot.channels.get("fbo", 0))
                    )
                    embed = discord.Embed(
                        title=f"Your last filed flight will be cancelled <t:{int(flight[6])+86_400}:R>.",
                        colour=self.bot.color(2),
                        description=f"""
Hey {user.name}! 

We have noticed that you have not completed your last flight yet. Please remember to mark your flight as completed with the command </va flight complete:1016059999056826479>.
Your flight will be cancelled if you fail to do so <t:{int(flight[6])+86_400}:R>. Another reminder will be sent <t:{int(flight[6])+64_800}:R> if you haven't completed it yet.
                                """,
                    )
                    if fbo:
                        await fbo.send(user.mention, embed=embed)

                if (round(time.time()) - int(flight[6])) > 86_400:
                    await db.execute("DELETE FROM flights WHERE id=?", (flight[0],))
                    await db.execute(
                        "DELETE FROM reports WHERE flight_id=?", (flight[0],)
                    )
                    user = self.bot.get_user(int(flight[1]))
                    if not user:
                        return
                    fbo = self.bot.sendable_channel(
                        self.bot.get_channel(self.bot.channels.get("fbo", 0))
                    )
                    embed = discord.Embed(
                        title="Your last filed flight has been cancelled.",
                        colour=self.bot.color(2),
                        description=f"""
Hi there {user.name},

Around <t:{int(flight[6])}:R> you filed a flight, but never marked it as completed. To prevent people filing a flight, but never actually completing it, we automatically cancel it after 24 hours. 
This sadly happened to your last flight. Please remember to mark your flight as completed next time!
                                """,
                    )
                    if fbo:
                        await fbo.send(user.mention, embed=embed)

            await db.commit()

    @flight.command(name="file", description="🗳️ File a flight for the ClearFly VA.")
    @discord.option(
        name="aircraft",
        description="The aircraft you want to fly with, ICAO code please (e.g. B738).",
        autocomplete=get_aircraft,
    )
    @discord.option(
        name="origin",
        description="The airport you want to fly from, in ICAO format (e.g. KJFK).",
        autocomplete=get_airports,
    )
    @discord.option(
        name="destination",
        description="The airport you want to fly to, in ICAO format (e.g. EBBR).",
        autocomplete=get_airports,
    )
    @commands.has_role(1013933799777783849)
    @commands.cooldown(1, 30, commands.BucketType.user)
    @is_banned_check()
    async def va_file(
        self,
        ctx: discord.ApplicationContext,
        aircraft: str,
        origin: str,
        destination: str,
    ):
        await ctx.defer()

        usrs = await get_users("id")
        if str(ctx.author.id) not in list(usrs):
            overv_channel = self.bot.get_channel(
                self.bot.channels.get("va-overview", 0)
            )
            if isinstance(overv_channel, discord.TextChannel):
                embed = discord.Embed(
                    title="You're not part of the VA!",
                    colour=self.bot.color(1),
                    description=f"Feel free to sign up at any time in {overv_channel.mention}",
                )
                await ctx.respond(embed=embed)
                return

        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute("SELECT icao FROM aircraft")
            ac_list = await cur.fetchall()
            ac_list = [craft[0] for craft in ac_list]

        if aircraft not in ac_list:
            embed = discord.Embed(
                title="Invalid aircraft",
                colour=self.bot.color(1),
                description="Please provide a valid aircraft ICAO code (e.g. B738).",
            )
            await ctx.respond(embed=embed)
            return

        if (origin[:4].upper()) not in airports_icao:
            embed = discord.Embed(
                title="Invalid origin",
                colour=self.bot.color(1),
                description="Please provide a valid airport ICAO code (e.g. KJFK).",
            )
            await ctx.respond(embed=embed)
            return
        if (destination[:4].upper()) not in airports_icao:
            embed = discord.Embed(
                title="Invalid destination",
                colour=self.bot.color(1),
                description="Please provide a valid airport ICAO code (e.g. KJFK).",
            )
            await ctx.respond(embed=embed)
            return
        hdr = {"X-API-Key": os.getenv("CWX_KEY")}
        timeout = aiohttp.ClientTimeout(total=10)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as cs:
                async with cs.get(
                    f"https://api.checkwx.com/metar/{origin[:4].upper()}",
                    headers=hdr,
                ) as r:
                    resp = await r.json()
        except:
            resp = {"results": []}

        flight_num = await generate_flight_number(
            aircraft, origin[:4].upper(), destination[:4].upper()
        )
        embed = discord.Embed(
            title="Flight filed successfully!",
            colour=self.bot.color(),
            description=f"Flight will automatically be removed if not marked as completed <t:{round(time.time())+86_400}:R>.",
        )
        embed.set_author(
            name=f"Filed by {ctx.author.name}", icon_url=ctx.author.display_avatar.url
        )
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute(
                "SELECT is_trial FROM users WHERE user_id=?", (str(ctx.author.id),)
            )
            cur2 = await db.execute(
                "SELECT is_completed FROM flights WHERE user_id=?",
                (str(ctx.author.id),),
            )
            is_trial = await cur.fetchone()
            if not is_trial:
                raise Exception(
                    "Failed to check wether you are a first time user or not."
                )
            is_completed = await cur2.fetchall()
            if is_trial[0] == 1:
                embed.set_footer(
                    text="You have filed a flight within 24 hours from sign up, so you're now officially a member of the VA. Congratulations!"
                )
                await db.execute(
                    "UPDATE users SET is_trial=0 WHERE user_id=?", (str(ctx.author.id),)
                )
                await db.commit()
            if not is_completed == []:
                if is_completed[-1][0] == 0:  # type: ignore
                    embed = discord.Embed(
                        title="You haven't completed your last flight!",
                        colour=self.bot.color(1),
                        description="The last flight you filed hasn't been marked as completed, thus you can't file a new one.",
                    )
                    await ctx.respond(embed=embed)
                    return
        card_id = "flight_card" + str(random.randint(0, 9)) + ".png"
        img = Image.open(f"images/va_card/{self.bot.theme}/va_flightcard_blank.png")
        font = ImageFont.truetype("fonts/Inter-Regular.ttf", size=48)
        route_font = ImageFont.truetype("fonts/Inter-Regular.ttf", size=128)
        metar_font = ImageFont.truetype("fonts/Inter-Regular.ttf", size=36)

        data = ""
        if not resp["results"]:
            data = "No METAR data found."
        else:
            data = str(
                resp.get(
                    "data",
                    [
                        "N/A",
                    ],
                )[0]
            )

        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute("SELECT * FROM aircraft WHERE icao=?", (aircraft,))
            aircraft_data = await cur.fetchone()
            if not aircraft_data:
                raise Exception("Couldn't fetch aircraft data.")

        with open("airports.json", "r") as f:
            airport_data = json.load(f)

        with Pilmoji(img) as pilmoji:
            colour = (255, 255, 255)
            x_padding = 40
            date = str(datetime.datetime.utcnow().date()).split("-")
            minute = (
                f"{datetime.datetime.utcnow().minute}"
                if datetime.datetime.utcnow().minute > 9
                else f"{datetime.datetime.utcnow().minute}0"
            )
            date.reverse()
            time_str = (
                f"{datetime.datetime.utcnow().hour}:{minute} UTC | {'/'.join(date)}"
            )
            flight_time = str(
                datetime.timedelta(
                    hours=calculate_time(
                        (
                            airport_data.get(origin[:4].upper()).get("lat", 0),
                            airport_data.get(origin[:4].upper()).get("lon", 0),
                        ),
                        (
                            airport_data.get(destination[:4].upper()).get("lat", 0),
                            airport_data.get(destination[:4].upper()).get("lon", 0),
                        ),
                        aircraft_data[4],
                    )
                )
            ).split(":")

            flight_time = f"{flight_time[0]}:{flight_time[1]}"

            pilmoji.text(
                (img.size[0] - (font.getlength(time_str) + x_padding), 43),  # type: ignore
                time_str,
                font=font,
                fill=colour,
            )
            pilmoji.text(
                (x_padding, 43),
                flight_num,
                font=font,
                fill=colour,
            )
            pilmoji.text(
                (x_padding + 10, 145), origin[:4].upper(), font=route_font, fill=colour
            )
            pilmoji.text(
                (
                    (
                        img.size[0]
                        - (
                            route_font.getlength(destination[:4].upper())
                            + (x_padding + 10)
                        )
                    ),  # type: ignore
                    145,
                ),
                destination[:4].upper(),
                font=route_font,
                fill=colour,
            )
            pilmoji.text(
                (170, 415),
                textwrap.fill(ctx.author.name, 10, max_lines=1),
                font=font,
                fill=colour,
            )
            pilmoji.text(
                (720, 415),
                aircraft,
                font=font,
                fill=colour,
            )
            pilmoji.text(
                (170, 357),
                flight_time,
                font=font,
                fill=colour,
            )
            pilmoji.text(
                (720, 357),
                str(
                    round(
                        calculate_distance(
                            (
                                airport_data.get(origin[:4].upper()).get("lat", 0),
                                airport_data.get(origin[:4].upper()).get("lon", 0),
                            ),
                            (
                                airport_data.get(destination[:4].upper()).get("lat", 0),
                                airport_data.get(destination[:4].upper()).get("lon", 0),
                            ),
                        )
                    )
                )
                + " NM",
                font=font,
                fill=colour,
            )
            pilmoji.text(
                (x_padding + 5, 525 + x_padding / 2),  # type: ignore
                textwrap.fill(data, 46, max_lines=3),
                font=metar_font,
                fill=colour,
            )

        with io.BytesIO() as output:
            img.save(output, format="PNG")
            output.seek(0)
            file = discord.File(output, filename=card_id)
        embed.set_image(url=f"attachment://{card_id}")

        flight = {
            "user_id": str(ctx.author.id),
            "flight_number": flight_num,
            "aircraft": aircraft,
            "origin": origin[:4].upper(),
            "destination": destination[:4].upper(),
            "filed_at": round(time.time()),
            "is_completed": False,
            "divert": "",
            "incident": "",
        }

        async with aiosqlite.connect("va.db") as db:
            await db.execute(
                "INSERT INTO flights (user_id, flight_number, aircraft, origin, destination, filed_at, is_completed, divert, incident) VALUES (:user_id, :flight_number, :aircraft, :origin, :destination, :filed_at, :is_completed, :divert, :incident)",
                flight,
            )
            await db.commit()

        await ctx.respond(embed=embed, file=file)

    @flight.command(
        name="complete", description="✅ Mark your last flight as completed."
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.has_role(1013933799777783849)
    @is_banned_check()
    async def va_complete(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute(
                "SELECT id FROM flights WHERE user_id=? AND is_completed=0",
                (str(ctx.author.id),),
            )
            flight_ids = await cur.fetchall()
            cur2 = await db.execute(
                "SELECT * FROM flights WHERE user_id=? AND is_completed=0",
                (str(ctx.author.id),),
            )
            flight_id2 = await cur2.fetchall()

            if flight_ids == []:
                embed = discord.Embed(
                    title="You do not have any non-completed flights!",
                    colour=self.bot.color(1),
                    description="I did not find any flights filed by you that are not marked as completed.",
                )
                await ctx.respond(embed=embed)
                return
            else:
                await db.execute(
                    "UPDATE flights SET is_completed=1 WHERE id=?", (flight_ids[0][0],)  # type: ignore
                )
                await db.commit()

            flight_id2 = flight_id2[0]  # type: ignore
            embed = discord.Embed(
                title="Flight completed!",
                colour=self.bot.color(),
                description="You have marked your flight as completed, and it has been permantly logged.",
            ).add_field(
                name="Flight Details",
                value=f"""
Flight number: **{flight_id2[2]}**
Aircraft: **{flight_id2[3]}**
Origin: **{flight_id2[4]}**
Destination: **{flight_id2[5]}**
            """,
            )
        await ctx.respond(embed=embed)

    @flight.command(name="cancel", description="❌ Cancel your last flight.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_role(1013933799777783849)
    @is_banned_check()
    async def va_cancel(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute(
                "SELECT * FROM flights WHERE user_id=?", (str(ctx.author.id),)
            )
            flights = await cur.fetchall()

            if flights == []:
                embed = discord.Embed(
                    title="No flights found!", colour=self.bot.color(1)
                )
                await ctx.respond(embed=embed)
                return
            last_flight = flights[-1]  # type: ignore

            if last_flight[7]:
                embed = discord.Embed(
                    title="You completed your last flight!",
                    description="I can't cancel a flight you have done already!",
                    colour=self.bot.color(1),
                )
                await ctx.respond(embed=embed)
            else:
                await db.execute("DELETE FROM flights WHERE id=?", (last_flight[0],))
                await db.execute(
                    "DELETE FROM reports WHERE flight_id=?", (last_flight[0],)
                )
                await db.commit()
                embed = discord.Embed(
                    title="Flight successfully cancelled!", colour=self.bot.color()
                )
                await ctx.respond(embed=embed)

    @flight.command(
        name="divert", description="🔀 Divert your last flight to another airport."
    )
    @discord.option(
        name="airport",
        description="The airport you're diverting too.",
        autocomplete=get_airports,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_role(1013933799777783849)
    @is_banned_check()
    async def va_divert(self, ctx: discord.ApplicationContext, airport):
        await ctx.defer()

        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute(
                "SELECT * FROM flights WHERE user_id=?", (str(ctx.author.id),)
            )
            flights = await cur.fetchall()

            if flights == []:
                embed = discord.Embed(
                    title="No flights found!", colour=self.bot.color(1)
                )
                await ctx.respond(embed=embed)
                return
            last_flight = flights[-1]  # type: ignore

            if last_flight[7]:
                embed = discord.Embed(
                    title="You completed your last flight!",
                    description="I can't edit a flight you have completed already!",
                    colour=self.bot.color(1),
                )
                await ctx.respond(embed=embed)
            else:
                await db.execute(
                    "UPDATE flights SET divert=? WHERE id=?",
                    (f" __*diverted to **{airport[:4].upper()}***__", last_flight[0]),
                )
                await db.commit()
                embed = discord.Embed(
                    title=f"Flight successfully diverted to `{airport[:4].upper()}`!",
                    colour=self.bot.color(),
                )
                await ctx.respond(embed=embed)

    @flight.command(
        name="report",
        description="📝 Report an incident that happend on your last flight.",
    )
    @commands.has_role(1013933799777783849)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @is_banned_check()
    async def va_report(self, ctx: discord.ApplicationContext):
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute(
                "SELECT * FROM flights WHERE user_id=?", (str(ctx.author.id),)
            )
            flights = await cur.fetchall()

            if flights == []:
                embed = discord.Embed(
                    title="No flights found!", colour=self.bot.color(1)
                )
                await ctx.respond(embed=embed)
                return
            last_flight = flights[-1]  # type: ignore

            if last_flight[7]:
                embed = discord.Embed(
                    title="You completed your last flight!",
                    description="I can't edit a flight you have completed already!",
                    colour=self.bot.color(1),
                )
                await ctx.respond(embed=embed)
            else:
                await ctx.send_modal(
                    VAReportModal(self.bot, title="Report an incident")
                )

    @user.command(name="view_report", description="📄 View a users reports.")
    @discord.option(
        name="user",
        description="The user you want to see the flights of.",
        required=False,
    )
    @commands.has_role(1013933799777783849)
    @is_banned_check()
    async def va_view_report(
        self, ctx: discord.ApplicationContext, user: discord.Member | discord.User
    ):
        await ctx.defer()

        if not user:
            user = ctx.author

        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute(
                "SELECT * FROM reports WHERE user_id=?", (str(user.id),)
            )
            reports = await cur.fetchall()
            if reports == []:
                embed = discord.Embed(
                    title="No reports found", colour=self.bot.color(1)
                )
                await ctx.respond(embed=embed)
                return
            reports.reverse()  # type: ignore

        pages = [
            Page(
                embeds=[
                    discord.Embed(
                        title=f"{user.name}'s reports",
                        description=f"""
**<t:{report[3]}:F>: {report[4]}**
{report[5]}
                        """,
                        colour=self.bot.color(),
                    ).set_footer(
                        text=f"Total of {len(reports)} reports"  # type: ignore
                    )
                ]
            )
            for report in reports
        ]
        paginator = Paginator(pages)
        await paginator.respond(ctx.interaction)

    @user.command(name="flights", description="🛬 View a users flights.")
    @discord.option(
        name="user",
        description="The user you want to see the flights of.",
        required=False,
    )
    @commands.has_role(1013933799777783849)
    @is_banned_check()
    async def va_flights(
        self, ctx: discord.ApplicationContext, user: discord.Member | discord.User
    ):
        await ctx.defer()

        if user is None:
            user = ctx.author

        if not await has_flights(user):
            embed = discord.Embed(
                title="No flights found",
                description="This user has no flights filed.",
                colour=self.bot.color(1),
            )
            await ctx.respond(embed=embed)
            return

        with open("airports.json", "r") as file:
            airports_data = json.load(file)

        flights = []
        async with aiosqlite.connect("va.db") as db:
            cursor = await db.execute(
                "SELECT * FROM flights WHERE user_id=?", (str(user.id),)
            )
            rows = await cursor.fetchall()
            flights = [
                f"**{i}**: **{row[2]}**, **{row[3]}**, **{row[4]}** -> **{row[5]}**{row[8]} (**{round(calculate_distance((airports_data.get(row[4])['lat'], airports_data.get(row[4])['lon']),(airports_data.get(row[5])['lat'], airports_data.get(row[5])['lon'])))}**nm), *filed <t:{row[6]}:f>*{row[9]}"
                for i, row in enumerate(rows, 1)
            ]

        chunks = [flights[i : i + 10] for i in range(0, len(flights), 10)]

        pages = [
            Page(
                embeds=[
                    discord.Embed(
                        title=f"Flights {i+1}-{i+len(chunk)}",
                        description="\n".join(chunk),
                        colour=self.bot.color(),
                    ).set_footer(
                        text=f"Showing 10/page, total of {len(flights)} flights"
                    )
                ]
            )
            for i, chunk in enumerate(chunks)
        ]
        paginator = Paginator(pages)
        await paginator.respond(ctx.interaction)

    @user.command(name="map", description="🌍 View a user's flights in map style.")
    @commands.has_role(1013933799777783849)
    @discord.option(
        name="user",
        description="The user you want to see the flights of.",
        required=False,
    )
    @discord.option(
        name="version",
        description="The map version you want to use.",
        choices=["General Aviation", "Airliner", "All"],
    )
    @discord.option(
        name="auto_zoom", description="Zoom automatically to fit the flights."
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @is_banned_check()
    async def va_flight_map(
        self,
        ctx: discord.ApplicationContext,
        user: discord.Member | discord.User,
        version: str = "All",
        auto_zoom: bool = True,
    ):
        await ctx.defer()

        if not user:
            user = ctx.author

        if not await has_flights(user):
            embed = discord.Embed(
                title="No flights found",
                description="This user has no flights filed.",
                colour=self.bot.color(1),
            )
            await ctx.respond(embed=embed)
            return

        async with aiosqlite.connect("va.db") as db:
            if version == "General Aviation":
                cursor = await db.execute(
                    f"SELECT origin, destination FROM flights WHERE user_id=? AND aircraft IN {await get_aircraft_from_type('GA', 'IN_SQL')}",
                    (str(user.id),),
                )
            elif version == "Airliner":
                cursor = await db.execute(
                    f"SELECT origin, destination FROM flights WHERE user_id=? AND aircraft IN {await get_aircraft_from_type('Airliner', 'IN_SQL')}",
                    (str(user.id),),
                )
            else:
                cursor = await db.execute(
                    "SELECT origin, destination FROM flights WHERE user_id=?",
                    (str(user.id),),
                )
            waypoints_data = await cursor.fetchall()

        with open("airports.json", "r") as file:
            airports_data = json.load(file)

        waypoints = []

        for origin, destination in waypoints_data:
            origin_data = airports_data.get(origin)
            dest_data = airports_data.get(destination)

            if origin_data and dest_data:
                origin_coords = (origin_data["lat"], origin_data["lon"])
                dest_coords = (dest_data["lat"], dest_data["lon"])
                waypoints.append((origin_coords, dest_coords))

        fig = go.Figure()

        for waypoint in waypoints:
            fig.add_trace(
                go.Scattergeo(
                    lat=[wayp[0] for wayp in waypoint],
                    lon=[wayp[1] for wayp in waypoint],
                    mode="lines",
                    line=dict(color="#6db2d9", width=2),
                )
            )

            for coords in waypoint:
                fig.add_trace(
                    go.Scattergeo(
                        lat=[coords[0]],
                        lon=[coords[1]],
                        mode="markers",
                        marker=dict(
                            symbol="circle",
                            color="#ffffff",
                            size=5,
                            line=dict(color="#6db2d9", width=1),
                        ),
                    )
                )

        if auto_zoom:
            fig.update_geos(
                resolution=50,
                projection_type="natural earth",
                showland=True,
                landcolor="#093961",
                showocean=True,
                oceancolor="#142533",
                showrivers=True,
                rivercolor="#142533",
                showcountries=True,
                countrycolor="#2681b4",
                showlakes=True,
                lakecolor="#142533",
                showframe=False,
                coastlinecolor="#2681b4",
                fitbounds="locations",
            )
        else:
            fig.update_geos(
                resolution=50,
                projection_type="equirectangular",
                showland=True,
                landcolor="#093961",
                showocean=True,
                oceancolor="#142533",
                showrivers=True,
                rivercolor="#142533",
                showcountries=True,
                countrycolor="#2681b4",
                showlakes=True,
                lakecolor="#142533",
                showframe=False,
                coastlinecolor="#2681b4",
            )
        fig.update_layout(showlegend=False)

        if auto_zoom:
            image_bytes = fig.to_image(format="png", width=2048, height=2048)
        else:
            image_bytes = fig.to_image(format="png", width=2048, height=2048)

        image = Image.open(BytesIO(image_bytes))

        grayscale_image = image.convert("L")

        left, upper, right, lower = image.size[0], image.size[1], 0, 0
        pixels = grayscale_image.load()

        for x in range(image.size[0]):
            for y in range(image.size[1]):
                if pixels[x, y] < 255:
                    left = min(left, x)
                    upper = min(upper, y)
                    right = max(right, x)
                    lower = max(lower, y)

        cropped_image = image.crop((left, upper + 1, right, lower))

        if version == "Airliner":
            flight_type = "airliner"
        elif version == "General Aviation":
            flight_type = "GA"
        else:
            flight_type = ""

        with io.BytesIO() as output:
            output_filename = "map.png"
            cropped_image.save(output, format="PNG")
            output.seek(0)
            map_file = discord.File(output, filename=output_filename)
            embed = discord.Embed(
                title=f"{user.name}'s flight map",
                description=f"{user.mention} has completed **{len(waypoints_data)}** {flight_type} flight(s)!",  # type: ignore
                colour=self.bot.color(),
            ).set_image(url=f"attachment://{output_filename}")
            if auto_zoom:
                embed.set_footer(
                    text="Can't figure out where this is on the map? Try running the command with auto_zoom disabled."
                )
            await ctx.respond(embed=embed, file=map_file)

        await asyncio.sleep(20)

    @user.command(name="flight", description="🗺️ View a user's flights in map style.")
    @commands.has_role(1013933799777783849)
    @discord.option(
        name="user",
        description="The user you want to see the flight of.",
        required=False,
    )
    @discord.option(
        name="auto_zoom", description="Zoom automatically to fit the flight."
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @is_banned_check()
    async def va_flight(
        self,
        ctx: discord.ApplicationContext,
        user: discord.Member | discord.User,
        auto_zoom: bool = True,
    ):
        await ctx.defer()

        if not user:
            user = ctx.author

        if not await has_flights(user):
            embed = discord.Embed(
                title="No flights found",
                description="This user has no flights filed.",
                colour=self.bot.color(1),
            )
            await ctx.respond(embed=embed)
            return

        flight_count = 0
        flights = [[]]
        flight_list_number = 0
        for flight in get_flights_from_user(user):
            if flight_count < 10:
                flights[flight_list_number].append(
                    discord.SelectOption(
                        label=flight[2],
                        value=str(flight[0]),
                        description=f"{flight[4]}-{flight[5]}, {flight[3]}",
                    )
                )
                flight_count += 1
            else:
                flight_count = 0
                flight_list_number += 1
                flights.append(
                    [
                        discord.SelectOption(
                            label=flight[2],
                            value=str(flight[0]),
                            description=f"{flight[4]}-{flight[5]}, {flight[3]}",
                        )
                    ]
                )
                flight_count += 1

        flight_list_number = 0

        def get_flights():
            return flights[flight_list_number]

        def is_disabled():
            if len(flights) > 1:
                return False
            else:
                return True

        class VAFlightSelectView(discord.ui.View):
            def __init__(
                self,
                bot: ClearBot,
                flights: list[list[str]],
                flight_list_number: int,
            ):
                self.flights = flights
                self.flight_list_number = flight_list_number
                self.bot = bot
                super().__init__(timeout=120.0)

            async def on_timeout(self):
                for child in self.children:
                    if isinstance(child, discord.ui.Select) or isinstance(
                        child, discord.ui.Button
                    ):
                        child.disabled = True
                await ctx.edit(view=self)

            @discord.ui.select(
                placeholder="CF12345",
                max_values=1,
                options=get_flights(),
            )
            async def select_callback(
                self, select: discord.ui.Select, interaction: discord.Interaction
            ):
                if not self.bot.is_interaction_owner(interaction, ctx.author.id):
                    await interaction.response.send_message(
                        "Run the command yourself to use it!", ephemeral=True
                    )
                    return
                if not isinstance(select.values[0], str):
                    return

                await interaction.response.defer()
                async with aiosqlite.connect("va.db") as db:
                    cursor = await db.execute(
                        "SELECT * FROM flights WHERE id=?",
                        (int(select.values[0]),),
                    )
                    flight_data = await cursor.fetchone()
                    if not flight_data:
                        return
                    cursor = await db.execute(
                        "SELECT crz_speed, type FROM aircraft WHERE icao=?",
                        (flight_data[3],),
                    )
                    aircraft_data = await cursor.fetchone()
                    if not aircraft_data:
                        raise Exception("No aircraft data available.")

                with open("airports.json", "r") as file:
                    airports_data = json.load(file)

                waypoints = []
                fig = go.Figure()

                origin_data = airports_data.get(flight_data[4])
                dest_data = airports_data.get(flight_data[5])

                if origin_data and dest_data:
                    origin_coords = (origin_data["lat"], origin_data["lon"])
                    dest_coords = (dest_data["lat"], dest_data["lon"])
                    waypoints.append((origin_coords, dest_coords))
                else:
                    raise Exception("No origin/destination data available.")

                for waypoint in waypoints:
                    fig.add_trace(
                        go.Scattergeo(
                            lat=[wayp[0] for wayp in waypoint],
                            lon=[wayp[1] for wayp in waypoint],
                            mode="lines",
                            line=dict(color="#6db2d9", width=2),
                        )
                    )

                    for i, coords in enumerate(waypoint, 4):
                        fig.add_trace(
                            go.Scattergeo(
                                lat=[coords[0]],
                                lon=[coords[1]],
                                mode="markers",
                                marker=dict(
                                    symbol="circle",
                                    color="#ffffff",
                                    size=5,
                                    line=dict(color="#6db2d9", width=5),
                                ),
                            )
                        )
                        fig.add_trace(
                            go.Scattergeo(
                                lat=[coords[0]],
                                lon=[coords[1]],
                                mode="text",
                                text=flight_data[i],
                                textfont=dict(
                                    color="#ffffff",
                                    size=32 if auto_zoom else 12,
                                ),
                                textposition=["top center"],
                                line=dict(color="#6db2d9", width=5),
                            )
                        )

                if auto_zoom:
                    fig.update_geos(
                        resolution=50,
                        projection_type="natural earth",
                        showland=True,
                        landcolor="#093961",
                        showocean=True,
                        oceancolor="#142533",
                        showrivers=True,
                        rivercolor="#142533",
                        showcountries=True,
                        countrycolor="#2681b4",
                        showlakes=True,
                        lakecolor="#142533",
                        showframe=False,
                        coastlinecolor="#2681b4",
                        fitbounds="locations",
                    )
                else:
                    fig.update_geos(
                        resolution=50,
                        projection_type="equirectangular",
                        showland=True,
                        landcolor="#093961",
                        showocean=True,
                        oceancolor="#142533",
                        showrivers=True,
                        rivercolor="#142533",
                        showcountries=True,
                        countrycolor="#2681b4",
                        showlakes=True,
                        lakecolor="#142533",
                        showframe=False,
                        coastlinecolor="#2681b4",
                    )
                fig.update_layout(showlegend=False)

                if auto_zoom:
                    image_bytes = fig.to_image(format="png", width=2048, height=2048)
                else:
                    image_bytes = fig.to_image(format="png", width=2048, height=2048)

                image = Image.open(BytesIO(image_bytes))

                grayscale_image = image.convert("L")

                left, upper, right, lower = image.size[0], image.size[1], 0, 0
                pixels = grayscale_image.load()

                for x in range(image.size[0]):
                    for y in range(image.size[1]):
                        if pixels[x, y] < 255:
                            left = min(left, x)
                            upper = min(upper, y)
                            right = max(right, x)
                            lower = max(lower, y)

                cropped_image = image.crop((left, upper + 1, right, lower))

                if (flight_data[8] == "") or (flight_data[9] == ""):
                    notes = "*No Notes*"
                else:
                    notes = flight_data[8] + "\n" + flight_data[9]

                flight_time = str(
                    datetime.timedelta(
                        hours=calculate_time(
                            origin_coords, dest_coords, aircraft_data[0]
                        )
                    )
                ).split(":")

                flight_time = f"{flight_time[0]}:{flight_time[1]}"

                with io.BytesIO() as output:
                    output_filename = f"flight_{user.id}_{select.values[0]}.png"
                    cropped_image.save(output, format="PNG")
                    output.seek(0)
                    map_file = discord.File(output, filename=output_filename)
                    embed = (
                        discord.Embed(
                            title=f"Flight {flight_data[2]}",
                            description=f"""
Flight number: **{flight_data[2]}**
Aircraft: **{flight_data[3]}**
Origin: **{flight_data[4]}** - **{airports_data.get(flight_data[4]).get('name', 'Unnamed')}**
Destination: **{flight_data[5]}** - **{airports_data.get(flight_data[5]).get('name', 'Unnamed')}**
Distance: **{round(calculate_distance(origin_coords, dest_coords), 1)}** nm, **{round(calculate_distance(origin_coords, dest_coords, unit='KM'), 1)}**km, **{round(calculate_distance(origin_coords, dest_coords, unit='MI'), 1)}** mi
Estimated flight time: **{flight_time}** (with CRZ speed(TAS) {aircraft_data[0]}kts)
Filed at: **<t:{flight_data[6]}:F>**
Notes:
{notes}
                        """,
                            colour=self.bot.color(),
                        )
                        .set_image(url=f"attachment://{output_filename}")
                        .set_author(
                            name=f"Flown by {user.name}",
                            icon_url=user.display_avatar.url,
                        )
                    )
                    if auto_zoom:
                        embed.set_footer(
                            text="Can't figure out where this is on the map? Try running the command with auto_zoom disabled."
                        )
                    await ctx.edit(embed=embed, file=map_file)

            @discord.ui.button(
                label="<", style=discord.ButtonStyle.danger, disabled=True
            )
            async def back_button_callback(
                self, button: discord.Button, interaction: discord.Interaction
            ):
                self.flight_list_number -= 1
                if self.flight_list_number < 0:
                    return
                for child in self.children:
                    if str(child.type) == "ComponentType.string_select" and isinstance(
                        child, discord.ui.Select
                    ):
                        child.options = self.flights[self.flight_list_number]  # type: ignore
                    elif isinstance(child, discord.ui.Button):
                        if (self.flight_list_number == 0) and (child.label == "<"):
                            child.disabled = True
                        elif str(child.label).endswith(str(len(self.flights))):
                            child.label = (
                                f"{self.flight_list_number+1}/{len(self.flights)}"
                            )
                        else:
                            child.disabled = False
                await interaction.response.edit_message(view=self)

            @discord.ui.button(
                label=f"{flight_list_number+1}/{len(flights)}",
                style=discord.ButtonStyle.secondary,
                disabled=True,
            )
            async def page_button(
                self, button: discord.Button, interaction: discord.Interaction
            ):
                pass

            @discord.ui.button(
                label=">", style=discord.ButtonStyle.primary, disabled=is_disabled()
            )
            async def next_button_callback(
                self, button: discord.Button, interaction: discord.Interaction
            ):
                self.flight_list_number += 1
                if self.flight_list_number > len(self.flights) - 1:
                    return
                for child in self.children:
                    if str(child.type) == "ComponentType.string_select" and isinstance(
                        child, discord.ui.Select
                    ):
                        child.options = self.flights[self.flight_list_number]  # type: ignore
                    elif isinstance(child, discord.ui.Button):
                        if (self.flight_list_number == (len(self.flights) - 1)) and (
                            child.label == ">"
                        ):
                            child.disabled = True
                        elif str(child.label).endswith(str(len(self.flights))):
                            child.label = (
                                f"{self.flight_list_number+1}/{len(self.flights)}"
                            )
                        else:
                            child.disabled = False

                await interaction.response.edit_message(view=self)

        embed = discord.Embed(
            title=f"Select one of {user.name}'s flights!", colour=self.bot.color()
        )
        await ctx.respond(
            embed=embed,
            view=VAFlightSelectView(
                bot=self.bot, flights=flights, flight_list_number=flight_list_number
            ),
        )

    @va.command(
        name="leaderboard", description="🏆 See who has the most flights in the VA!"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @is_banned_check()
    async def va_lb(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        async with aiosqlite.connect("va.db") as db:
            cursor = await db.execute(
                "SELECT user_id, COUNT(*) as flight_count FROM flights GROUP BY user_id ORDER BY flight_count DESC"
            )
            lb = await cursor.fetchall()

        font = ImageFont.truetype(
            "fonts/Inter-Regular.ttf",
            size=43,
            layout_engine=ImageFont.Layout.BASIC,
        )
        img = Image.open(f"images/leaderboard/{self.bot.theme}/lb.png")
        names = [
            f"{i}      {self.bot.user_object(await self.bot.get_or_fetch_user(int(elem[0]))).name}"
            for i, elem in enumerate(lb, 1)
        ]
        values = [f"Flights: {elem[1]}" for elem in lb]
        with Pilmoji(img) as pilmoji:
            pilmoji.text(
                (790, 30),
                "\n\n".join(values[:10]),
                fill=(255, 255, 255),
                font=font,
                emoji_position_offset=(0, 20),
            )
            pilmoji.text(
                (27, 30),
                "\n\n".join(names[:10]),
                fill=(255, 255, 255),
                font=font,
                emoji_position_offset=(0, 20),
            )
        w, h = img.size
        with io.BytesIO() as output:
            if len(values) < 10:
                img.crop((0, 0, w, h - 95 * (10 - len(values)))).save(
                    output, format="PNG"
                )
            else:
                img.save(output, format="PNG")
            output.seek(0)
            file = discord.File(output, filename="lb.png")
        embed = discord.Embed(
            title="ClearFly VA Leaderboard",
            description="See more information with </va stats:1016059999056826479>!",
            colour=self.bot.color(),
        ).set_image(url="attachment://lb.png")
        await ctx.respond(embed=embed, file=file)

    @va.command(name="stats", description="📊 See the statistics of the ClearFly VA!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @is_banned_check()
    async def va_stats(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute("SELECT COUNT(*) FROM flights")
            total_flights = await cur.fetchone()
            if not total_flights:
                raise Exception("Failed to get flight count.")
            total_flights = total_flights[0]

            cur = await db.execute("SELECT COUNT(*) FROM flights WHERE incident != ''")
            incident_flights = await cur.fetchone()
            if not incident_flights:
                raise Exception("Failed to get incident count.")
            incident_flights = incident_flights[0]

            cur = await db.execute("SELECT COUNT(*) FROM users")
            total_users = await cur.fetchone()
            if not total_users:
                raise Exception("Failed to get incident count.")
            total_users = total_users[0]

            cur = await db.execute(
                "SELECT aircraft, COUNT(*) as count FROM flights GROUP BY aircraft ORDER BY count DESC LIMIT 1"
            )
            most_used_aircraft = await cur.fetchone()
            if not most_used_aircraft:
                raise Exception("Failed to get most used aircraft.")
            most_used_aircraft = most_used_aircraft[0]

            cur = await db.execute(
                "SELECT COUNT(*), COUNT(CASE WHEN is_official THEN 1 END) FROM aircraft"
            )
            total_aircraft = await cur.fetchone()
            if not total_aircraft:
                raise Exception("Failed to get aircraft count.")

            cur = await db.execute(
                "SELECT origin, COUNT(*) as count FROM flights GROUP BY origin ORDER BY count DESC LIMIT 1"
            )
            most_common_origin = await cur.fetchone()
            if not most_common_origin:
                raise Exception("Failed to get most common origin.")
            most_common_origin = most_common_origin[0]

            cur = await db.execute(
                "SELECT destination, COUNT(*) as count FROM flights GROUP BY destination ORDER BY count DESC LIMIT 1"
            )
            most_common_destination = await cur.fetchone()
            if not most_common_destination:
                raise Exception("Failed to get most common destination.")
            most_common_destination = most_common_destination[0]

            cur = await db.execute(
                "SELECT COUNT(*) FROM flights WHERE divert IS NOT ''"
            )
            diversions = await cur.fetchone()
            if not diversions:
                raise Exception("Failed to get diversions count.")
            diversions = diversions[0]

            cur = await db.execute("SELECT origin, destination FROM flights")
            origins_dests = await cur.fetchall()

        avg_flights_per_user = total_flights / total_users if total_users else 0

        with open("airports.json", "r") as file:
            airports_data = json.load(file)

        total_distance_nm = 0
        total_distance_km = 0
        total_distance_mi = 0
        for flight in origins_dests:
            total_distance_nm += calculate_distance(
                (
                    airports_data.get(flight[0])["lat"],
                    airports_data.get(flight[0])["lon"],
                ),
                (
                    airports_data.get(flight[1])["lat"],
                    airports_data.get(flight[1])["lon"],
                ),
            )
            total_distance_km += calculate_distance(
                (
                    airports_data.get(flight[0])["lat"],
                    airports_data.get(flight[0])["lon"],
                ),
                (
                    airports_data.get(flight[1])["lat"],
                    airports_data.get(flight[1])["lon"],
                ),
                unit="KM",
            )
            total_distance_mi += calculate_distance(
                (
                    airports_data.get(flight[0])["lat"],
                    airports_data.get(flight[0])["lon"],
                ),
                (
                    airports_data.get(flight[1])["lat"],
                    airports_data.get(flight[1])["lon"],
                ),
                unit="MI",
            )

        if total_distance_km > 0:
            distance_compare_phrase = f"{round((total_distance_km/12742)*100 ,1)}% of the diameter of the Earth"
        elif total_distance_km > 13000:
            distance_compare_phrase = f"{round((total_distance_km/17964)*100 ,1)}% of the A350's maximum range"
        elif total_distance_km > 18000:
            distance_compare_phrase = (
                f"{round((total_distance_km/40075)*100 ,1)}% of the equator's length"
            )
        elif total_distance_km > 384400:
            distance_compare_phrase = f"{round((total_distance_km/384400)*100 ,1)}% of the distance between the Moon and the Earth"
        else:
            distance_compare_phrase = f""

        embed = discord.Embed(title="ClearFly VA Statistics", colour=self.bot.color())
        embed.add_field(
            name="Users",
            inline=False,
            value=f"""
Number of users: **{total_users}**
Average flights per user: **{round(avg_flights_per_user)}**
Total distance flown by users: **{round(total_distance_nm, 1)}**nm, **{round(total_distance_km, 1)}**km, **{round(total_distance_mi, 1)}**mi *that's {distance_compare_phrase}!*
*Check who has filed the most flights with the </va leaderboard:1016059999056826479> commmand!*
        """,
        )
        embed.add_field(
            name="Flights",
            inline=False,
            value=f"""
Number of flights: **{total_flights}**
Number of diversions: **{diversions}**
Number of incidents: **{incident_flights}**
Success rate: **{100-round((incident_flights/total_flights)*100, 1)}%** *a 'successful' flight is a flight without a diversion or incident.*
Most common origin: **{most_common_origin}**
Most common destination: **{most_common_destination}**
        """,
        )
        embed.add_field(
            name="Aircraft",
            inline=False,
            value=f"""
Number of aircraft: **{total_aircraft[0]}** (**{total_aircraft[1]}** official)
Most used aircraft: **{most_used_aircraft}**
        """,
        )
        await ctx.respond(embed=embed)

    @flight.command(
        name="flightnumber",
        description="💯 Generate a flight number based on the provided values.",
    )
    @discord.option(
        name="aircraft",
        description="The aircraft you want to fly with, ICAO code please (e.g. B738).",
        autocomplete=get_aircraft,
    )
    @discord.option(
        name="origin",
        description="The airport you want to fly from, in ICAO format (e.g. KJFK).",
        autocomplete=get_airports,
    )
    @discord.option(
        name="destination",
        description="The airport you want to fly to, in ICAO format (e.g. EBBR).",
        autocomplete=get_airports,
    )
    @commands.has_role(1013933799777783849)
    @is_banned_check()
    async def va_flightnumber(
        self,
        ctx: discord.ApplicationContext,
        aircraft: str,
        origin: str,
        destination: str,
    ):
        await ctx.defer()

        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute("SELECT icao FROM aircraft")
            ac_list = await cur.fetchall()
            ac_list = [craft[0] for craft in ac_list]
            cur = await db.execute("SELECT * FROM aircraft WHERE icao=?", (aircraft,))
            aircraft_data = await cur.fetchone()
            if not aircraft_data:
                raise Exception("Couldn't fetch aircraft data.")

        if aircraft not in ac_list:
            embed = discord.Embed(
                title="Invalid aircraft",
                colour=self.bot.color(1),
                description="Please provide a valid aircraft ICAO code (e.g. B738).",
            )
            await ctx.respond(embed=embed)
            return

        if (origin[:4].upper()) not in airports_icao:
            embed = discord.Embed(
                title="Invalid origin",
                colour=self.bot.color(1),
                description="Please provide a valid airport ICAO code (e.g. KJFK).",
            )
            await ctx.respond(embed=embed)
            return
        if (destination[:4].upper()) not in airports_icao:
            embed = discord.Embed(
                title="Invalid destination",
                colour=self.bot.color(1),
                description="Please provide a valid airport ICAO code (e.g. KJFK).",
            )
            await ctx.respond(embed=embed)
            return

        origin = origin[:4].upper()
        destination = destination[:4].upper()

        with open("airports.json", "r") as f:
            airport_data = json.load(f)

        flight_time = str(
            datetime.timedelta(
                hours=calculate_time(
                    (
                        airport_data.get(origin[:4].upper()).get("lat", 0),
                        airport_data.get(origin[:4].upper()).get("lon", 0),
                    ),
                    (
                        airport_data.get(destination[:4].upper()).get("lat", 0),
                        airport_data.get(destination[:4].upper()).get("lon", 0),
                    ),
                    aircraft_data[4],
                )
            )
        ).split(":")

        flight_time = f"{flight_time[0]}:{flight_time[1]}"

        distance = (
            str(
                round(
                    calculate_distance(
                        (
                            airport_data.get(origin[:4].upper()).get("lat", 0),
                            airport_data.get(origin[:4].upper()).get("lon", 0),
                        ),
                        (
                            airport_data.get(destination[:4].upper()).get("lat", 0),
                            airport_data.get(destination[:4].upper()).get("lon", 0),
                        ),
                    )
                )
            )
            + " NM"
        )

        embed = discord.Embed(
            title=await generate_flight_number(aircraft, origin, destination),
            description=f"""
Departs from **{origin[:4].upper()}**, landing at **{destination[:4].upper()}** using a **{aircraft[:4].upper()}**. 
The distance between airports is **{distance}** with estimated flight time being **{flight_time}**.
""",
            color=self.bot.color(),
        )
        await ctx.respond(embed=embed)

    @vadmin.command(description="⚙️ Setup the VA system.")
    @commands.has_role(965422406036488282)
    async def setup(self, ctx: discord.ApplicationContext):
        fbo = self.bot.sendable_channel(
            self.bot.get_channel(self.bot.channels.get("fbo", 0))
        )
        if not fbo:
            raise Exception("Didn't find the fbo channel.")
        embed = discord.Embed(
            title="ClearFly VA",
            colour=self.bot.color(),
            description=f"""
ClearFly VA is a Virtual Airline that offers a fun way to fly without requiring any prior training or extensive knowledge on aviation. However, we expect our pilots to behave professionally, without engaging in any intentional crashing, starting engines on the runway, or any other unprofessional activities.

## Ready to get started with ClearFly VA? Follow these steps
    **1.** Visit {fbo.mention} and enter </va flight file:1016059999056826479>.
    **2.** Click on the command that appears and input the necessary information. Then, run the command.
    **3.** Fly your flight with a ClearFly livery (available in <#1041057335449227314> or <#1087399445966110881>).
    **4.** Once you complete your flight, run the command </va flight complete:1016059999056826479> within 24 hours. Otherwise, the flight will be automatically cancelled.

## Wondering what aircraft you can fly?
You can choose any aircraft that has a ClearFly livery, available in <#1041057335449227314> for official paints or in <#1087399445966110881> for community-made liveries. Just be sure you equip your aircraft with a ClearFly livery before taking off. 

Happy flying!
            """,
        )
        embed2 = discord.Embed(
            title="Recommended add-ons: StableApproach",
            colour=self.bot.color(),
            description="""
## Download
https://forums.x-plane.org/index.php?/files/file/76763-stableapproach-flight-data-monitoring-for-x-plane/ 
## Setup
**1.** Open the StableApproach settings in the plugins menu.
**2.** Open the “Virtual Airline” category.
**3.** Put the text in the box labeled “Virtual Airline”: “ClearFly-Official/StableApproach”. Also copy your User ID, you'll need this later.
**4.** Go to the “Aircraft” tab. Click “Download VA Profile”, and click “Apply + Save”. This will enable StableApproach to use our profile for that aircraft whenever you fly it.
**5.** Use the `/va user set_sa_id` command and paste the User ID you copied earlier in it.
**6.** That’s it! StableApproach will now download our custom aircraft profiles and send landing reports in <#1013934267966967848>.
        """,
        )
        embm = discord.Embed(
            title="ClearFly VA Official Liveries",
            colour=self.bot.color(),
            description="Below you can find all official ClearFly liveries. Don't see the aircraft you want to fly? Someone might have made it in <#1087399445966110881>!",
        )
        emb1 = discord.Embed(
            title="Boeing 737-800 by Zibo",
            colour=self.bot.color(),
            url="https://drive.google.com/file/d/1bNXkHHlItE-MhfM6Nc-l5-W75zW9thYP/view?usp=share_link",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1054156349568729139/1100161617326526606/icon.png"
        )
        emb2 = discord.Embed(
            title="Cessna Citation X by Laminar Research",
            colour=self.bot.color(),
            url="https://drive.google.com/file/d/1X4sShTh58rDucdeJQbX1VdkZtqvBXJIQ/view?usp=sharing",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1054156349568729139/1100161617666252930/Cessna_CitationX_icon11.png"
        )
        emb3 = discord.Embed(
            title="Cessna 172SP by Laminar Research",
            colour=self.bot.color(),
            url="https://drive.google.com/file/d/1wQgPFIhMJixk3xt2gNrvfa-okTLWIjgv/view?usp=share_link",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1054156349568729139/1099739093551829022/Cessna_172SP_icon11.png"
        )
        emb4 = discord.Embed(
            title="Cessna 172SP (G1000) by Laminar Research",
            colour=self.bot.color(),
            url="https://drive.google.com/file/d/1jGElFWge_vb_6riAol6bnOIos-thwJJA/view?usp=share_link",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1001401783689678868/1133803168115982396/Cessna_172SP_G1000_icon11.png"
        )
        embs = [embm, emb1, emb2, emb3, emb4]
        liv_channel = self.bot.sendable_channel(
            self.bot.get_channel(self.bot.channels.get("va-liveries", 0))
        )
        overv_channel = self.bot.sendable_channel(
            self.bot.channels.get("va-overview", 0)
        )
        await ctx.respond("All ready to go!", ephemeral=True)
        if overv_channel and liv_channel:
            await overv_channel.send(
                embeds=[embed, embed2], view=VAStartView(bot=self.bot)
            )
            await liv_channel.send(embeds=embs)

    @vadmin.command(
        name="add_aircraft", description="➕ Add a new aircraft to the VA fleet."
    )
    @discord.option(name="icao", description="The ICAO code of the new aircraft.")
    @discord.option(
        name="aircraft_type",
        description="The type of aircraft.",
        choices=[
            "Airliner",
            "GA",
            "Military",
            "Cargo",
            "Helicopter",
            "Ultra-light",
            "Glider",
        ],
    )
    @discord.option(name="crz_speed", description="Aircraft cruise speed in TAS.")
    @discord.option(
        name="is_official", description="If the aircraft has an official livery."
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_role(965422406036488282)
    async def add_ac(
        self,
        ctx: discord.ApplicationContext,
        icao: str,
        aircraft_type: str,
        crz_speed: int,
        is_official: bool,
    ):
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute("SELECT icao FROM aircraft")
            aircraft = await cur.fetchall()
            aircraft = [aircraft[0] for aircraft in aircraft]

            if icao.upper() in aircraft:
                embed = discord.Embed(
                    title=f"`{icao.upper()}` is already in the fleet!",
                    colour=self.bot.color(1),
                    description="The aircraft you provided is already in the ClearFly VA fleet, please provide an aircraft that hasn't been added yet.",
                )
                await ctx.respond(embed=embed)
                return
            await db.execute(
                "INSERT INTO aircraft (icao, is_official, type, crz_speed) VALUES (?, ?, ?, ?)",
                (icao.upper(), is_official, aircraft_type, crz_speed),
            )
            await db.commit()
            embed = (
                discord.Embed(
                    title="Successfully added new aircraft", colour=self.bot.color()
                )
                .add_field(name="ICAO", value=icao.upper())
                .add_field(name="Type", value=aircraft_type)
                .add_field(name="CRZ speed", value=f"{crz_speed}kts (TAS)")
                .add_field(name="Is Official?", value=str(is_official))
            )
            await ctx.respond(embed=embed)

    @vadmin.command(
        name="remove_aircraft", description="🗑️ Remove an aircraft from the VA fleet."
    )
    @discord.option(
        name="icao",
        description="The ICAO code of the aircraft.",
        autocomplete=get_aircraft,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_role(965422406036488282)
    async def remove_ac(self, ctx: discord.ApplicationContext, icao: str):
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute("SELECT icao FROM aircraft")
            aircraft = await cur.fetchall()
            aircraft = [aircraft[0] for aircraft in aircraft]

            if icao.upper() in aircraft:
                await db.execute("DELETE FROM aircraft WHERE icao=?", (icao.upper(),))
                await db.commit()
                embed = discord.Embed(
                    title=f"`{icao.upper()}` deleted successfully",
                    colour=self.bot.color(),
                )
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(
                    title=f"`{icao.upper()}` is not in the fleet!",
                    colour=self.bot.color(1),
                    description="The aircraft you provided is no in the ClearFly VA fleet, please provide an aircraft that is actually in the fleet.",
                )
                await ctx.respond(embed=embed)
                return

    @vadmin.command(
        name="list_aircraft", description="🛩️ List the aircrafts of the VA fleet."
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_role(965422406036488282)
    async def list_ac(self, ctx: discord.ApplicationContext):
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute("SELECT * FROM aircraft")
            aircraft = await cur.fetchall()

        aircraft = [
            f"{i}: **{aircraft[1]}**, type: **{aircraft[3]}**, official: **{aircraft[2]}**"
            for i, aircraft in enumerate(aircraft, 1)
        ]
        embed = discord.Embed(
            title="List of VA fleet",
            description="\n".join(aircraft),
            colour=self.bot.color(),
        )
        await ctx.respond(embed=embed)

    @vadmin.command(name="ban", description="🔨 Ban a user from the VA.")
    @discord.option(name="user", description="The user to ban.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_role(965422406036488282)
    async def va_ban(self, ctx: discord.ApplicationContext, user: discord.Member):
        await ctx.defer()
        if not str(user.id) in list(await get_users("id")):
            embed = discord.Embed(
                title="That user is not part of the VA!", colour=self.bot.color(1)
            )
            await ctx.respond(embed=embed)
            return
        async with aiosqlite.connect("va.db") as db:
            await db.execute(
                "UPDATE users SET is_ban=1 WHERE user_id=?", (str(user.id),)
            )
            await db.commit()

        embed = discord.Embed(
            title="Successfully banned user!", colour=self.bot.color()
        )
        await ctx.respond(embed=embed)

    @vadmin.command(name="unban", description="🔨 Unban a user from the VA.")
    @discord.option(name="user", description="The user to unban.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_role(965422406036488282)
    async def va_uunban(self, ctx: discord.ApplicationContext, user: discord.Member):
        await ctx.defer()
        if not str(user.id) in list(await get_users("id")):
            embed = discord.Embed(
                title="That user is not part of the VA!", colour=self.bot.color(1)
            )
            await ctx.respond(embed=embed)
            return
        async with aiosqlite.connect("va.db") as db:
            await db.execute(
                "UPDATE users SET is_ban=0 WHERE user_id=?", (str(user.id),)
            )
            await db.commit()

        embed = discord.Embed(
            title="Successfully unbanned user!", colour=self.bot.color()
        )
        await ctx.respond(embed=embed)

    @va.command(
        name="liveries",
        description="🌄 Looking to fly for the ClearFly VA? Here are the liveries to get you started!",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def va_livs(self, ctx: discord.ApplicationContext):
        embm = discord.Embed(
            title="ClearFly VA Official Liveries",
            colour=self.bot.color(),
            description="Below you can find all official ClearFly liveries. Don't see the aircraft you want to fly? Someone might have made it in <#1087399445966110881>!",
        )
        emb1 = discord.Embed(
            title="Boeing 737-800 by Zibo",
            colour=self.bot.color(),
            url="https://drive.google.com/file/d/1bNXkHHlItE-MhfM6Nc-l5-W75zW9thYP/view?usp=share_link",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1054156349568729139/1100161617326526606/icon.png"
        )
        emb2 = discord.Embed(
            title="Cessna Citation X by Laminar Research",
            colour=self.bot.color(),
            url="https://drive.google.com/file/d/1X4sShTh58rDucdeJQbX1VdkZtqvBXJIQ/view?usp=sharing",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1054156349568729139/1100161617666252930/Cessna_CitationX_icon11.png"
        )
        emb3 = discord.Embed(
            title="Cessna 172SP by Laminar Research",
            colour=self.bot.color(),
            url="https://drive.google.com/file/d/1wQgPFIhMJixk3xt2gNrvfa-okTLWIjgv/view?usp=share_link",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1054156349568729139/1099739093551829022/Cessna_172SP_icon11.png"
        )
        emb4 = discord.Embed(
            title="Cessna 172SP (G1000) by Laminar Research",
            colour=self.bot.color(),
            url="https://drive.google.com/file/d/1jGElFWge_vb_6riAol6bnOIos-thwJJA/view?usp=share_link",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1001401783689678868/1133803168115982396/Cessna_172SP_G1000_icon11.png"
        )
        embs = [embm, emb1, emb2, emb3, emb4]
        await ctx.respond(embeds=embs)

    @user.command(
        name="set_sa_id",
        description="🆔 Set your StableApproach ID so we can post your landings on Discord.",
    )
    @discord.option(
        "sa_id", description="Your StableApproach UserID, found in the plugin settings."
    )
    @is_banned_check()
    async def set_id(self, ctx: discord.ApplicationContext, sa_id: str):
        await ctx.defer(ephemeral=True)

        self.col.update_one(
            {"discord_id": ctx.author.id},
            {"$set": {"sa_id": sa_id, "discord_id": ctx.author.id}},
            upsert=True,
        )
        embed = discord.Embed(
            title="Successfully set your StableApproach ID", colour=self.bot.color()
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(VACommands(bot))
