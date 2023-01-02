import discord
import os, requests, json, fitz, datetime
from discord import option
from discord.ext.pages import Page, Paginator
from discord.ext import commands
from airports import airports
from main import cfc, errorc

class AvCommands(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    av = discord.SlashCommandGroup(name="aviation", description="Commands related to airports, images/charts and similar.")
    async def get_airports(self, ctx: discord.AutocompleteContext):
        return [airport for airport in airports if airport.startswith(ctx.value.upper())]

    @av.command(name="metar", description="Get the metar data of an airport.")
    @option("airport", description="The airport you want the metar data of.", autocomplete=get_airports)
    async def metar(self, ctx, airport):
        await ctx.defer()
        hdr = {"X-API-Key": os.getenv("CWX_KEY")}
        req = requests.get(f"https://api.checkwx.com/metar/{airport[:4].upper()}/decoded", headers=hdr)
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
Winds : **{json.dumps(resp['data'][0].get('wind', {'degrees':'N/A'}).get('degrees'))}° at {json.dumps(resp['data'][0].get('wind', {'speed_kts': 'N/A'}).get('speed_kts', 'N/A'))} Knots**
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
Winds : **{json.dumps(resp['data'][0].get('wind', {'degrees':'N/A'}).get('degrees'))}° at {json.dumps(resp['data'][0].get('wind', {'speed_kts': 'N/A'}).get('speed_kts', 'N/A'))} Knots**
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
Winds : **{json.dumps(resp['data'][0].get('wind', {'degrees':'N/A'}).get('degrees'))}° at {json.dumps(resp['data'][0].get('wind', {'speed_kts': 'N/A'}).get('speed_kts', 'N/A'))} Knots**
            """, inline=False)
            await ctx.respond(embed=embed, view=METARViewI(bot=self.bot))
        else:
            embed = discord.Embed(title="Error 404!", description=f"Didn't found metar data for {airport[:4].upper()}.", color=errorc)
            await ctx.respond(embed=embed)

    @av.command(name="images/charts", description="Fetches images/charts of the provided airport.")
    @commands.cooldown(
    1, 30, commands.BucketType.user
    )
    @discord.option("airport", description="The airport you want images/charts from.", autocomplete=get_airports)
    @discord.option("chart", description="The chart type you want.",choices=['Airport Diagram', 'Approaches', 'Minimums'])
    async def chart(self, ctx, airport, chart):
        if chart == 'Approaches':
            await ctx.defer()
            req = requests.get(f"https://api.aviationapi.com/v1/images/charts?apt={airport[:4].upper()}&group=6")
            load = json.loads(req.text)
            if airport[:4].upper().startswith(("K", "P", "0")):
                if load[airport[:4].upper()] == []:
                    embed = discord.Embed(title="Error 404", description=f"Didn't found a diagram for {airport[:4].upper()}.", colour=errorc)
                    await ctx.respond(embed=embed)
                else:
                    url = load[airport[:4].upper()][0]['pdf_path']
                    r = requests.get(url, stream=True)
                    i = 0
                    pages = [
                    ]
                    for chart in load[airport[:4].upper()]:
                        url = load[airport[:4].upper()][i]['pdf_path']
                        r = requests.get(url, stream=True)
                        with open(f"images/charts/chart{i}.pdf", "wb") as f:
                            f.write(r.content)
                        doc = fitz.open(f"images/charts/chart{i}.pdf")
                        for page in doc:
                            pix = page.get_pixmap()
                            pix.save(f"images/charts/chart{i}.jpg")
                            i += 1
                    i = 0
                    for chart in load[airport.upper()]:
                        dfile = discord.File(f"images/charts/chart{i}.jpg", filename=f"chart{i}.jpg")
                        pages.append(
                            Page(embeds=[discord.Embed(title=f"{load[airport[:4].upper()][i]['chart_name']} for {airport[:4].upper()}", colour=cfc)], files=[dfile])
                        )
                        pages[i].embeds[0].set_image(url=f"attachment://chart{i}.jpg")
                        i += 1
                    paginator = Paginator(pages=pages)
                    await paginator.respond(ctx.interaction)
            else:
                embed = discord.Embed(title="Error 422", description="Only US airports are allowed as input.", colour=errorc)
                await ctx.respond(embed=embed)
        if chart == 'Minimums':
            await ctx.defer()
            req = requests.get(f"https://api.aviationapi.com/v1/images/charts?apt={airport[:4].upper()}&group=3")
            load = json.loads(req.text)
            if airport[:4].upper().startswith(("K", "P", "0")):
                if load[airport[:4].upper()] == []:
                    embed = discord.Embed(title="Error 404", description=f"Didn't found a diagram for {airport[:4].upper()}.", colour=errorc)
                    await ctx.respond(embed=embed)
                else:
                    url = load[airport[:4].upper()][0]['pdf_path']
                    r = requests.get(url, stream=True)
                    i, a = 0,0
                    pages = [
                    ]
                    for chart in load[airport[:4].upper()]:
                        url = load[airport[:4].upper()][i]['pdf_path']
                        r = requests.get(url, stream=True)
                        with open(f"images/charts/chart{i}.pdf", "wb") as f:
                            f.write(r.content)
                        doc = fitz.open(f"images/charts/chart{i}.pdf")
                        i += 1
                        for page in doc:
                            pix = page.get_pixmap()
                            pix.save(f"images/charts/chart{a}.jpg")
                            a += 1
                    i = 0
                    a = 0
                    for chart in load[airport.upper()]:
                        dfile = discord.File(f"images/charts/chart{i}.jpg", filename=f"chart{i}.jpg")
                        pages.append(
                            Page(embeds=[discord.Embed(title=f"{load[airport[:4].upper()][i]['chart_name']} for {airport[:4].upper()}", colour=cfc)], files=[dfile])
                        )
                        pages[a].embeds[0].set_image(url=f"attachment://chart{i}.jpg")
                        i += 1
                        a += 1
                    paginator = Paginator(pages=pages)
                    await paginator.respond(ctx.interaction)
            else:
                embed = discord.Embed(title="Error 422", description="Only US airports are allowed as input.", colour=errorc)
                await ctx.respond(embed=embed)
        if chart == 'Airport Diagram':
            if airport[:4].upper().startswith(("K", "P", "0")):
                await ctx.defer()
                req = requests.get(f"https://api.aviationapi.com/v1/images/charts?apt={airport[:4].upper()}&group=2")
                load = json.loads(req.text)
                if load[airport[:4].upper()] == []:
                    embed = discord.Embed(title="Error 404", description=f"Didn't found a diagram for {airport[:4].upper()}.", colour=errorc)
                    await ctx.respond(embed=embed)
                else:
                    url = load[airport[:4].upper()][0]['pdf_path']
                    r = requests.get(url, stream=True)

                    with open(f"images/charts/apd.pdf", "wb") as f:
                        f.write(r.content)
                    doc = fitz.open("images/charts/apd.pdf")  # open document
                    i = 0
                    for page in doc:
                        pix = page.get_pixmap()  # render page to an image
                        pix.save(f"images/charts/apd{i}.jpg")
                        i += 1
                    embed = discord.Embed(title=f"{airport[:4].upper()}'s airport diagram:", colour=cfc)
                    dfile = discord.File("images/charts/apd0.jpg", filename="apd.jpg")
                    embed.set_image(url="attachment://apd.jpg")
                    await ctx.respond(embed=embed, file=dfile)
            else:
                embed = discord.Embed(title="Error 422", description="Only US airports are allowed as input.", colour=errorc)
                await ctx.respond(embed=embed)
        for i in os.listdir("images/charts"):
            os.remove(f"images/charts/{i}")

    @commands.Cog.listener()
    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error: discord.DiscordException
    ):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond("This command is currently on cooldown.", ephemeral=True)
        else:
            raise error

def setup(bot):
    bot.add_cog(AvCommands(bot=bot))