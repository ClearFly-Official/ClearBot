import datetime
import json
import textwrap
import aiohttp
import discord
import aiosqlite
import os
import random
import plotly.graph_objects as go
from io import BytesIO
import plotly.io as pio
import time
from discord.ext import commands, tasks
from discord.ext.pages import Paginator, Page
from main import errorc, warningc, cfc
from airports import airports, airports_icao
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji

overv_id = 1099712642916044881  # 1040927466975404054
fbo_id = 1013934267966967848


# get_types:
#     full
#     id
async def get_users(get_type="full"):
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


async def is_banned(user: discord.User | discord.Member):
    async with aiosqlite.connect("va.db") as db:
        cur = await db.execute(
            "SELECT is_ban FROM users WHERE user_id=?", (str(user.id),)
        )
        is_ban = await cur.fetchone()

    if (is_ban == ()) or (is_ban is None):
        return False
    elif is_ban[0] == 1:
        return True
    else:
        return False


async def generate_flight_number(
    aircraft_icao, origin_icao, destination_icao, prefix="CF"
):
    async with aiosqlite.connect("va.db") as db:
        cur = await db.execute("SELECT icao FROM aircraft")
        aircraft = await cur.fetchall()
        aircraft = [aircraft[0] for aircraft in aircraft]
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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


class VAStartView(discord.ui.View):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Start", style=discord.ButtonStyle.green, custom_id="VA:start_button"
    )
    async def start_button_callback(
        self, button: discord.Button, interaction: discord.Interaction
    ):
        user_ids = await get_users("id")
        if str(interaction.user.id) in user_ids:
            embed = discord.Embed(
                title="You're already part of the VA!",
                colour=errorc,
                description="Joining the VA when you're already in it, is not possible. Flying two aircraft in different parts of the world at the same time is impossible after all.",
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            guild = self.bot.get_guild(965419296937365514)
            role = guild.get_role(1013933799777783849)
            await interaction.user.add_roles(role)
            fbo = self.bot.get_channel(fbo_id)
            embed = discord.Embed(
                title="Thanks for joining our VA!",
                colour=cfc,
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
    def __init__(self, title):
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
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute(
                "SELECT id FROM flights WHERE user_id=?", (str(interaction.user.id),)
            )
            flights = await cur.fetchall()

            report = {
                "user_id": str(interaction.user.id),
                "flight_id": flights[-1][0],
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
                (flights[-1][0],),
            )
            await db.commit()
            embed = discord.Embed(
                title="Successfully reported incident!",
                description="You may view it with </va user view_report:1016059999056826479>.\n**Don't forget to complete your flight, otherwise it will be __deleted__!**",
                colour=cfc,
            )
            await interaction.response.send_message(embed=embed)


class VACommands(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

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

    async def get_airports(self, ctx: discord.AutocompleteContext):
        if ctx.value == "":
            return [
                "Start typing the name of an airport for results to appear(e.g. KJFK)"
            ]
        return [
            airport for airport in airports if airport.startswith(ctx.value.upper())
        ]

    async def get_aircraft(self, ctx: discord.AutocompleteContext):
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute("SELECT icao FROM aircraft")
            aircraft = await cur.fetchall()
            aircraft = [aircraft[0] for aircraft in aircraft]

        return [craft for craft in aircraft if craft.startswith(ctx.value.upper())]

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(VAStartView(self.bot))
        self.trial_check.start()
        self.completed_flight_check.start()
        print("| VA cog loaded successfully")

    @tasks.loop(minutes=10)
    async def trial_check(self):
        users = await get_users()
        for user in users:
            if ((round(time.time()) - user[2]) > 86_400) and (user[3] == 1):
                try:
                    user_dm = self.bot.get_user(int(user[1]))
                    guild = self.bot.get_guild(965419296937365514)
                    user_role = guild.get_member(int(user[1]))
                    role = guild.get_role(1013933799777783849)
                    await user_role.remove_roles(role)
                    if user_dm is not None:
                        user_embed = discord.Embed(
                            title="You have been kicked from the ClearFly VA.",
                            colour=cfc,
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
                if ((round(time.time()) - flight[6]) > 3_600) and (
                    (round(time.time()) - flight[6]) < 4_200
                ):
                    user = self.bot.get_user(int(flight[1]))
                    fbo = self.bot.get_channel(fbo_id)
                    embed = discord.Embed(
                        title=f"Your last filed flight will be cancelled <t:{flight[6]+86_400}:R>.",
                        colour=warningc,
                        description=f"""
Hey {user.name}! 

We have noticed that you have not completed your last flight yet. Please remember to mark your flight as completed with the command </va flight complete:1016059999056826479>.
Your flight will be cancelled if you fail to do so <t:{flight[6]+86_400}:R>. 

**THIS IS YOUR __LAST__ REMINDER**
                            """,
                    )
                if ((round(time.time()) - flight[6]) > 21_600) and (
                    (round(time.time()) - flight[6]) < 22_200
                ):
                    user = self.bot.get_user(int(flight[1]))
                    fbo = self.bot.get_channel(fbo_id)
                    embed = discord.Embed(
                        title=f"Your last filed flight will be cancelled <t:{flight[6]+86_400}:R>.",
                        colour=warningc,
                        description=f"""
Hey {user.name}! 

We have noticed that you have not completed your last flight yet. Please remember to mark your flight as completed with the command </va flight complete:1016059999056826479>.
Your flight will be cancelled if you fail to do so <t:{flight[6]+86_400}:R>. You will be reminded one last time before it's too late <t:{flight[6]+82_800}:R>
                            """,
                    )
                    await fbo.send(user.mention, embed=embed)
                if ((round(time.time()) - flight[6]) > 43_200) and (
                    (round(time.time()) - flight[6]) < 43_800
                ):
                    user = self.bot.get_user(int(flight[1]))
                    fbo = self.bot.get_channel(fbo_id)
                    embed = discord.Embed(
                        title=f"Your last filed flight will be cancelled <t:{flight[6]+86_400}:R>.",
                        colour=warningc,
                        description=f"""
Hey {user.name}! 

We have noticed that you have not completed your last flight yet. Please remember to mark your flight as completed with the command </va flight complete:1016059999056826479>.
Your flight will be cancelled if you fail to do so <t:{flight[6]+86_400}:R>. Another reminder will be sent <t:{flight[6]+64_800}:R> if you haven't completed it yet.
                            """,
                    )
                    await fbo.send(user.mention, embed=embed)
                if (round(time.time()) - flight[6]) > 86_400:
                    await db.execute("DELETE FROM flights WHERE id=?", (flight[0],))
                    await db.execute(
                        "DELETE FROM reports WHERE flight_id=?", (flight[0],)
                    )
                    user = self.bot.get_user(int(flight[1]))
                    fbo = self.bot.get_channel(fbo_id)
                    embed = discord.Embed(
                        title="Your last filed flight has been cancelled.",
                        colour=warningc,
                        description=f"""
Hi there {user.name},

Around <t:{flight[6]}:R> you filed a flight, but never marked it as completed. To prevent people filing a flight, but never actually completing it, we automatically cancel it after 24 hours. 
This sadly happened to your last flight. Please remember to mark your flight as completed next time!
                            """,
                    )
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
    @commands.cooldown(1, 60)
    async def va_file(
        self,
        ctx: discord.ApplicationContext,
        aircraft: str,
        origin: str,
        destination: str,
    ):
        await ctx.defer()
        if await is_banned(ctx.author):
            embed = discord.Embed(title="You're banned from the VA!", colour=errorc)
            await ctx.respond(embed=embed)
            return
        usrs = await get_users("id")
        if str(ctx.author.id) not in usrs:
            overv_channel = self.bot.get_channel(overv_id)
            embed = discord.Embed(
                title="You're not part of the VA!",
                colour=errorc,
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
                colour=errorc,
                description="Please provide a valid aircraft ICAO code (e.g. B738).",
            )
            await ctx.respond(embed=embed)
            return
        if (origin[:4].upper()) not in airports_icao:
            embed = discord.Embed(
                title="Invalid origin",
                colour=errorc,
                description="Please provide a valid airport ICAO code (e.g. KJFK).",
            )
            await ctx.respond(embed=embed)
            return
        if (destination[:4].upper()) not in airports_icao:
            embed = discord.Embed(
                title="Invalid destination",
                colour=errorc,
                description="Please provide a valid airport ICAO code (e.g. KJFK).",
            )
            await ctx.respond(embed=embed)
            return
        hdr = {"X-API-Key": os.getenv("CWX_KEY")}
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                f"https://api.checkwx.com/metar/{origin[:4].upper()}",
                headers=hdr,
            ) as r:
                r.raise_for_status()
                resp = await r.json()
        flight_num = await generate_flight_number(
            aircraft, origin[:4].upper(), destination[:4].upper()
        )
        embed = discord.Embed(
            title="Flight filed successfully!",
            colour=cfc,
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
                if is_completed[-1][0] == 0:
                    embed = discord.Embed(
                        title="You haven't completed your last flight!",
                        colour=errorc,
                        description="The last flight you filed hasn't been marked as completed, thus you can't file a new one.",
                    )
                    await ctx.respond(embed=embed)
                    return
        card_id = "flight_card" + str(random.randint(0, 9)) + ".png"
        img = Image.open("images/va_flightcard_blank.png")
        font = ImageFont.truetype("fonts/Inter-Regular.ttf", size=60)
        small_font = ImageFont.truetype("fonts/Inter-Regular.ttf", size=50)
        hdr_font = ImageFont.truetype("fonts/Inter-Regular.ttf", size=39)
        data = ""
        if resp["results"] == 0:
            data = "No METAR data found."
        else:
            data = str(resp["data"][0])
        with Pilmoji(img) as pilmoji:
            colour = (109, 178, 217)
            date = str(datetime.datetime.now().date()).split("-")
            date.reverse()
            filed_at_str = (
                f"{datetime.datetime.now().hour}:{datetime.datetime.now().minute} UTC"
            )
            pilmoji.text(
                (1228 - small_font.getsize(filed_at_str)[0], 112),
                filed_at_str,
                font=small_font,
                fill=colour,
            )
            pilmoji.text(
                (1228 - small_font.getsize("/".join(date))[0], 161),
                "/".join(date),
                font=small_font,
                fill=colour,
            )
            pilmoji.text((127, 350), origin[:4].upper(), font=font, fill=colour)
            pilmoji.text(
                (1228 - font.getsize(destination[:4].upper())[0], 350),
                destination[:4].upper(),
                font=font,
                fill=colour,
            )
            pilmoji.text(
                (127, 620),
                textwrap.fill(ctx.author.name, 10, max_lines=2),
                font=font,
                fill=colour,
            )
            pilmoji.text((525, 620), flight_num, font=font, fill=colour)
            pilmoji.text(
                (1228 - font.getsize(aircraft)[0], 620),
                aircraft,
                font=font,
                fill=colour,
            )
            pilmoji.text(
                (127, 776),
                origin[:4].upper() + " METAR",
                font=hdr_font,
                fill=(255, 255, 255),
            )
            pilmoji.text(
                (127, 830),
                textwrap.fill(data, 35, max_lines=3),
                font=font,
                fill=colour,
            )
        img.save(f"images/{card_id}")
        file = discord.File(f"images/{card_id}", filename=card_id)
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
        os.remove(f"images/{card_id}")

    @flight.command(
        name="complete", description="✅ Mark your last flight as completed."
    )
    @commands.cooldown(1, 60)
    @commands.has_role(1013933799777783849)
    async def va_complete(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if await is_banned(ctx.author):
            embed = discord.Embed(title="You're banned from the VA!", colour=errorc)
            await ctx.respond(embed=embed)
            return
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
                    colour=errorc,
                    description="I did not find any flights filed by you that are not marked as completed.",
                )
                await ctx.respond(embed=embed)
                return
            else:
                await db.execute(
                    "UPDATE flights SET is_completed=1 WHERE id=?", (flight_ids[0][0],)
                )
                await db.commit()
            embed = discord.Embed(
                title="Flight completed!",
                colour=cfc,
                description="You have marked your flight as completed, and it has been permantly logged.",
            ).add_field(
                name="Flight Details",
                value=f"""
Flight number: **{flight_id2[0][2]}**
Aircraft: **{flight_id2[0][3]}**
Origin: **{flight_id2[0][4]}**
Destination: **{flight_id2[0][5]}**
            """,
            )
        await ctx.respond(embed=embed)

    @flight.command(name="cancel", description="❌ Cancel your last flight.")
    @commands.cooldown(1, 60)
    @commands.has_role(1013933799777783849)
    async def va_cancel(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if await is_banned(ctx.author):
            embed = discord.Embed(title="You're banned from the VA!", colour=errorc)
            await ctx.respond(embed=embed)
            return
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute(
                "SELECT * FROM flights WHERE user_id=?", (str(ctx.author.id),)
            )
            flights = await cur.fetchall()

            if flights == []:
                embed = discord.Embed(title="No flights found!", colour=errorc)
                await ctx.respond(embed=embed)
                return
            last_flight = flights[-1]

            if last_flight[7]:
                embed = discord.Embed(
                    title="You completed your last flight!",
                    description="I can't cancel a flight you have done already!",
                    colour=errorc,
                )
                await ctx.respond(embed=embed)
            else:
                await db.execute("DELETE FROM flights WHERE id=?", (last_flight[0],))
                await db.execute(
                    "DELETE FROM reports WHERE flight_id=?", (last_flight[0],)
                )
                await db.commit()
                embed = discord.Embed(
                    title="Flight successfully cancelled!", colour=cfc
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
    @commands.has_role(1013933799777783849)
    async def va_divert(self, ctx: discord.ApplicationContext, airport):
        await ctx.defer()
        if await is_banned(ctx.author):
            embed = discord.Embed(title="You're banned from the VA!", colour=errorc)
            await ctx.respond(embed=embed)
            return
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute(
                "SELECT * FROM flights WHERE user_id=?", (str(ctx.author.id),)
            )
            flights = await cur.fetchall()

            if flights == []:
                embed = discord.Embed(title="No flights found!", colour=errorc)
                await ctx.respond(embed=embed)
                return
            last_flight = flights[-1]

            if last_flight[7]:
                embed = discord.Embed(
                    title="You completed your last flight!",
                    description="I can't edit a flight you have completed already!",
                    colour=errorc,
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
                    colour=cfc,
                )
                await ctx.respond(embed=embed)

    @flight.command(
        name="report",
        description="📝 Report an incident that happend on your last flight.",
    )
    @commands.has_role(1013933799777783849)
    async def va_report(self, ctx: discord.ApplicationContext):
        if await is_banned(ctx.author):
            embed = discord.Embed(title="You're banned from the VA!", colour=errorc)
            await ctx.respond(embed=embed)
            return
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute(
                "SELECT * FROM flights WHERE user_id=?", (str(ctx.author.id),)
            )
            flights = await cur.fetchall()

            if flights == []:
                embed = discord.Embed(title="No flights found!", colour=errorc)
                await ctx.respond(embed=embed)
                return
            last_flight = flights[-1]

            if last_flight[7]:
                embed = discord.Embed(
                    title="You completed your last flight!",
                    description="I can't edit a flight you have completed already!",
                    colour=errorc,
                )
                await ctx.respond(embed=embed)
            else:
                await ctx.send_modal(VAReportModal(title="Report an incident"))

    @user.command(name="view_report", description="📄 View a users reports.")
    @discord.option(name="user", description="The user you want to see the flights of.")
    @commands.has_role(1013933799777783849)
    @commands.cooldown(1, 5)
    async def va_view_report(
        self, ctx: discord.ApplicationContext, user: discord.Member = None
    ):
        await ctx.defer()
        if await is_banned(ctx.author):
            embed = discord.Embed(title="You're banned from the VA!", colour=errorc)
            await ctx.respond(embed=embed)
            return
        if user == None:
            user = ctx.author

        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute(
                "SELECT * FROM reports WHERE user_id=?", (str(user.id),)
            )
            reports = await cur.fetchall()
            if reports == []:
                embed = discord.Embed(title="No reports found", colour=errorc)
                await ctx.respond(embed=embed)
                return
            reports.reverse()

        pages = [
            Page(
                embeds=[
                    discord.Embed(
                        title=f"{user.name}'s reports",
                        description=f"""
**<t:{report[3]}:F>: {report[4]}**
{report[5]}
                        """,
                        colour=cfc,
                    ).set_footer(text=f"Total of {len(reports)} reports")
                ]
            )
            for report in reports
        ]
        paginator = Paginator(pages)
        await paginator.respond(ctx.interaction)

    @user.command(name="flights", description="🛬 View a users flights.")
    @discord.option(name="user", description="The user you want to see the flights of.")
    @commands.has_role(1013933799777783849)
    @commands.cooldown(1, 5)
    async def va_flights(
        self, ctx: discord.ApplicationContext, user: discord.Member = None
    ):
        await ctx.defer()
        if await is_banned(ctx.author):
            embed = discord.Embed(title="You're banned from the VA!", colour=errorc)
            await ctx.respond(embed=embed)
            return
        if user is None:
            user = ctx.author
        flights = []
        async with aiosqlite.connect("va.db") as db:
            cursor = await db.execute(
                "SELECT * FROM flights WHERE user_id=?", (str(user.id),)
            )
            rows = await cursor.fetchall()
            if rows == []:
                embed = discord.Embed(
                    title="No flights found for this user!", colour=errorc
                )
                await ctx.respond(embed=embed)
                return
            flights = [
                f"**{i}**: **{row[2]}**, **{row[3]}**, **{row[4]}** -> **{row[5]}**{row[8]}, *filed <t:{row[6]}:f>*{row[9]}"
                for i, row in enumerate(rows, 1)
            ]

        chunks = [flights[i : i + 10] for i in range(0, len(flights), 10)]

        pages = [
            Page(
                embeds=[
                    discord.Embed(
                        title=f"Flights {i+1}-{i+len(chunk)}",
                        description="\n".join(chunk),
                        colour=cfc,
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
    @discord.option(name="user", description="The user you want to see the flights of.")
    @discord.option(name="auto_zoom", description="Zoom automatically to fit the flights.")
    @commands.cooldown(1, 10)
    async def va_flight_map(self, ctx: discord.ApplicationContext, user: discord.Member = None, auto_zoom: bool = True):
        await ctx.defer()
        if await is_banned(ctx.author):
            embed = discord.Embed(title="You're banned from the VA!", colour=errorc)
            await ctx.respond(embed=embed)
            return
        if user is None:
            user = ctx.author

        user_id = str(user.id)

        async with aiosqlite.connect("va.db") as db:
            cursor = await db.execute(
                "SELECT * FROM flights WHERE user_id=?", (str(user.id),)
            )
            amount = len(await cursor.fetchall())
            cursor = await db.execute("SELECT origin, destination FROM flights WHERE user_id=?", (user_id,))
            waypoints_data = await cursor.fetchall()

        with open('airports.json', 'r') as file:
            airports_data = json.load(file)

        waypoints = []

        for origin, destination in waypoints_data:
            origin_data = airports_data.get(origin)
            dest_data = airports_data.get(destination)

            if origin_data and dest_data:
                origin_coords = (origin_data['lat'], origin_data['lon'])
                dest_coords = (dest_data['lat'], dest_data['lon'])
                waypoints.append((origin_coords, dest_coords))

        fig = go.Figure()

        for waypoint in waypoints:
            fig.add_trace(
                go.Scattergeo(
                    lat=[wayp[0] for wayp in waypoint],
                    lon=[wayp[1] for wayp in waypoint],
                    mode='lines',
                    line=dict(color='#6db2d9', width=2),
                )
            )
        if auto_zoom:
            fig.update_geos(
                projection_type='natural earth',
                showland=True, landcolor='#093961',
                showocean=True, oceancolor='#142533',
                showcountries=True,
                showlakes=True, lakecolor='#142533',
                showframe=False,
                coastlinecolor="#2681b4",
                fitbounds='locations',
            )
        else:
            fig.update_geos(
                projection_type='equirectangular',
                showland=True, landcolor='#093961',
                showocean=True, oceancolor='#142533',
                showcountries=True,
                showlakes=True, lakecolor='#142533',
                showframe=False,
                coastlinecolor="#2681b4",
            )
        fig.update_layout(showlegend=False)
        image_bytes = fig.to_image(format='png')
        image = Image.open(BytesIO(image_bytes))

        grayscale_image = image.convert('L')

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

        output_filename = 'map.png'
        cropped_image.save(output_filename)

        with open(output_filename, 'rb') as file:
            map_file = discord.File(file)
            embed = discord.Embed(title=f"{user.name}'s flight map", description=f"{user.mention} has completed **{amount}** flight(s)!",colour=cfc).set_image(url=f"attachment://{output_filename}")
            if auto_zoom:
                embed.set_footer(text="Can't figure out where this is on the map? Try running the command with auto_zoom disabled.")
            await ctx.respond(embed=embed, file=map_file)
        os.remove(output_filename)

    @va.command(
        name="leaderboard", description="🏆 See who has the most flights in the VA!"
    )
    @commands.cooldown(1, 30)
    async def va_lb(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if await is_banned(ctx.author):
            embed = discord.Embed(title="You're banned from the VA!", colour=errorc)
            await ctx.respond(embed=embed)
            return
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
        img = Image.open("images/lbClear.png")
        names = [
            f"{i}      {self.bot.get_user(int(elem[0])).name}"
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
        if len(values) < 10:
            img.crop((0, 0, w, h - 95 * (10 - len(values)))).save("images/lb.png")
        else:
            img.save("images/lb.png")
        file = discord.File("images/lb.png", filename="lb.png")
        embed = discord.Embed(
            title="ClearFly VA Leaderboard",
            description="See more information with </va stats:1016059999056826479>!",
            colour=cfc,
        ).set_image(url="attachment://lb.png")
        await ctx.respond(embed=embed, file=file)
        os.remove("images/lb.png")

    @va.command(name="stats", description="📊 See the statistics of the ClearFly VA!")
    @commands.cooldown(1, 15)
    async def va_stats(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if await is_banned(ctx.author):
            embed = discord.Embed(title="You're banned from the VA!", colour=errorc)
            await ctx.respond(embed=embed)
            return

        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute("SELECT COUNT(*) FROM flights")
            total_flights = (await cur.fetchone())[0]

            cur = await db.execute("SELECT COUNT(*) FROM flights WHERE incident != ''")
            incident_flights = (await cur.fetchone())[0]

            cur = await db.execute("SELECT COUNT(*) FROM users")
            total_users = (await cur.fetchone())[0]

            cur = await db.execute(
                "SELECT aircraft, COUNT(*) as count FROM flights GROUP BY aircraft ORDER BY count DESC LIMIT 1"
            )
            most_used_aircraft = (await cur.fetchone())[0]

            cur = await db.execute(
                "SELECT COUNT(*), COUNT(CASE WHEN is_official THEN 1 END) FROM aircraft"
            )
            total_aircraft = await cur.fetchone()

            cur = await db.execute(
                "SELECT origin, COUNT(*) as count FROM flights GROUP BY origin ORDER BY count DESC LIMIT 1"
            )
            most_common_origin = (await cur.fetchone())[0]

            cur = await db.execute(
                "SELECT destination, COUNT(*) as count FROM flights GROUP BY destination ORDER BY count DESC LIMIT 1"
            )
            most_common_destination = (await cur.fetchone())[0]

            cur = await db.execute(
                "SELECT COUNT(*) FROM flights WHERE divert IS NOT ''"
            )
            diversions = (await cur.fetchone())[0]

        avg_flights_per_user = total_flights / total_users if total_users else 0

        embed = discord.Embed(title="ClearFly VA Statistics", colour=cfc)
        embed.add_field(
            name="Users",
            inline=False,
            value=f"""
Number of users: **{total_users}**
Average flights per user: **{round(avg_flights_per_user)}**
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

    @vadmin.command(description="⚙️ Setup the VA system.")
    @commands.has_role(965422406036488282)
    async def setup(self, ctx: discord.ApplicationContext):
        fbo = self.bot.get_channel(fbo_id)
        embed = discord.Embed(
            title="ClearFly VA",
            colour=cfc,
            description=f"""
ClearFly VA is a Virtual Airline that offers a fun way to fly without requiring any prior training or extensive knowledge on aviation. However, we expect our pilots to behave professionally, without engaging in any intentional crashing, starting engines on the runway, or any other unprofessional activities.

**__Ready to get started with ClearFly VA? Follow these steps:__**
    **1.** Visit {fbo.mention} and enter </va flight file:1016059999056826479>.
    **2.** Click on the command that appears and input the necessary information. Then, run the command.
    **3.** Fly your flight with a ClearFly livery (available in <#1041057335449227314> or <#1087399445966110881>).
    **4.** Once you complete your flight, run the command </va flight complete:1016059999056826479> within 24 hours. Otherwise, the flight will be automatically cancelled.

**__Wondering what aircraft you can fly?__**
You can choose any aircraft that has a ClearFly livery, available in <#1041057335449227314> for official paints or in <#1087399445966110881> for community-made liveries. Just be sure you equip your aircraft with a ClearFly livery before taking off. 

Happy flying!
            """,
        )
        embed2 = discord.Embed(
            title="Recommended add-ons: StableApproach",
            colour=cfc,
            description="""
**__Download:__**
https://forums.x-plane.org/index.php?/files/file/76763-stableapproach-flight-data-monitoring-for-x-plane/ 
**__Setup:__**
**1.** Open the StableApproach settings in the plugins menu.
**2.** Open the “Virtual Airline” category.
**3.** Put the text in the box labeled “Virtual Airline”: “ClearFly-Official/StableApproach”.
**4.** Go to the “Aircraft” tab. Click “Download VA Profile”, and click “Apply + Save”. This will enable StableApproach to use our profile for that aircraft whenever you fly it.
**5.** That’s it! StableApproach will now download our custom aircraft profiles.
        """,
        )
        embm = discord.Embed(
            title="ClearFly VA Official Liveries",
            colour=cfc,
            description="Below you can find all official ClearFly liveries. Don't see the aircraft you want to fly? Someone might have made it in <#1087399445966110881>!",
        )
        emb1 = discord.Embed(
            title="Boeing 737-800 by Zibo",
            colour=cfc,
            url="https://drive.google.com/file/d/1bNXkHHlItE-MhfM6Nc-l5-W75zW9thYP/view?usp=share_link",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1054156349568729139/1100161617326526606/icon.png"
        )
        emb2 = discord.Embed(
            title="Cessna Citation X by Laminar Research",
            colour=cfc,
            url="https://drive.google.com/file/d/1X4sShTh58rDucdeJQbX1VdkZtqvBXJIQ/view?usp=sharing",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1054156349568729139/1100161617666252930/Cessna_CitationX_icon11.png"
        )
        emb3 = discord.Embed(
            title="Cessna 172SP by Laminar Research",
            colour=cfc,
            url="https://drive.google.com/file/d/1Fh0B1MKJWW4aSo0uOe4AF2pj4orKfOSI/view?usp=sharing",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1054156349568729139/1099739093551829022/Cessna_172SP_icon11.png"
        )
        embs = [embm, emb1, emb2, emb3]
        liv_channel = self.bot.get_channel(1041057335449227314)
        overv_channel = self.bot.get_channel(overv_id)
        await ctx.respond("All ready to go!", ephemeral=True)
        await overv_channel.send(embeds=[embed, embed2], view=VAStartView(bot=self.bot))
        await liv_channel.send(embeds=embs)

    @vadmin.command(
        name="add_aircraft", description="➕ Add a new aircraft to the VA fleet."
    )
    @discord.option(name="icao", description="The ICAO code of the new aircraft.")
    @discord.option(
        name="is_official", description="If the aircraft has an official livery."
    )
    @commands.has_role(965422406036488282)
    async def add_ac(
        self, ctx: discord.ApplicationContext, icao: str, is_official: bool
    ):
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute("SELECT icao FROM aircraft")
            aircraft = await cur.fetchall()
            aircraft = [aircraft[0] for aircraft in aircraft]

            if icao.upper() in aircraft:
                embed = discord.Embed(
                    title=f"`{icao.upper()}` is already in the fleet!",
                    colour=errorc,
                    description="The aircraft you provided is already in the ClearFly VA fleet, please provide an aircraft that hasn't been added yet.",
                )
                await ctx.respond(embed=embed)
                return
            await db.execute(
                "INSERT INTO aircraft (icao, is_official) VALUES (?, ?)",
                (icao.upper(), is_official),
            )
            await db.commit()
            embed = (
                discord.Embed(title="Successfully added new aircraft", colour=cfc)
                .add_field(name="ICAO", value=icao.upper())
                .add_field(name="Is Official?", value=is_official)
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
    @commands.cooldown(1, 10)
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
                    title=f"`{icao.upper()}` deleted successfully", colour=cfc
                )
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(
                    title=f"`{icao.upper()}` is not in the fleet!",
                    colour=errorc,
                    description="The aircraft you provided is no in the ClearFly VA fleet, please provide an aircraft that is actually in the fleet.",
                )
                await ctx.respond(embed=embed)
                return

    @vadmin.command(
        name="list_aircraft", description="🛩️ List the aircrafts of the VA fleet."
    )
    @commands.cooldown(1, 10)
    @commands.has_role(965422406036488282)
    async def list_ac(self, ctx: discord.ApplicationContext):
        async with aiosqlite.connect("va.db") as db:
            cur = await db.execute("SELECT * FROM aircraft")
            aircraft = await cur.fetchall()

        aircraft = [
            f"{aircraft[0]}: **{aircraft[1]}**, official: **{aircraft[2]}**"
            for aircraft in aircraft
        ]
        embed = discord.Embed(
            title="List of VA fleet", description="\n".join(aircraft), colour=cfc
        )
        await ctx.respond(embed=embed)

    @vadmin.command(name="ban", description="🔨 Ban a user from the VA.")
    @discord.option(name="user", description="The user to ban.")
    @commands.has_role(965422406036488282)
    async def va_ban(self, ctx: discord.ApplicationContext, user: discord.Member):
        await ctx.defer()
        if not str(user.id) in await get_users("id"):
            embed = discord.Embed(
                title="That user is not part of the VA!", colour=errorc
            )
            await ctx.respond(embed=embed)
            return
        async with aiosqlite.connect("va.db") as db:
            await db.execute(
                "UPDATE users SET is_ban=1 WHERE user_id=?", (str(user.id),)
            )
            await db.commit()

        embed = discord.Embed(title="Successfully banned user!", colour=cfc)
        await ctx.respond(embed=embed)

    @vadmin.command(name="unban", description="🔨 Unban a user from the VA.")
    @discord.option(name="user", description="The user to unban.")
    @commands.has_role(965422406036488282)
    async def va_uunban(self, ctx: discord.ApplicationContext, user: discord.Member):
        await ctx.defer()
        if not str(user.id) in await get_users("id"):
            embed = discord.Embed(
                title="That user is not part of the VA!", colour=errorc
            )
            await ctx.respond(embed=embed)
            return
        async with aiosqlite.connect("va.db") as db:
            await db.execute(
                "UPDATE users SET is_ban=0 WHERE user_id=?", (str(user.id),)
            )
            await db.commit()

        embed = discord.Embed(title="Successfully unbanned user!", colour=cfc)
        await ctx.respond(embed=embed)

    @va.command(
        name="liveries",
        description="🌄 Looking to fly for the ClearFly VA? Here are the liveries to get you started!",
    )
    async def va_livs(self, ctx: discord.ApplicationContext):
        embm = discord.Embed(
            title="ClearFly VA Official Liveries",
            colour=cfc,
            description="Below you can find all official ClearFly liveries. Don't see the aircraft you want to fly? Someone might have made it in <#1087399445966110881>!",
        )
        emb1 = discord.Embed(
            title="Boeing 737-800 by Zibo",
            colour=cfc,
            url="https://drive.google.com/file/d/1bNXkHHlItE-MhfM6Nc-l5-W75zW9thYP/view?usp=share_link",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1054156349568729139/1100161617326526606/icon.png"
        )
        emb2 = discord.Embed(
            title="Cessna Citation X by Laminar Research",
            colour=cfc,
            url="https://drive.google.com/file/d/1X4sShTh58rDucdeJQbX1VdkZtqvBXJIQ/view?usp=sharing",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1054156349568729139/1100161617666252930/Cessna_CitationX_icon11.png"
        )
        emb3 = discord.Embed(
            title="Cessna 172SP by Laminar Research",
            colour=cfc,
            url="https://drive.google.com/file/d/1Fh0B1MKJWW4aSo0uOe4AF2pj4orKfOSI/view?usp=sharing",
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1054156349568729139/1099739093551829022/Cessna_172SP_icon11.png"
        )
        embs = [embm, emb1, emb2, emb3]
        await ctx.respond(embeds=embs)


def setup(bot):
    bot.add_cog(VACommands(bot))
