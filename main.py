########################
#-Made by Matt3o0#4000-#
########################
import discord
import os
import platform
import pyfiglet
import requests
import random
from dotenv import load_dotenv
from time import sleep
from datetime import datetime
from random import choices
from math import sqrt
from discord.ext import commands, tasks
from discord.ext.commands import (BadArgument, Bot, BucketType,
                                  clean_content, command, cooldown)
from discord.ui import Button, View
from discord.utils import get
from discord import option


load_dotenv()

cfc = 0x4f93cf
errorc = 0xFF0000
intents = discord.Intents.all()
intents.members = True
intents.reactions = True

bot = discord.Bot(command_prefix=',', intents=intents)
fun = bot.create_group(name="fun",description="Commands that are supposed to be fun")
va = bot.create_group(name="va",description="Commands related to the ClearFly Virtual Airline")
admin = bot.create_group(name="admin", description="Commands for admins")
utility = bot.create_group(name="utility", description="Commands related to utility")
math = utility.create_subgroup(name="math", description="Commands related to math")


@bot.listen()
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Starting up."),status=discord.Status.online)
    sleep(0.5)
    await bot.change_presence(activity=discord.Game(name="Starting up.."),status=discord.Status.online)
    sleep(0.5)
    await bot.change_presence(activity=discord.Game(name="Starting up..."),status=discord.Status.online)
    channel=bot.get_channel(1001405648828891187)
    embed=discord.Embed(title="I started up!", description="Started bot up:\n   Defined Bot\nSuccesfully added views\nInitialised presence",color=0x00FF00)
    await channel.send(embed=embed)
    bot.add_view(MyView())
    bot.add_view(MyView2())
    bot.add_view(MyView3())
    bot.add_view(MyView4())
    bot.add_view(MyView5())
    presence.start()
    statements=[
      "Give me Baby Boeing 😩",
      "Boeing > Airbus",
      "How are you doing?",
      "Use me please.",
      "How can I assist you today?"
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
      "If it ain't Boeing, I'm not going."
    ]
    await bot.change_presence(activity=discord.Game(name=f"/help | {random.choice(statements)}"),status=discord.Status.online)


@bot.listen()
async def on_member_join(member):
    channel = bot.get_channel(965600413376200726)
    emb = discord.Embed(title=f"Welcome to ClearFly!", description=f"Hey there, {member.mention}! Be sure to read the <#1002194493304479784> to become a member and gain full access to the server! Thanks for joining!", color = 0x57a4cd)
    await channel.send(embed=emb)

@bot.listen()
async def on_member_remove(member):
  channel = bot.get_channel(1001405648828891187)
  emb = discord.Embed(title=f"{member} left.", color=cfc)
  pfp = member.avatar.url
  emb.set_thumbnail(url=pfp)
  await channel.send(embed=emb)

@bot.listen()
async def on_message_delete(message):
  channel = bot.get_channel(1001405648828891187)
  msgdel = message.clean_content
  msgatr = message.author.mention
  msgcnl = message.channel.mention
  pfp = message.author.avatar.url
  emb = discord.Embed(title="**Message Deleted:**", color=0x4f93cf)
  emb.add_field(name="Content:", value=f"{msgdel}", inline = False)
  emb.add_field(name="Author:", value=f"{msgatr}", inline = True)
  emb.add_field(name="Channel:", value=f"{msgcnl}", inline = True)
  emb.set_thumbnail(url=pfp)
  await channel.send(embed=emb)

@bot.listen()
async def on_message_edit(before, after):
  if before.author.bot == False:
    channel = bot.get_channel(1001405648828891187)
    msgeditb = before.clean_content
    msgedita = after.clean_content
    msgatr = before.author.mention
    msgcnl = before.channel.mention
    pfp = before.author.avatar.url
    emb = discord.Embed(title="**Message Edited:**", color=0x4f93cf)
    emb.add_field(name="Content before:", value=f"{msgeditb}", inline = False)
    emb.add_field(name="Content after:", value=f"{msgedita}", inline = False)
    emb.add_field(name="Author:", value=f"{msgatr}", inline = True)
    emb.add_field(name="Channel:", value=f"{msgcnl}", inline = True)
    emb.set_thumbnail(url=pfp)
    await channel.send(embed=emb)
  else:
    pass



@bot.slash_command(name="report", description="Need help? Use this command to contact the admins!")
@option("subject",description="What is your report about?",choices=["Misbehaving User", "Spam", "Hacked/Compromised Account", "Raid"])
@option("priority", description="The priority level of the report", choices=["low", "medium", "high"])
@option("user", description="The user involved(if more than one mention in comments unless raid)", required=False)
@option("comments", description="Anything else to say about the report?", required=False)
async def report(ctx, subject ,priority ,user: discord.Member, comments):
  await ctx.respond("Sending report.", ephemeral=True)
  channel=bot.get_channel(965655791468183612)
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
    await ctx.edit(content="Sending report..")
    sleep(0.1)
    await ctx.edit(content="Sending report...")
    await ctx.edit(content=None, embed=confirmembed)
    await channel.send("Low priority report", embed=embed)
  if priority == "medium":
    embed.add_field(name="Subject:", value=subject)
    embed.add_field(name="Involved User:", value=user)
    embed.add_field(name="Comments *if any*:", value=f"""
    ```
    {comments}
    ```
    """, inline=False)
    await ctx.edit(content="Sending report..")
    sleep(0.1)
    await ctx.edit(content="Sending report...")
    await ctx.edit(content=None, embed=confirmembed)
    await channel.send("<@&1006725140933001246> Medium priority report", embed=embed)
  if priority == "high":
    embed.add_field(name="Subject:", value=subject)
    embed.add_field(name="Involved User:", value=user)
    embed.add_field(name="Comments *if any*:", value=f"""
    ```
    {comments}
    ```
    """, inline=False)
    await ctx.edit(content="Sending report..")
    sleep(0.1)
    await ctx.edit(content="Sending report...")
    await ctx.edit(content=None, embed=confirmembed)
    await channel.send("<@&1006725140933001246> ATTENTION ALL ADMINS", embed=embed)
    await channel.send("<@&1006725140933001246> ^ THIS IS A HIGH PRIORITY REPORT")

@admin.command(name="echo",description="Send a message as the bot.(Admin only)")
@commands.has_permissions(manage_channels=True)
async def echo(ctx, text: str):
    await ctx.respond('posted your message!',ephemeral  = True)
    await ctx.channel.send(text)
    pfp = ctx.author.avatar.url
    channel = bot.get_channel(1001405648828891187)
    emb = discord.Embed(title=f"{ctx.author} used echo:", description=text, color = 0x4f93cf)
    emb.set_thumbnail(url=pfp)
    await channel.send(embed=emb)
    print(ctx.author, "used echo:", text)

@admin.command(name="embed",description="Send an embed as the bot.(Admin only)")
@commands.has_permissions(manage_channels=True)
async def embed(ctx, title: str, description: str):
    await ctx.respond('posted your embed!',ephemeral  = True)
    emb = discord.Embed(title=title, description=description, color=0x4f93cf)
    await ctx.channel.send(embed=emb)
    pfp = ctx.author.avatar.url
    channel2 = bot.get_channel(1001405648828891187)
    embed = discord.Embed(title=f"{ctx.author} used embed:", color = 0x4f93cf)
    embed.add_field(
        name="Title",
        value=f"""
```
{title}
```
            """
      )
    embed.add_field(
            name="Description",
            value=f"""
```
{description}
```
            """
      , inline = False)
    embed.set_thumbnail(url=pfp)
    await channel2.send(embed=embed)

@bot.command(name='the-team', description='Shows The ClearFly Team!')
async def team(ctx):
  emb = discord.Embed(title="**The ClearFly Team:**",color=cfc)
  logo = "https://cdn.discordapp.com/attachments/927609657655177238/992887468410024026/ClearFly_Logo.png"
  emb.add_field(name="WolfAir",value="Founder & Modeler",inline=False)
  emb.add_field(name="Matt3o0",value="Bot Creator & Admin",inline=False)
  emb.add_field(name="DJ",value="Admin",inline=False)
  emb.set_thumbnail(url=logo)
  await ctx.respond(embed=emb)

@utility.command(name="avatar",description="Shows your avatar.")
async def avatar(ctx, user: discord.Member = None):
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

@fun.command(name="ascii",description="Convert texts into ascii characters.")
async def ascii(ctx, text):
  try:
    ascii = pyfiglet.figlet_format(text)
    await ctx.respond(f"```{ascii}```")
  except Exception as e:
    await ctx.respond(f'Error:\n{e}', ephemeral  = True)

@utility.command(name="who-is", description="Fetches a user profile")
async def whois(ctx, user: discord.Member = None):
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
    sleep(1)
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
    sleep(1)
    await ctx.respond(embed=embed)


@utility.command(name="github", description="Shows the bot's GitHub repository.")
async def github(ctx):
  emb = discord.Embed(title="GitHub:", description="[Here's the repository!](https://github.com/duvbolone/ClearBot)",color=cfc)
  await ctx.respond(embed=emb)

@fun.command(name="8ball", description="Ask the bot some questions!")
async def test(ctx, question):
  answers = [
    "No.",
    "Yes.",
    "Maybe.",
    "Never.",
    "Ok",
    "Uhm ok...",
    "For legal purposes, I can't respond to that question",
    "No thank you.",
    "You're joking right?",
    "I'm certain.",
    "I don't think so...",
    "Ask Google, don't bother me.|| Not Bing, I dare you.||",
    "Go to sleep, you're tired.",
    "I'm not qualified to give medical advice, sorry.",
    "Ask again later.",
    "What?",
    "Haha, no.",
    "I'd go with yes",
    "Sure",
    "Yeah",
    "I'm concerned.",
    "Really good question to be honest, I still have no clue.",
    "WolfAir probably knows.",
    "A bit suspicious<:susge:965624336956407838>.",
    "Eh, probably not.",
    "Respectfully, shut up."
  ]
  embed = discord.Embed(title=f'{question}:', description=f'{random.choice(answers)}', color=cfc)
  await ctx.respond(embed=embed)

@admin.command(name="spam", description="Spam the channel to oblivion.")
@commands.has_permissions(manage_channels=True)
async def spam(ctx, text ,amount: int):
  channel = bot.get_channel(1001405648828891187)
  user = ctx.author
  if amount > 100:
    await ctx.respond("Sorry, but that too much.", ephemeral=True)
    embed = discord.Embed(title=f"**{user}** tried to spam `{ctx.channel}` **{amount} times** with the following text but failed:", description=text, color=cfc)
    embed.set_thumbnail(url=user.avatar.url)
    await channel.send(embed=embed)
  else:
    embed = discord.Embed(title=f"**{user}** spammed `{ctx.channel}` **{amount} times** with the following text:", description=text, color=cfc)
    embed.set_thumbnail(url=user.avatar.url)
    await ctx.respond("Get ready for the show <:aye:965627580743024671>", ephemeral=True)
    await channel.send(embed=embed)
    for i in range(amount):
      await ctx.send(text)

@admin.command(name="slowmode", description="Set the slow mode of a channel")
@option("slowmode", description="What the slow mode delay should be.")
@option("channel", description="The channel to set a slow mode too.", required=False)
@commands.has_permissions(manage_channels=True)
async def sm(ctx, slowmode:int, channel: discord.TextChannel):
  if channel == None:
    await ctx.channel.edit(slowmode_delay=slowmode)
    embed = discord.Embed(title=f"This channel's slow mode has been set to {slowmode} second(s)!", color=cfc)
    await ctx.respond(embed=embed)
  else:
    await channel.edit(slowmode_delay=slowmode)
    embed = discord.Embed(title=f"`{channel}`'s slow mode has been set to {slowmode} second(s)!", color=cfc)
    await ctx.respond(embed=embed)
  
@admin.command(description='Delete messages from a channel.')
@commands.has_permissions(manage_channels=True)
async def purge(ctx, amount: int):
    channel = bot.get_channel(1001405648828891187)
    if amount > 100:
      class Purge(discord.ui.Button):
        def __init__(self):
          super().__init__(timeout=10.0)

          @discord.ui.button(custom_id="okbutton", style=discord.ButtonStyle.green, emoji="✅")
          async def button_callback(self, button, interaction):
                await interaction.response.send_message(f"Ok, purging {amount} messages.", ephemeral=True)
                await ctx.channel.purge(limit=amount, check=lambda message: not message.pinned)
                embed = discord.Embed(title=f"{ctx.author} purged **{amount}** messages in `{ctx.channel} after confirmation!", color=0x4f94cf)
                await channel.send(embed=embed)
      class Purge2(discord.ui.Button):
        def __init__(self):
          super().__init__(timeout=10.0)

          @discord.ui.button(custom_id="nobutton", style=discord.ButtonStyle.danger, emoji="❌")
          async def button_callback(self, button, interaction):
                await interaction.response.send_message(f"Ok, cancelling purge.", ephemeral=True)
        
      embed=discord.Embed(title="**Do you want to continue?**", description=f"You are purging **{amount} messages!**")
      await ctx.respond("That's to much", ephemeral=True)
    else:
      await ctx.channel.purge(limit=amount, check=lambda message: not message.pinned)
      await ctx.respond(f"Purging {amount} messages.", ephemeral=True)
      embed = discord.Embed(title=f"{ctx.author} purged **{amount}** messages in `{ctx.channel}`!", color=cfc)
      embed.set_thumbnail(url=ctx.author.avatar.url)
      await channel.send(embed=embed)

@fun.command(name="dadjoke", description="Gives a dadjoke")
async def dadjoke(ctx):
  joke = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "text/plain"}).text
  embed = discord.Embed(title=f"**{joke}**", color=cfc)
  await ctx.respond(embed=embed)

@math.command(name="basic", description="Do some basic math.")
@option("type", description="The type of basic math you want to do.", choices=["Addition","Subtraction","Multiplication","Division"])
@option("input1", description="The first number.")
@option("input2", description="The second number.")
async def basic(ctx, type,input1:int, input2:int):
  if type == "Addition":
    embed = discord.Embed(title=f"{input1} + {input2} = {input1+input2}", color=cfc)
    await ctx.respond(embed=embed)
  if type == "Subtraction":
    embed = discord.Embed(title=f"{input1} - {input2} = {input1-input2}", color=cfc)
    await ctx.respond(embed=embed)
  if type == "Multiplication":
    embed = discord.Embed(title=f"{input1} x {input2} = {input1*input2}", color=cfc)
    await ctx.respond(embed=embed)
  if type == "Division":
    embed = discord.Embed(title=f"{input1} : {input2} = {input1/input2}", color=cfc)
    await ctx.respond(embed=embed)

@math.command(name="advanced", description="Do some more advanced math.")
@option("type", description="The type of advanced math you want to do.", choices=["Square root", "Power"])
@option("input", description="The first number")
@option("power", description="The exponent (not needed for sqrt)", required=False)
async def square_root(ctx, type, input: int, exponent:int):
  if type == "Square root":
    embed = discord.Embed(title=f"The square root of {input} is {sqrt(input)}", color=cfc)
    await ctx.respond(embed=embed)
  if type == "Power" and exponent == None:
    await ctx.respond("You need to give a exponent...")
  if type == "Power":
    embed = discord.Embed(title=f"The square root of {input} is {input**exponent}", color=cfc)
    await ctx.respond(embed=embed)

###################################
####     Virtual Airline     ######
###################################
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

@va.command(name="file", descriprion="File a flight that you will do for the Clearfly VA.")
@option("aircraft", description="The aircraft you will use for the flight.(for more aircraft send a dm to WolfAir)", choices=["B732", "B738", "A300"])
@option("origin", description="The airport(ICAO) you will fly from.", choices=airports)
@option("destination", description="The airport(ICAO) you will fly to.", choices=airports)
async def file(ctx, aircraft, origin, destination):
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
@va.command(name="flights", descripiton="Fetches flights a user has done.")
async def datar(ctx, user: discord.Member = None):
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



###############
##--BUTTONS--##
###############
class MyView(discord.ui.View):
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
  embed = discord.Embed(title="ClearFly Rules", description="1. Don’t post any NSFW(Not Safe For Work) or inappropriate content. This will result in a warning, or an immediate ban depending on the severity.\n\n2. Post content in the correct channels.\n\n3. Do not spam, except in the spam channel.\n\n4. No harassment. If you are being harassed, let the staff know by using the </report:1018970055972757506> command, and we will deal with it from there. Refrain from communicating with the person harassing you as we resolve the problem.\n\n5. Don’t excessively ping members. This will result in a mute.\n\n6. Don’t post any political content.\n\n7. Use common sense.\n\n8. Follow the [Discord TOS](https://discord.com/terms) and [Community Guidelines.](https://discord.com/guidelines)", color=cfc)
  await ctx.respond("rules posted!",ephemeral=True)
  await ctx.send(embed=embed,view=MyView())

class MyView2(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=None)

    @discord.ui.button(label="I have read the FAQ", custom_id="faqbutton", style=discord.ButtonStyle.secondary, emoji="<:ClearFly_half_clear:1009117524677369866>")
    async def button_callback(self, button, interaction):
      author = interaction.user
      guild = bot.get_guild(965419296937365514)
      role = guild.get_role(1002932992534134814)
      await author.add_roles(role)
      await interaction.response.send_message("Thanks for reading the FAQ, now you can ask questions in <#965598257017413673>!",ephemeral=True)

@admin.command(name="faq", descritpion="sends the faq(admin only)")
@commands.has_permissions(manage_channels=True)
async def faq(ctx):
  embed = discord.Embed(title="ClearFly FAQ", description="**When will it release?**\nWhen it’s done.\n\n**Is the project dead?**\nNo, we are just not working on it 24/7\n\n**Will there be a 3D cabin?**\nYes!\n\n**Will there be a custom FMC?**\nThis is a complicated topic. We most likely will custom code something like CIV-A for navigation in the initial release, but might later code a UNS if we gain enough experience for the modern avionics version.", color=cfc)
  await ctx.respond("FAQ posted!",ephemeral=True)
  await ctx.send(embed=embed,view=MyView2())

class MyView3(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=None)

    @discord.ui.button(custom_id="announcebutton", style=discord.ButtonStyle.primary, emoji="📣")
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


class MyView4(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=None)

    @discord.ui.button(custom_id="updatebutton", style=discord.ButtonStyle.primary, emoji="🛠")
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
class MyView5(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=None)

    @discord.ui.button(custom_id="vabutton", style=discord.ButtonStyle.primary, emoji="✈️")
    async def button_callback(self, button, interaction):
      author = interaction.user
      guild = bot.get_guild(965419296937365514)
      role = guild.get_role(1013933799777783849)
      if role in author.roles:
        author = interaction.user
        guild = bot.get_guild(965419296937365514)
        role = guild.get_role(1013933799777783849)
        await author.remove_roles(role)
        await interaction.response.send_message("You are no longer part of the ClearFly VA",ephemeral=True)
      else:
        author = interaction.user
        guild = bot.get_guild(965419296937365514)
        role = guild.get_role(1013933799777783849)
        await author.add_roles(role)
        await interaction.response.send_message("You are now part of the ClearFly VA!",ephemeral=True)
@admin.command(name="buttonroles", descritpion="sends the button roles(admin only)")
@commands.has_permissions(manage_channels=True)
async def faq(ctx):
  embed = discord.Embed(title="Announcement Pings", description="Click on 📣 for announcement pings.\n*(click again to remove.)*", color=cfc)
  emb = discord.Embed(title="Update Pings", description="Click on 🛠 for update pings.\n*(click again to remove.)*", color=cfc)
  embva = discord.Embed(title="ClearFly VA pilot", description="Click on ✈️ to be part of the Official ClearFly VA!\n*(click again to remove.)*", color=cfc)
  await ctx.respond("Button roles posted!",ephemeral=True)
  await ctx.send(embed=embed,view=MyView3())
  await ctx.send(embed=emb,view=MyView4())
  await ctx.send(embed=embva,view=MyView5())

##############################
##no more commands down here##
##############################

@utility.command(name="ping",description="Shows the latency speed of the bot.")
async def ping(ctx):
    emb = discord.Embed(title="Bot's latency", description=f"The bot's latency is {round(bot.latency*1000)}ms!", color=0x4f93cf)
    await ctx.respond(embed=emb)

bot.launch_time = datetime.utcnow()

@utility.command(name="stats",description="Show statistics about the bot and server.")
async def stats(ctx):
  delta_uptime = datetime.utcnow() - bot.launch_time
  hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)
  embed = discord.Embed(title = "**Bot Stats**", description =    f"""
```rb
Creator: Matt3o0#4764
Uptime: {days}d {hours}h {minutes}m {seconds}s
```
  """, color = 0x4f93cf)
  servers = len(bot.guilds)
  members = 0
  for guild in bot.guilds:
    members += guild.member_count - 1
  pythonVersion = platform.python_version()
  dpyVersion = discord.__version__
  serverCount = len(bot.guilds)
  memberCount = len(set(bot.get_all_members()))
  embed.add_field(
            name="**Server Stats**",
            value=f"""
```rb
Members: {members}
```
            """,
            inline=False
      )
  await ctx.respond(embed = embed)

@bot.command(name="help", description="Help command for the bot.")
async def embed(ctx):
    emb = discord.Embed(title = "**Help**",color = cfc)
    emb.add_field(name="**Available commands**", value=f"""
*more to come soon!*
```
/help : Shows this information.
/report : Report a user or situation to the team.
/utility stats : Show statistics about the bot and server.
/utility ping : Shows the latency speed of the bot.
/utility who-is : Shows all kind of information about a user.
/utility the-team : Shows The ClearFly Team!
/utility avatar : Shows your avatar.
/utility github : Shows the bot's GitHub repository.
/utility math basic: Do some basic math.
/utility math advanced: Do some advanced math.
/fun ascii : Converts text in to ascii.
/fun 8ball : Ask the bot some questions!
/fun dadjoke: Gets you a dadjoke.
```
  """)
    emb.add_field(
            name="**ClearFly Virtual Airline**",
            value=f"""
```
/va file : File a flight you are gonna do for the ClearFly VA.
/va flights : Fetches information about all flights a user has done
```
            """, inline=False
      )
    await ctx.respond(embed=emb)

#############################################
bot.run(os.getenv('TOKEN'))
