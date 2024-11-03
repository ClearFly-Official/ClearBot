import re
import discord
import aiohttp
import io
import os, json, fitz
import datetime
from discord import option
from discord.ext.pages import Page, Paginator
from discord.ext import commands
from main import ClearBot, get_airports

CLD_COVERS = {
    "CLR" : "Clear",
    "BKN": "Broken",
    "FEW": "Few",
    "SCT": "Scattered",
    "OVC" : "Overcast",
    "N/A": "N/A"
}

def return_numbers(string: str) -> int:
    return int(re.sub(r"\D", "", string))


def calculate_active_runways(
    runways: list[tuple[str, str]], wind_degree: int
) -> list[str]:
    rwy_headings = []
    for runway in runways:
        rwy_headings.append(int(runway[0])*10)
        rwy_headings.append(int(runway[1])*10)
    active_runways = []
    offsets = []
    for runway in rwy_headings:
        offset = abs(wind_degree - runway)
        if offset <= 90:
            offsets.append((runway, offset))
        
    offsets = sorted(offsets, key=lambda x: x[1])
    return [str(int(rwy[0]/10)) for rwy in offsets]

class AvCommands(discord.Cog):
    def __init__(self, bot: ClearBot):
        self.bot = bot

    av = discord.SlashCommandGroup(
        name="aviation", description="✈️ Commands related to aviation."
    )
    airport = av.create_subgroup(
        name="airport", description="🛬 Commands related to airports."
    )

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            "\033[34m|\033[0m \033[96;1mAviation\033[0;36m cog loaded sucessfully\033[0m"
        )

    @airport.command(name="metar", description="⛅️ Get the METAR data of an airport.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @option(
        "airport",
        description="The airport you want the metar data of.",
        autocomplete=get_airports,
    )
    async def metar(self, ctx: discord.ApplicationContext, airport):
        await ctx.defer()
        icao = airport[:4].upper()
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://aviationweather.gov/api/data/metar?ids={icao}&format=json&taf=false") as resp:
                data = await resp.json()
        
        if len(data) == 0:
            embed = discord.Embed(title="METAR unavailable", 
                                  description="The given airport might not have reporting equipment, or it simply doesn't exist.",
                                  color=self.bot.color(1))
            await ctx.respond(embed=embed)
            return
        else:
            data = data[0]

        na = lambda x: data.get(x, "N/A")
        altim_unit = "hPa"
        if data.get("altim", 0) > 1100:
            altim_unit = "inHg"
        wdir = str(na('wdir'))
        if wdir == "VRB":
            wdir = "Variable"
        else:
            wdir += "°"

        embed = discord.Embed(title=data.get("name", airport), color=self.bot.color())
        embed.description = f"Observed <t:{data.get('obsTime', 0)}:R> (<t:{data.get('obsTime', 0)}:f>)"
        embed.add_field(name="Raw", value=f"```{data.get('rawOb', f'{icao} //')}```", inline=False,)
        embed.add_field(name="Weather (Decoded)", inline=False, value=f"""
Winds:         **{na('wspd')}** kts at **{na('wdir')}**
Visibility:    **{na('visib')}** mi
Temperature:   **{na('temp')}** °C
Dew point:     **{na('dewp')}** °C
{'Altimeter' if altim_unit == 'inHg' else 'QNH'}:     **{na('altim')}** {altim_unit}
""")
        cloud_str = ""
        for cld in data.get("clouds", []):
            base = cld.get('base')
            cover = CLD_COVERS.get(cld.get('cover', 'N/A'), cld.get('cover', 'N/A'))
            if base:
                cloud_str += f"**{cover}** at **{base}** ft\n"
            else:
                cloud_str += f"**{cover}**\n"
        embed.add_field(name="Clouds (Decoded)", inline=False, value=cloud_str)
        embed.set_footer(text="Source: NOAA/aviationweather.gov")

        await ctx.respond(embed=embed)

    @airport.command(
        name="charts", description="🗺️ Fetches charts of the provided airport."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @discord.option(
        "airport",
        description="The airport you want charts from.",
        autocomplete=get_airports,
    )
    @discord.option(
        "chart",
        description="The chart type you want.",
        choices=["Airport Diagram", "Approaches", "Minimums"],
    )
    async def chart(self, ctx, airport, chart):
        await ctx.defer()
        if chart == "Approaches":
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                    f"https://api.aviationapi.com/v1/charts?apt={airport[:4].upper()}&group=6"
                ) as r:
                    load = await r.json()
            if airport[:4].upper().startswith(("K", "P", "0")):
                if load[airport[:4].upper()] == []:
                    embed = discord.Embed(
                        title="Error 404",
                        description=f"Didn't found a diagram for {airport[:4].upper()}.",
                        colour=self.bot.color(1),
                    )
                    await ctx.respond(embed=embed)
                else:
                    url = load[airport[:4].upper()][0]["pdf_path"]
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(url) as r:
                            i = 0
                            pages = []
                    for chart in load[airport[:4].upper()]:
                        url = load[airport[:4].upper()][i]["pdf_path"]
                        async with aiohttp.ClientSession() as cs:
                            async with cs.get(url) as r:
                                chart_data = await r.content.read()
                        chart_file = io.BytesIO(chart_data)
                        doc = fitz.open("pdf", chart_file)  # type: ignore
                        for page in doc:
                            pix = page.get_pixmap(dpi=150)
                            img_data = pix.pil_tobytes(format="JPEG", optimize=True)
                            chart_img = io.BytesIO(img_data)
                            dfile = discord.File(chart_img, filename=f"chart{i}.jpg")
                            pages.append(
                                Page(
                                    embeds=[
                                        discord.Embed(
                                            title=f"{load[airport[:4].upper()][i]['chart_name']} for {airport[:4].upper()}",
                                            description=f"[PDF link]({load[airport[:4].upper()][i]['pdf_path']})",
                                            colour=self.bot.color(),
                                        )
                                    ],
                                    files=[dfile],
                                )
                            )
                            pages[i].embeds[0].set_image(
                                url=f"attachment://chart{i}.jpg"
                            )
                            i += 1

                    paginator = Paginator(
                        pages=pages,
                        use_default_buttons=False,
                        custom_buttons=self.bot.paginator_buttons,
                    )
                    await paginator.respond(ctx.interaction)

            else:
                embed = discord.Embed(
                    title="Invalid airport code",
                    description="Only US airports are allowed as input.",
                    colour=self.bot.color(1),
                )
                await ctx.respond(embed=embed)
        if chart == "Minimums":
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                    f"https://api.aviationapi.com/v1/charts?apt={airport[:4].upper()}&group=3"
                ) as r:
                    load = await r.json()
            if airport[:4].upper().startswith(("K", "P", "0")):
                if load[airport[:4].upper()] == []:
                    embed = discord.Embed(
                        title="Error 404",
                        description=f"Didn't found a diagram for {airport[:4].upper()}.",
                        colour=self.bot.color(1),
                    )
                    await ctx.respond(embed=embed)
                else:
                    url = load[airport[:4].upper()][0]["pdf_path"]
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(url) as r:
                            i = 0
                            pages = []
                    for j, chart in enumerate(load[airport[:4].upper()]):
                        url = load[airport[:4].upper()][j]["pdf_path"]
                        async with aiohttp.ClientSession() as cs:
                            async with cs.get(url) as r:
                                chart_data = await r.content.read()
                        chart_file = io.BytesIO(chart_data)
                        doc = fitz.open("pdf", chart_file)  # type: ignore
                        for page in doc:
                            pix = page.get_pixmap(dpi=150)
                            img_data = pix.pil_tobytes(format="JPEG", optimize=True)
                            chart_img = io.BytesIO(img_data)
                            dfile = discord.File(chart_img, filename=f"chart{i}.jpg")
                            pages.append(
                                Page(
                                    embeds=[
                                        discord.Embed(
                                            title=f"{load[airport[:4].upper()][j]['chart_name']} for {airport[:4].upper()}",
                                            description=f"[PDF link]({load[airport[:4].upper()][j]['pdf_path']})",
                                            colour=self.bot.color(),
                                        )
                                    ],
                                    files=[dfile],
                                )
                            )
                            pages[i].embeds[0].set_image(
                                url=f"attachment://chart{i}.jpg"
                            )
                            i += 1

                    paginator = Paginator(
                        pages=pages,
                        use_default_buttons=False,
                        custom_buttons=self.bot.paginator_buttons,
                    )
                    await paginator.respond(ctx.interaction)
            else:
                embed = discord.Embed(
                    title="Invalid airport code",
                    description="Only US airports are allowed as input.",
                    colour=self.bot.color(1),
                )
                await ctx.respond(embed=embed)
        if chart == "Airport Diagram":
            if airport[:4].upper().startswith(("K", "P", "0")):
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(
                        f"https://api.aviationapi.com/v1/charts?apt={airport[:4].upper()}&group=2"
                    ) as r:
                        load = await r.json()

                if load[airport[:4].upper()] == []:
                    embed = discord.Embed(
                        title="Error 404",
                        description=f"Didn't found a diagram for {airport[:4].upper()}.",
                        colour=self.bot.color(1),
                    )
                    await ctx.respond(embed=embed)
                else:
                    url = load[airport[:4].upper()][0]["pdf_path"]
                    dfile = None
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(url) as r:
                            chart_data = await r.content.read()
                            chart_file = io.BytesIO(chart_data)
                            doc = fitz.open("pdf", chart_file)  # type: ignore
                    for i, page in enumerate(doc):
                        pix = page.get_pixmap(dpi=150)
                        img_data = pix.pil_tobytes(format="JPEG", optimize=True)
                        chart_img = io.BytesIO(img_data)
                        dfile = discord.File(chart_img, filename=f"apd.jpg")
                    embed = discord.Embed(
                        title=f"{airport[:4].upper()}'s airport diagram:",
                        colour=self.bot.color(),
                    )
                    embed.set_image(url="attachment://apd.jpg")
                    await ctx.respond(embed=embed, file=dfile)
            else:
                embed = discord.Embed(
                    title="Invalid airport code",
                    description="Only US airports are allowed as input.",
                    colour=self.bot.color(1),
                )
                await ctx.respond(embed=embed)

    @airport.command(name="info", description="ℹ️ Fetch info about an airport.")
    @discord.option(
        name="airport",
        description="The airport you want to know information about.",
        autocomplete=get_airports,
    )
    async def airport_info(self, ctx: discord.ApplicationContext, airport: str):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                f"https://airportdb.io/api/v1/airport/{airport[:4].upper()}?apiToken={os.getenv('ADB_TOKEN')}"
            ) as resp:
                if resp.status == 200:
                    json_resp = await resp.json()
                else:
                    embed = discord.Embed(
                        title="No airport information found.",
                        colour=self.bot.color(1),
                    )
                    await ctx.respond(embed=embed)
                    return
        site_link = json_resp.get("home_link")
        wiki_link = json_resp.get("wikipedia_link")
        view = discord.ui.View()

        if self.bot.is_valid_url(site_link):
            button = discord.ui.Button(label="Open airport site", url=site_link)
            view.add_item(button)
        else:
            button = discord.ui.Button(
                label="Open airport site", url="https://matt3o0.is-a.dev", disabled=True
            )
            view.add_item(button)

        if self.bot.is_valid_url(wiki_link):
            button = discord.ui.Button(label="Open Wikipedia page", url=wiki_link)
            view.add_item(button)
        else:
            button = discord.ui.Button(
                label="Open Wikipedia page",
                url="https://matt3o0.is-a.dev",
                disabled=True,
            )
            view.add_item(button)

        iata = "N/A" if json_resp.get("iata_code") == "" else json_resp.get("iata_code")

        if json_resp.get("continent", "N/A") == "NA":
            continent = "North America"
        elif json_resp.get("continent", "N/A") == "EU":
            continent = "Europe"
        elif json_resp.get("continent", "N/A") == "AS":
            continent = "Asia"
        elif json_resp.get("continent", "N/A") == "OC":
            continent = "Oceania"
        elif json_resp.get("continent", "N/A") == "SA":
            continent = "South America"
        elif json_resp.get("continent", "N/A") == "AN":
            continent = "Antartica"
        elif json_resp.get("continent", "N/A") == "AF":
            continent = "Africa"
        else:
            continent = json_resp.get("continent", "N/A")

        pages = []
        elevation = json_resp.get("elevation_ft")

        gen_embed = discord.Embed(
            title=f"Information about '{airport}'",
            description=f"""
ICAO: **{json_resp.get('icao_code', 'N/A')}**
IATA: **{iata}**
Type: **{json_resp.get('type', 'N/A').replace('_', ' ').title()}**
Name: **{json_resp.get('name', 'N/A')}**
Elevation: **{elevation if elevation else 'N/A'}**ft
Continent: **{continent}**
Country Code: **{json_resp.get('iso_country', 'N/A')}**
Region Code: **{json_resp.get('iso_region', 'N/A')}**
Municipality: **{json_resp.get('municipality', 'N/A')}**
        """,
            color=self.bot.color(),
        )
        pages.append(Page(embeds=[gen_embed], custom_view=view))

        if json_resp.get("freqs"):
            freq_emb = discord.Embed(title="Frequencies", color=self.bot.color())

            for freq in json_resp.get("freqs"):
                freq_emb.add_field(
                    name=freq.get("description", "N/A"),
                    value=f"Type: **{freq.get('type', 'N/A')}**\nFrequency: **{freq.get('frequency_mhz')}**MHz",
                )

            pages.append(Page(embeds=[freq_emb]))

        if json_resp.get("runways"):
            for rwy in json_resp.get("runways"):
                embed = discord.Embed(color=self.bot.color())
                le_ident = rwy.get("le_ident", "N/A")
                le_ils = rwy.get("le_ils", {"e": 1})

                he_ident = rwy.get("he_ident", "N/A")
                he_ils = rwy.get("he_ils", {"e": 1})

                le_deg = rwy.get("le_heading_degT", "N/A")
                he_deg = rwy.get("he_heading_degT", "N/A")

                surf = ""
                match rwy.get("surface", "N/A").lower():
                    # Abbrevations sourced from https://en.wikipedia.org/wiki/Runway
                    case "asp":
                        surf = "asphalt"
                    case "bit":
                        surf = "bituminous asphalt"
                    case "bri":
                        surf = "bricks"
                    case "cla":
                        surf = "clay"
                    case "con":
                        surf = "contrete"
                    case "conc-g":
                        surf = "concrete - grooved"
                    case _:
                        surf = rwy.get("surface", "N/A")

                dim = ["N/A", "N/A"]

                if rwy.get("length_ft"):
                    dim[0] = rwy.get("length_ft")

                if rwy.get("width_ft"):
                    dim[1] = rwy.get("width_ft")

                elev = ["N/A", "N/A"]

                if rwy.get("le_elevation_ft"):
                    elev[0] = rwy.get("le_elevation_ft")

                if rwy.get("he_elevation_ft"):
                    elev[1] = rwy.get("he_elevation_ft")

                embed.description = f"""
## {'~~' if int(rwy.get('closed')) else ''}{'💡' if rwy.get('lighted') else '🌌'} Runway {le_ident}{f'*({le_deg}°)*' if le_deg else ''}/{he_ident}{f'*({he_deg}°)*' if he_deg else ''}{'~~' if int(rwy.get('closed')) else ''}
**{dim[0]}**ft x **{dim[1]}**ft
Surface: **{surf.title()}**
Elevation: **{elev[0]}**ft / **{elev[1]}**ft
            """

                if le_ils.get("freq") and he_ils.get("freq"):
                    embed.description += f"""
### ILS
{le_ident}: **{le_ils.get('freq')}**MHz (course **{le_ils.get('course')}**°)
{he_ident}: **{he_ils.get('freq')}**MHz (course **{he_ils.get('course')}**°)
"""
                else:
                    embed.description += "\n### *No ILS available*"

                pages.append(Page(embeds=[embed]))

        paginator = Paginator(
            pages=pages,
            use_default_buttons=False,
            custom_buttons=self.bot.paginator_buttons,
        )

        await paginator.respond(ctx.interaction)

    @airport.command(
        name="active_runways",
        description="🎬 Make an assumption of the active runways of an airport.",
    )
    @discord.option(
        name="airport",
        description="The airport you want to know the active runways of",
        autocomplete=get_airports,
    )
    async def active_runways(self, ctx: discord.ApplicationContext, airport: str):
        await ctx.defer()
        icao = airport[:4].upper()
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://aviationweather.gov/api/data/metar?ids={icao}&format=json&taf=false") as resp:
                metar_data = await resp.json()
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                f"https://airportdb.io/api/v1/airport/{icao}?apiToken={os.getenv('ADB_TOKEN')}"
            ) as resp:
                if resp.status == 200 and len(metar_data) > 0:
                    json_resp = await resp.json()
                    metar_data = metar_data[0]

                    runways = []
                    for i, runway in enumerate(json_resp["runways"]):
                        if runway["closed"] == "0":
                            runways.append(
                                (
                                    json_resp["runways"][i]["le_ident"],
                                    json_resp["runways"][i]["he_ident"],
                                )
                            )
                        
                    wdir = metar_data.get("wdir", "N/A")

                    if wdir == "N/A":
                        embed = discord.Embed(
                            title="No wind data found",
                            description="Wind data is required to make a prediction on active runways at the given airport.",
                            colour=self.bot.color(1),
                        )
                        await ctx.respond(embed=embed)
                        return
                    
                    if wdir == "VRB":
                        embed = discord.Embed(
                            title="Wind is variable",
                            description="""
Variable wind direction is reported at the given airport, making it impossible to predict active runways.
Try listening to the ATIS/AWOS of the airport if available.
                            """,
                            colour=self.bot.color(1),
                        )
                        await ctx.respond(embed=embed)
                        return
                    ac_runways = calculate_active_runways(runways, int(wdir))

                    ac_runways = [
                        f"**{i}**: {rwy}" for i, rwy in enumerate(ac_runways, 1)
                    ]
                    embed = discord.Embed(
                        title=f"Active runways at {airport[:4].upper()}",
                        description="\n".join(ac_runways),
                        colour=self.bot.color(),
                    ).set_footer(text="Not for real-world use.")
                    await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Airport not found", colour=self.bot.color(1)
                    )
                    await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(AvCommands(bot=bot))
