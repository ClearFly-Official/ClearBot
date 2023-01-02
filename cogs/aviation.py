import discord
import os, requests, json, fitz, datetime
from discord import option
from airports import airports
from main import cfc, errorc

class AvCommands(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    av = discord.SlashCommandGroup(name="aviation", description="Commands related to airports, charts and similar.")
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

    @av.command(name="airport-diagram", description="Fetches the airport diagram of the provided airport.")
    @option("airport", description="The airport you want the diagram from.", autocomplete=get_airports)
    async def apd(self, ctx, airport):
        if airport[:4].upper().startswith(("K", "P", "0")):
            await ctx.defer()
            req = requests.get(f"https://api.aviationapi.com/v1/charts?apt={airport[:4].upper()}&group=2")
            load = json.loads(req.text)
            if load[airport[:4].upper()] == []:
                embed = discord.Embed(title="Error 404", description="Didn't found a diagram for {airport[:4].upper()}.", colour=errorc)
                await ctx.respond(embed=embed)
            else:
                url = load[airport[:4].upper()][0]['pdf_path']
                r = requests.get(url, stream=True)

                with open(f"images/apd.pdf", "wb") as f:
                    f.write(r.content)
                doc = fitz.open("images/apd.pdf")  # open document
                i = 0
                for page in doc:
                    pix = page.get_pixmap()  # render page to an image
                    pix.save(f"images/apd{i}.jpg")
                    i += 1
                embed = discord.Embed(title=f"{airport[:4].upper()}'s airport diagram:", colour=cfc)
                dfile = discord.File("images/apd0.jpg", filename="apd.jpg")
                embed.set_image(url="attachment://apd.jpg")
                await ctx.respond(embed=embed, file=dfile)
        else:
            embed = discord.Embed(title="Error 422", description="Only US airports are allowed as input.", colour=errorc)
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(AvCommands(bot=bot))