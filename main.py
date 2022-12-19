###################
#-Made by Matt3o0-#
###################

import discord#Py-cord
import os
import random
from dotenv import load_dotenv
from discord.ext import tasks
from datetime import datetime 
from discord.ext import commands

bot = discord.Bot(intents=discord.Intents.all())
va = bot.create_group(name="va-admin",description="Commands related to the ClearFly Virtual Airline")
admin = bot.create_group(name="admin2", description="Commands for admins")
load_dotenv()
bot_start_time = datetime.utcnow()
#cfc = 0x2681b4 #<- default color
#cfc = 0xcc8d0e # <- halloween color
cfc = 0x00771d # <- christmas color
errorc = 0xFF0000

@bot.listen()
async def on_ready():
        await bot.change_presence(activity=discord.Game(name="Starting up."),status=discord.Status.online)
        await bot.change_presence(activity=discord.Game(name="Starting up.."),status=discord.Status.online)
        await bot.change_presence(activity=discord.Game(name="Starting up..."),status=discord.Status.online)
        channel = bot.get_channel(1001405648828891187)
        now = discord.utils.format_dt(datetime.now())
        bot.add_view(RulesView())
        bot.add_view(FAQView())
        bot.add_view(AnnounceRoleView())
        bot.add_view(UpdateRoleView())
        bot.add_view(InfoB4training())
        if os.path.exists(".onpc"):
            embed = discord.Embed(title="I started up!", description=f"""
            Started bot up on {now}
            *Data save available*
            """,color=0x00FF00)
            await channel.send(embed=embed)
        else:
            embed=discord.Embed(title="I started up!", description=f"""
            Started bot up on {now}
            *Data save unavailable*
            """,color=0x00FF00)
            await channel.send(embed=embed)
        presence.start()
        statements=[
        "Give me Baby Boeing 😩",
        "Boeing > Airbus",
        "How are you doing?",
        "Use me please.",
        "How can I assist you today?",
        ]
        await bot.change_presence(activity=discord.Game(name=f"/help | {random.choice(statements)}"),status=discord.Status.online)
        print("The bot is ready for usage!")

@tasks.loop(minutes=5)
async def presence():
        statements=[
        "Give me Baby Boeing 😩",
        "Boeing > Airbus",
        "How are you doing?",
        "Use me please.",
        "How can I assist you today?",
        "BABY BOEINGGGG",
        "If it ain't Boeing, I'm not going.",
        "I'm tired",
        "Nuke airbus smh",
        "Boeing supremacy",
        "*Sends missile to Airbus hq*",
        "Wolfair is my daddy:)",
        "Deep™",
        "What ya looking at 🤨",
        ]
        await bot.change_presence(activity=discord.Game(name=f"/help | {random.choice(statements)}"),status=discord.Status.online)

class RulesView(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=None)

    @discord.ui.button(label="I have read and accept the rules", custom_id="rulebutton", style=discord.ButtonStyle.secondary, emoji="<:ClearFly_half_clear:1009117524677369866>")
    async def button_callback(self, button, interaction):
      guilds = bot.get_guild(965419296937365514)
      roles = guilds.get_role(1002200398905483285)
      if roles in interaction.user.roles:
        await interaction.response.send_message("You already accepted the rules!",ephemeral=True)
      else:
        author = interaction.user
        channel = bot.get_channel(1001405648828891187)
        pfp = author.avatar.url
        guild = bot.get_guild(965419296937365514)
        role = guild.get_role(1002200398905483285)
        embed = discord.Embed(title=f"{author} accepted the rules!", color=cfc)
        embed.set_thumbnail(url=pfp)
        await author.add_roles(role)
        await interaction.response.send_message("Rules accepted, have fun in the server!",ephemeral=True)
        await channel.send(embed=embed)

@admin.command(name="rules", descritpion="sends the rules(admin only)")
@commands.has_permissions(manage_channels=True)
async def rules(ctx):
  embed1 = discord.Embed(color=cfc)
  embed1.set_image(url="https://cdn.discordapp.com/attachments/1001845626956427265/1050885748439662612/CFRules.png")
  embed2 = discord.Embed(color=cfc, description="""
**1.** Don’t post any inappropriate content.

**2.** Use channels for their intended use.

**3.** Do not spam mention members.

**4.** Do not be overly political.

**5.** Use common sense.

**6.** Follow the [Discord TOS](https://discord.com/terms) and [Community Guidelines](https://discord.com/guidelines).

**7.** Use </report:1018970055972757506> to let us know about anyone breaking the rules.
""")
  await ctx.respond("Rules posted!",ephemeral=True)
  await ctx.send(embeds=[embed1, embed2],view=RulesView())

class FAQView(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=None)

    @discord.ui.button(label="I have read the FAQ", custom_id="faqbutton", style=discord.ButtonStyle.secondary, emoji="<:ClearFly_half_clear:1009117524677369866>")
    async def button_callback(self, button, interaction):
      author = interaction.user
      guild = bot.get_guild(965419296937365514)
      role = guild.get_role(1002932992534134814)
      await author.add_roles(role)
      await interaction.response.send_message("Thanks for reading the FAQ, now you can ask questions in the server!",ephemeral=True)

@admin.command(name="faq", descritpion="sends the faq(admin only)")
@commands.has_permissions(manage_channels=True)
async def faq(ctx):
  embed = discord.Embed(title="ClearFly FAQ", description="""
**Q: When will the Boeing 737-100 be released?**
A: When it’s finished.

**Q: Is the project dead?**
A: Nope! To see the latest updates, go to the 737 Updates channel.

**Q: Will there be a 3D cabin?**
A: Yes!

**Q: Will there be a custom FMC?**
A: Our current plan is to code VOR navigation only.
""", color=cfc)
  await ctx.respond("FAQ posted!",ephemeral=True)
  await ctx.send(embed=embed,view=FAQView())

class AnnounceRoleView(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=None)

    @discord.ui.button(custom_id="announcebutton", style=discord.ButtonStyle.secondary, emoji="📣")
    async def button_callback(self, button, interaction):
      author = interaction.user
      guild = bot.get_guild(965419296937365514)
      role = guild.get_role(965689409364197467)
      if role in author.roles:
        author = interaction.user
        guild = bot.get_guild(965419296937365514)
        role = guild.get_role(965689409364197467)
        await author.remove_roles(role)
        await interaction.response.send_message("You won't get mentioned anymore for announcements.",ephemeral=True)
      else:
        author = interaction.user
        guild = bot.get_guild(965419296937365514)
        role = guild.get_role(965689409364197467)
        await author.add_roles(role)
        await interaction.response.send_message("You will now get mentioned for announcments!",ephemeral=True)


class UpdateRoleView(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=None)

    @discord.ui.button(custom_id="updatebutton", style=discord.ButtonStyle.secondary, emoji="🛠")
    async def button_callback(self, button, interaction):
      author = interaction.user
      guild = bot.get_guild(965419296937365514)
      role = guild.get_role(965688527109107712)
      if role in author.roles:
        author = interaction.user
        guild = bot.get_guild(965419296937365514)
        role = guild.get_role(965688527109107712)
        await author.remove_roles(role)
        await interaction.response.send_message("You won't get mentioned for updates anymore.",ephemeral=True)
      else:
        author = interaction.user
        guild = bot.get_guild(965419296937365514)
        role = guild.get_role(965688527109107712)
        await author.add_roles(role)
        await interaction.response.send_message("You will now get mentioned for updates!",ephemeral=True)
@admin.command(name="buttonroles", descritpion="sends the button roles(admin only)")
@commands.has_permissions(manage_channels=True)
async def buttonroles(ctx):
  embed = discord.Embed(title="Announcement Pings", description="Click on 📣 for announcement pings.\n*(click again to remove.)*", color=cfc)
  emb = discord.Embed(title="Update Pings", description="Click on 🛠 for update pings.\n*(click again to remove.)*", color=cfc)
  await ctx.respond("Button roles posted!",ephemeral=True)
  await ctx.send(embed=embed,view=AnnounceRoleView())
  await ctx.send(embed=emb,view=UpdateRoleView())

class InfoB4training(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(label="Continue to flight training", style=discord.ButtonStyle.green, custom_id="vastudent")
  async def first_button_callback(self, button, interaction):
    author = interaction.user
    guild = bot.get_guild(965419296937365514)
    role = guild.get_role(1040918463763468369)
    if role in author.roles:
      author = interaction.user
      guild = bot.get_guild(965419296937365514)
      role = guild.get_role(1040918463763468369)
      await author.remove_roles(role)
      await interaction.response.send_message("You are no longer a student in the ClearFly VA.",ephemeral=True)
    else:
      author = interaction.user
      guild = bot.get_guild(965419296937365514)
      role = guild.get_role(1040918463763468369)
      await author.add_roles(role)
      await interaction.response.send_message("You are now part of the ClearFly VA, get ready for some training!",ephemeral=True)
      channel = bot.get_channel(1038062843808972850)
      await channel.send(f"{interaction.user.mention} continue here, run </va training:1016059999056826479> and input your desired destination and origin.")


@va.command(name="setup", description="Sends the required message.")
@commands.has_role(965422406036488282)
async def vasetup(ctx):
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
  channel1 = bot.get_channel(1040927466975404054)
  channel2 = bot.get_channel(1041057335449227314)
  await channel1.send(embed=embed, view=InfoB4training
())
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


cogs = [
    "listeners",
    "dev",
    "admin",
    "fun",
    "level",
    "utility",
    "va"
]
for cog in cogs:
    bot.load_extension(f"cogs.{cog}")
  
bot.run(os.getenv('TOKEN'))