import discord
import aiohttp
import os, json, fitz
import aiofiles
from datetime import datetime
from discord import option
from discord.ext.pages import Page, Paginator
from discord.ext import commands
from airports import airports
from main import cfc, errorc


class AvCommands(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    av = discord.SlashCommandGroup(
        name="aviation",
        description="✈️ Commands related to aviation.",
    )

    async def get_airports(self, ctx: discord.AutocompleteContext):
        if ctx.value == "":
            return [
                "Start typing the name of an airport for results to appear(e.g. KJFK)"
            ]
        return [airport for airport in airports if airport.startswith(ctx.value.upper())]

    @commands.Cog.listener()
    async def on_ready(self):
        print("| Aviation cog loaded sucessfully")

    @av.command(name="metar", description="⛅️ Get the metar data of an airport.")
    @commands.cooldown(1, 10)
    @option(
        "airport",
        description="The airport you want the metar data of.",
        autocomplete=get_airports,
    )
    async def metar(self, ctx: discord.ApplicationContext, airport):
        await ctx.defer()
        hdr = {"X-API-Key": os.getenv("CWX_KEY")}
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                f"https://api.checkwx.com/metar/{airport[:4].upper()}/decoded",
                headers=hdr,
            ) as r:
                r.raise_for_status()
                resp = await r.json()

        class METARViewM(discord.ui.View):
            def __init__(self, bot):
                self.bot = bot
                super().__init__(timeout=60.0)
                
            async def on_timeout(self):
                await ctx.edit(view=self)
                
            @discord.ui.button(
                label="Change to Metric units", style=discord.ButtonStyle.primary
            )
            async def button_callback(self, button, interaction):
                if ctx.author == interaction.user:
                    time = str(json.dumps(resp["data"][0]["observed"]).replace('"', ""))
                    obstime = discord.utils.format_dt(
                        datetime.strptime(time+"+00:00", "%Y-%m-%dT%H:%M:%S%z"), "R"
                    )
                    airportn = json.dumps(resp["data"][0]["station"]["name"]).replace(
                        '"', ""
                    )
                    embed = discord.Embed(
                        title=f"Metar data for **{airportn}** from **{time}** ({obstime})",
                        color=cfc,
                    )
                    embed.add_field(
                        name="Raw Metar Data:",
                        value=f"""
```
{json.dumps(resp['data'][0]['raw_text']).replace('"', "")}
```
            """,
                    )
                    embed.add_field(
                        name="Translated Metar Data:",
                        value=f"""
Airport : **{json.dumps(resp['data'][0]['station']['name']).replace('"', "")}**(**{json.dumps(resp['data'][0]['icao']).replace('"', "")}**)
Barometer : **hPa {json.dumps(resp['data'][0]['barometer']['hpa'])}**
Clouds : **{json.dumps(resp['data'][0]['clouds'][0]['text']).replace('"', "")}**(**{json.dumps(resp['data'][0]['clouds'][0]['code']).replace('"', "")}**)
Temperature : **{json.dumps(resp['data'][0]['temperature'].get('celsius', 'N/A'))}C°**
Dewpoint : **{json.dumps(resp['data'][0]['dewpoint'].get('celsius', 'N/A'))}C°**
Elevation : **{json.dumps(resp['data'][0]['elevation']['meters']).replace('"', "")} Meters**
Flight Category : **{json.dumps(resp['data'][0]['flight_category']).replace('"', "")}**
Humidity : **{json.dumps(resp['data'][0]['humidity']['percent'])}%**
Visibility : **{json.dumps(resp['data'][0]['visibility']['meters']).replace('"', "")} Meters**
Winds : **{json.dumps(resp['data'][0].get('wind', {'degrees':'N/A'}).get('degrees'))}° at {json.dumps(resp['data'][0].get('wind', {'speed_kts': 'N/A'}).get('speed_kts', 'N/A'))} Knots**
            """,
                        inline=False,
                    )
                    await interaction.response.edit_message(
                        embed=embed, view=METARViewI(bot=self.bot)
                    )
                else:
                    await interaction.response.send_message(
                        "Run the command yourself to use it!", ephemeral=True
                    )

        class METARViewI(discord.ui.View):
            def __init__(self, bot):
                self.bot = bot
                super().__init__(timeout=120.0)

            async def on_timeout(self):
                await ctx.edit(view=self)
                
            @discord.ui.button(
                label="Change to Imperial units", style=discord.ButtonStyle.primary
            )
            async def button_callback(self, button, interaction):
                if ctx.author == interaction.user:
                    time = str(json.dumps(resp["data"][0]["observed"]).replace('"', ""))
                    obstime = discord.utils.format_dt(
                        datetime.strptime(time+"+00:00", "%Y-%m-%dT%H:%M:%S%z"), "R"
                    )
                    airportn = json.dumps(resp["data"][0]["station"]["name"]).replace(
                        '"', ""
                    )
                    embed = discord.Embed(
                        title=f"Metar data for **{airportn}** from **{time}** ({obstime})",
                        color=cfc,
                    )
                    embed.add_field(
                        name="Raw Metar Data:",
                        value=f"""
```
{json.dumps(resp['data'][0]['raw_text']).replace('"', "")}
```
            """,
                    )
                    embed.add_field(
                        name="Translated Metar Data:",
                        value=f"""
Airport : **{json.dumps(resp['data'][0]['station']['name']).replace('"', "")}**(**{json.dumps(resp['data'][0]['icao']).replace('"', "")}**)
Barometer : **Hg {json.dumps(resp['data'][0]['barometer']['hg'])}**
Clouds : **{json.dumps(resp['data'][0]['clouds'][0]['text']).replace('"', "")}**(**{json.dumps(resp['data'][0]['clouds'][0]['code']).replace('"', "")}**)
Temperature : **{json.dumps(resp['data'][0]['temperature'].get('fahrenheit', 'N/A')).replace('"', "")}F°**
Dewpoint : **{json.dumps(resp['data'][0]['dewpoint'].get('fahrenheit', 'N/A'))}F°**
Elevation : **{json.dumps(resp['data'][0]['elevation']['feet']).replace('"', "")} Feet**
Flight Category :**{json.dumps(resp['data'][0]['flight_category']).replace('"', "")}**
Humidity : **{json.dumps(resp['data'][0]['humidity']['percent'])}%**
Visibility : **{json.dumps(resp['data'][0]['visibility']['miles']).replace('"', "")} Miles**
Winds : **{json.dumps(resp['data'][0].get('wind', {'degrees':'N/A'}).get('degrees'))}° at {json.dumps(resp['data'][0].get('wind', {'speed_kts': 'N/A'}).get('speed_kts', 'N/A'))} Knots**
            """,
                        inline=False,
                    )
                    await interaction.response.edit_message(
                        embed=embed, view=METARViewM(bot=self.bot)
                    )
                else:
                    await interaction.response.send_message(
                        "Run the command yourself to use it!", ephemeral=True
                    )

        if resp["results"] == 1:
            time = str(json.dumps(resp["data"][0]["observed"]).replace('"', ""))
            obstime = discord.utils.format_dt(
                datetime.strptime(time+"+00:00", "%Y-%m-%dT%H:%M:%S%z"), "R"
            )
            airportn = json.dumps(resp["data"][0]["station"]["name"]).replace('"', "")
            embed = discord.Embed(
                title=f"Metar data for **{airportn}** from **{time}** ({obstime})",
                color=cfc,
            )
            embed.add_field(
                name="Raw Metar Data:",
                value=f"""
```
{json.dumps(resp['data'][0]['raw_text']).replace('"', "")}
```
            """,
            )
            embed.add_field(
                name="Translated Metar Data:",
                value=f"""
Airport : **{json.dumps(resp['data'][0]['station']['name']).replace('"', "")}**(**{json.dumps(resp['data'][0]['icao']).replace('"', "")}**)
Barometer : **hPa {json.dumps(resp['data'][0]['barometer']['hpa'])}**
Clouds : **{json.dumps(resp['data'][0]['clouds'][0]['text']).replace('"', "")}**(**{json.dumps(resp['data'][0]['clouds'][0]['code']).replace('"', "")}**)
Temperature : **{json.dumps(resp['data'][0]['temperature'].get('celsius', 'N/A'))}C°**
Dewpoint : **{json.dumps(resp['data'][0]['dewpoint'].get('celsius', 'N/A'))}C°**
Elevation : **{json.dumps(resp['data'][0]['elevation']['meters']).replace('"', "")} Meters**
Flight Category : **{json.dumps(resp['data'][0]['flight_category']).replace('"', "")}**
Humidity : **{json.dumps(resp['data'][0]['humidity']['percent'])}%**
Visibility : **{json.dumps(resp['data'][0]['visibility']['meters']).replace('"', "")} Meters**
Winds : **{json.dumps(resp['data'][0].get('wind', {'degrees':'N/A'}).get('degrees'))}° at {json.dumps(resp['data'][0].get('wind', {'speed_kts': 'N/A'}).get('speed_kts', 'N/A'))} Knots**
            """,
                inline=False,
            )
            await ctx.respond(embed=embed, view=METARViewI(bot=self.bot))
        else:
            embed = discord.Embed(
                title="Error 404!",
                description=f"Didn't found metar data for {airport[:4].upper()}.",
                color=errorc,
            )
            await ctx.respond(embed=embed)

    @av.command(name="charts", description="🗺️ Fetches charts of the provided airport.")
    @commands.cooldown(
    1, 20, commands.BucketType.user
    )
    @discord.option("airport", description="The airport you want charts from.", autocomplete=get_airports)
    @discord.option("chart", description="The chart type you want.",choices=['Airport Diagram', 'Approaches', 'Minimums'])
    async def chart(self, ctx, airport, chart):
        await ctx.defer()
        if chart == 'Approaches':
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://api.aviationapi.com/v1/charts?apt={airport[:4].upper()}&group=6") as r:
                    load = await r.json()
            if airport[:4].upper().startswith(("K", "P", "0")):
                if load[airport[:4].upper()] == []:
                    embed = discord.Embed(title="Error 404", description=f"Didn't found a diagram for {airport[:4].upper()}.", colour=errorc)
                    await ctx.respond(embed=embed)
                else:
                    url = load[airport[:4].upper()][0]['pdf_path']
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(url) as r:
                                i = 0
                                pages = [
                                ]
                    for chart in load[airport[:4].upper()]:
                        url = load[airport[:4].upper()][i]['pdf_path']
                        async with aiohttp.ClientSession() as cs:
                            async with cs.get(url) as r:
                                async with aiofiles.open(f"images/charts/chart{i}.pdf", "wb") as f:
                                    await f.write(await r.content.read())
                        doc = fitz.open(f"images/charts/chart{i}.pdf")
                        for page in doc:
                            pix = page.get_pixmap(dpi=150)
                            pix.save(f"images/charts/chart{i}.jpg")
                            i += 1
                    i = 0
                    for chart in load[airport[:4].upper()]:
                        dfile = discord.File(f"images/charts/chart{i}.jpg", filename=f"chart{i}.jpg")
                        pages.append(
                            Page(embeds=[discord.Embed(title=f"{load[airport[:4].upper()][i]['chart_name']} for {airport[:4].upper()}",description=f"[PDF link]({load[airport[:4].upper()][i]['pdf_path']})", colour=cfc)], files=[dfile])
                        )
                        pages[i].embeds[0].set_image(url=f"attachment://chart{i}.jpg")
                        i += 1
                    paginator = Paginator(pages=pages)
                    await paginator.respond(ctx.interaction)
            else:
                embed = discord.Embed(title="Error 422", description="Only US airports are allowed as input.", colour=errorc)
                await ctx.respond(embed=embed)
        if chart == 'Minimums':
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://api.aviationapi.com/v1/charts?apt={airport[:4].upper()}&group=3") as r:
                    load = await r.json()
            if airport[:4].upper().startswith(("K", "P", "0")):
                if load[airport[:4].upper()] == []:
                    embed = discord.Embed(title="Error 404", description=f"Didn't found a diagram for {airport[:4].upper()}.", colour=errorc)
                    await ctx.respond(embed=embed)
                else:
                    url = load[airport[:4].upper()][0]['pdf_path']
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(url) as r:
                                i = 0
                                pages = [
                                ]
                    for chart in load[airport[:4].upper()]:
                        url = load[airport[:4].upper()][i]['pdf_path']
                        async with aiohttp.ClientSession() as cs:
                            async with cs.get(url) as r:
                                async with aiofiles.open(f"images/charts/chart{i}.pdf", "wb") as f:
                                    await f.write(await r.content.read())
                        doc = fitz.open(f"images/charts/chart{i}.pdf")
                        for page in doc:
                            pix = page.get_pixmap(dpi=150)
                            pix.save(f"images/charts/chart{i}.jpg")
                            i += 1
                    i = 0
                    for chart in load[airport[:4].upper()]:
                        dfile = discord.File(f"images/charts/chart{i}.jpg", filename=f"chart{i}.jpg")
                        pages.append(
                            Page(embeds=[discord.Embed(title=f"{load[airport[:4].upper()][i]['chart_name']} for {airport[:4].upper()}",description=f"[PDF link]({load[airport[:4].upper()][i]['pdf_path']})", colour=cfc)], files=[dfile])
                        )
                        pages[i].embeds[0].set_image(url=f"attachment://chart{i}.jpg")
                        i += 1
                    paginator = Paginator(pages=pages)
                    await paginator.respond(ctx.interaction)
            else:
                embed = discord.Embed(title="Error 422", description="Only US airports are allowed as input.", colour=errorc)
                await ctx.respond(embed=embed)
        if chart == 'Airport Diagram':
            if airport[:4].upper().startswith(("K", "P", "0")):
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://api.aviationapi.com/v1/charts?apt={airport[:4].upper()}&group=2") as r:
                        load = await r.json()

                if load[airport[:4].upper()] == []:
                    embed = discord.Embed(title="Error 404", description=f"Didn't found a diagram for {airport[:4].upper()}.", colour=errorc)
                    await ctx.respond(embed=embed)
                else:
                    url = load[airport[:4].upper()][0]['pdf_path']
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(url) as r:
                            async with aiofiles.open(f"images/charts/apd.pdf", "wb") as f:
                                await f.write(await r.content.read())
                    doc = fitz.open("images/charts/apd.pdf")  # open document
                    i = 0
                    for page in doc:
                        pix = page.get_pixmap(dpi=150)  # render page to an image
                        pix.save(f"images/charts/apd{i}.jpg")
                        i += 1
                    embed = discord.Embed(title=f"{airport[:4].upper()}'s airport diagram:", colour=cfc)
                    dfile = discord.File("images/charts/apd0.jpg", filename="apd.jpg")
                    embed.set_image(url="attachment://apd.jpg")
                    await ctx.respond(embed=embed, file=dfile)
            else:
                embed = discord.Embed(title="Error 422", description="Only US airports are allowed as input.", colour=errorc)
                await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(AvCommands(bot=bot))
