###################
#-Made by Matt3o0-#
###################
import glob
import discord #Using pycord
import os
import re
import platform
import pyfiglet
import requests
import random
import configparser
from dadjokes import Dadjoke
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
from discord import ButtonStyle, option


load_dotenv()#for the token

cfc = 0x4f93cf #<- this is the non halloween color
#cfc = 0xcc8d0e # <- halloween color
errorc = 0xFF0000

bot = discord.Bot(command_prefix=',', intents=discord.Intents.all())
############
## Groups ##
############
fun = bot.create_group(name="fun",description="Commands that are supposed to be fun")
va = bot.create_group(name="va",description="Commands related to the ClearFly Virtual Airline")
admin = bot.create_group(name="admin", description="Commands for admins")
leveling = bot.create_group(name="level", description="Commands related to leveling")
utility = bot.create_group(name="utility", description="Commands related to utility")
math = utility.create_subgroup(name="math", description="Commands related to math")
instructor = va.create_subgroup(name="instructor", description="Commands for the ClearFly Instructors")


###############
## Listeners ##
###############
@bot.listen()
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Starting up."),status=discord.Status.online)
    sleep(0.5)
    await bot.change_presence(activity=discord.Game(name="Starting up.."),status=discord.Status.online)
    sleep(0.5)
    await bot.change_presence(activity=discord.Game(name="Starting up..."),status=discord.Status.online)
    channel=bot.get_channel(1001405648828891187)
    now = discord.utils.format_dt(datetime.now())
    if os.path.exists(".onpc"):
      embed=discord.Embed(title="I started up!", description=f"""
      Started bot up on {now}
      *Data save available*
      """,color=0x00FF00)
      await channel.send(embed=embed)
    else:
      embed=discord.Embed(title="I started up!", description=f"""
      Started bot up on {now}
      *Data save available*
      """,color=0x00FF00)
      await channel.send(embed=embed)
    bot.add_view(MyView())
    bot.add_view(MyView2())
    bot.add_view(MyView3())
    bot.add_view(MyView4())
    bot.add_view(InfoB4training())
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

##level code lel##
@bot.listen()
async def on_message(message):
  if os.path.exists(".onpc"):
    nowlvlprog = 0
    config = configparser.ConfigParser()
    if message.channel.id == 966077223260004402:
      return
    if message.channel.id == 965600413376200726:
      return
    else:
      if message.author.bot == False:
        if os.path.exists(f"Leveling/users/{message.author.id}/data.ini"):
            config.read(f"Leveling/users/{message.author.id}/data.ini")
            belvlprog = config.get("Level", "lvlprog")
            if len(message.content) > 0:
              nowlvlprog = int(belvlprog)+1
            if len(message.content) > 10:
              nowlvlprog = int(belvlprog)+2
            if len(message.content) > 25:
              nowlvlprog = int(belvlprog)+5
            if len(message.content) > 50:
              nowlvlprog = int(belvlprog)+10
            if len(message.content) > 75:
              nowlvlprog = int(belvlprog)+15
            lvlprog = config.get("Level", "lvlprog")
            lvl = config.get("Level", "lvl")
            topprog = config.get("Level", "topprog")
            config.set("Level","lvlprog", f"{nowlvlprog}")
            if int(lvlprog) >= int(topprog):
                config.set("Level","lvlprog", "0")
                config.set("Level","lvl", f"{int(lvl)+1}")
                config.set("Level","topprog", f"{int(topprog)*2-(int(lvl)*3)}")
                lvlp = config.get("Level", "lvl")
                await message.channel.send(f"{message.author.mention} :partying_face: You reached level {lvlp}!")
            with open(f"Leveling/users/{message.author.id}/data.ini", "w") as configfile:
                config.write(configfile)
        else:
            os.mkdir(f"Leveling/users/{message.author.id}")
            config.add_section("Level")
            config.set("Level","lvlprog", "1")
            config.set("Level","lvl", "0")
            config.set("Level","topprog", "50")
            with open(f"Leveling/users/{message.author.id}/data.ini", "w") as configfile:
                config.write(configfile)
            lvlprog = config.get("Level", "lvlprog")
            topprog = config.get("Level", "topprog")
            lvl = config.get("Level", "lvl")
  else: 
    return

@leveling.command(name="userlevel", description="Gets the provided user's level.")
async def userlevel(ctx, member: discord.Member = None):
    await ctx.respond("Loading level data.")
    config = configparser.ConfigParser()
    sleep(0.2)
    await ctx.edit(content="Loading level data..")
    if member == None:
        sleep(0.2)
        await ctx.edit(content="Loading level data...")
        if os.path.exists(f"Leveling/users/{ctx.author.id}/data.ini"):
          config.read(f"Leveling/users/{ctx.author.id}/data.ini")
          lvlprog = config.get("Level", "lvlprog")
          lvl = config.get("Level", "lvl")
          topprog = config.get("Level", "topprog")
          embed = discord.Embed(title=f"Your current level:", description=f"XP: `{lvlprog}`/`{topprog}`  Level:`{lvl}`", color=cfc)
          embed.set_thumbnail(url=ctx.author.avatar.url)
          await ctx.edit(content=None, embed=embed)
        else:
          embed = discord.Embed(title="Error 404!", description="This most probably means that you never sended a message(slash commands or messages before the introduction of leveling don't count) in this server.", color=errorc)
          await ctx.edit(content=None, embed=embed)
    else:
        sleep(0.2)
        await ctx.edit(content="Loading level data...")
        if os.path.exists(f"Leveling/users/{member.id}/data.ini"):
          config.read(f"Leveling/users/{member.id}/data.ini")
          lvlprog = config.get("Level", "lvlprog")
          lvl = config.get("Level", "lvl")
          topprog = config.get("Level", "topprog")
          embed = discord.Embed(title=f"{member}'s current level:", description=f"XP: `{lvlprog}`/`{topprog}`  Level:`{lvl}`", color=cfc)
          embed.set_thumbnail(url=member.avatar.url)
          await ctx.edit(content=None, embed=embed)
        else:
          embed = discord.Embed(title="Error 404!", description="This most probably means that this user never sended a message(slash commands or messages before the introduction of leveling don't count) in this server.", color=errorc)
          await ctx.edit(content=None, embed=embed)

@bot.user_command(name="User level", description="Gets the provided user's level.")
async def userlevel(ctx, member: discord.Member = None):
    await ctx.respond("Loading level data.")
    config = configparser.ConfigParser()
    sleep(0.2)
    await ctx.edit(content="Loading level data..")
    if member == None:
        sleep(0.2)
        await ctx.edit(content="Loading level data...")
        if os.path.exists(f"Leveling/users/{ctx.author.id}/data.ini"):
          config.read(f"Leveling/users/{ctx.author.id}/data.ini")
          lvlprog = config.get("Level", "lvlprog")
          lvl = config.get("Level", "lvl")
          topprog = config.get("Level", "topprog")
          embed = discord.Embed(title=f"Your current level:", description=f"XP: `{lvlprog}`/`{topprog}`  Level:`{lvl}`", color=cfc)
          embed.set_thumbnail(url=ctx.author.avatar.url)
          await ctx.edit(content=None, embed=embed)
        else:
          embed = discord.Embed(title="Error 404!", description="This most probably means that you never sended a message(slash commands or messages before the introduction of leveling don't count) in this server.", color=errorc)
          await ctx.edit(content=None, embed=embed)
    else:
        sleep(0.2)
        await ctx.edit(content="Loading level data...")
        if os.path.exists(f"Leveling/users/{member.id}/data.ini"):
          config.read(f"Leveling/users/{member.id}/data.ini")
          lvlprog = config.get("Level", "lvlprog")
          lvl = config.get("Level", "lvl")
          topprog = config.get("Level", "topprog")
          embed = discord.Embed(title=f"{member}'s current level:", description=f"XP: `{lvlprog}`/`{topprog}`  Level:`{lvl}`", color=cfc)
          embed.set_thumbnail(url=member.avatar.url)
          await ctx.edit(content=None, embed=embed)
        else:
          embed = discord.Embed(title="Error 404!", description="This most probably means that this user never sended a message(slash commands or messages before the introduction of leveling don't count) in this server.", color=errorc)
          await ctx.edit(content=None, embed=embed)

@leveling.command(name="leaderboard", description="See the leaderboard of the whole server.")
async def lb(ctx):
  output = []
  index = 1
  config = configparser.ConfigParser()
  for index, filename in enumerate(glob.glob('Leveling/users/*/*')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        config.read(f"{filename}")
        lvl = int(config.get("Level", "lvl"))
        lvlprog = int(config.get("Level", "lvlprog"))
        topprog = int(config.get("Level", "topprog"))
        filen = filename.replace("Leveling/users/", f"")
        lbn = index+1
        id=os.path.dirname(filen)
        user = bot.get_user(int(id))
        line = f"{lvlprog+topprog*lvl} | Level:{lvl} XP:{lvlprog}/{topprog} {user.name}\n"
        output.append(line)
  def atoi(text):
    return int(text) if text.isdigit() else text
  def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)',text) ]
  output.sort(key=natural_keys, reverse=True)
  def delstr(lst):
    return [
        f"{' '.join(elem.split()[1:]).rstrip()}"
        for elem in lst
    ]
        
  if __name__ == "__main__":
        output = delstr(output)

  def movestr(lst):
    return [
        f"{' '.join(elem.split()[3:]).rstrip()} {' '.join(elem.split()[:3])}\n"
        for elem in lst
    ]
        
  if __name__ == "__main__":
          output = movestr(output)
          print(output)

  foutput = [f'{index} | {i}' for index, i in enumerate(output, 1)]
  embed = discord.Embed(title="ClearFly Level Leaderboard", description=f"""
  Chat more to go higher on the list!
  ```
{"".join(foutput)}
  ```
  """, color=cfc)
  await ctx.respond(embed=embed)



@bot.listen()
async def on_member_join(member):
    channel = bot.get_channel(965600413376200726)
    emb = discord.Embed(title=f"Welcome to ClearFly!", description=f"Hey there, {member.mention}! Be sure to read the <#1002194493304479784> to become a member and gain full access to the server! Thanks for joining!", color = cfc)
    await channel.send(embed=emb)

@bot.listen()
async def on_member_remove(member):
  channel = bot.get_channel(1001405648828891187)
  emb = discord.Embed(title=f"{member} left.", color=cfc, description=f"Joined on {discord.utils.format_dt(member.joined_at)}")
  pfp = member.avatar.url
  emb.set_thumbnail(url=pfp)
  await channel.send(embed=emb)

@bot.listen()
async def on_message_delete(message):
  if message.author.bot == False:
    channel = bot.get_channel(1001405648828891187)
    msgdel = message.clean_content
    msgatr = message.author.mention
    msgcnl = message.channel.mention
    pfp = message.author.avatar.url
    emb = discord.Embed(title="**Message Deleted:**", color=cfc)
    emb.add_field(name="Content:", value=f"{msgdel}", inline = False)
    emb.add_field(name="Author:", value=f"{msgatr}", inline = True)
    emb.add_field(name="Channel:", value=f"{msgcnl}", inline = True)
    emb.set_thumbnail(url=pfp)
    await channel.send(embed=emb)
  else:
    pass

@bot.listen()
async def on_message_edit(before, after):
  if before.author.bot == False:
    channel = bot.get_channel(1001405648828891187)
    msgeditb = before.clean_content
    msgedita = after.clean_content
    msgatr = before.author.mention
    msgcnl = before.channel.mention
    pfp = before.author.avatar.url
    emb = discord.Embed(title="**Message Edited:**", color=cfc)
    emb.add_field(name="Content before:", value=f"{msgeditb}", inline = False)
    emb.add_field(name="Content after:", value=f"{msgedita}", inline = False)
    emb.add_field(name="Author:", value=f"{msgatr}", inline = True)
    emb.add_field(name="Channel:", value=f"{msgcnl}", inline = True)
    emb.set_thumbnail(url=pfp)
    await channel.send(embed=emb)
  else:
    pass


##############
## Commands ##
##############
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

@admin.command(name="echo",description="Send a message as the bot.")
@commands.has_permissions(manage_channels=True)
async def echo(ctx, text: str):
    await ctx.respond('posted your message!',ephemeral  = True)
    await ctx.channel.send(text)
    pfp = ctx.author.avatar.url
    channel = bot.get_channel(1001405648828891187)
    emb = discord.Embed(title=f"{ctx.author} used echo:", description=text, color = cfc)
    emb.set_thumbnail(url=pfp)
    await channel.send(embed=emb)

@admin.command(name="embed",description="Send an embed as the bot.")
@commands.has_permissions(manage_channels=True)
async def embed(ctx, title: str, description: str):
    await ctx.respond('posted your embed!',ephemeral  = True)
    emb = discord.Embed(title=title, description=description, color=cfc)
    await ctx.channel.send(embed=emb)
    pfp = ctx.author.avatar.url
    channel2 = bot.get_channel(1001405648828891187)
    embed = discord.Embed(title=f"{ctx.author} used embed:", color = cfc)
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

@utility.command(name='the-team', description='Shows The ClearFly Team!')
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

@bot.user_command(name="User Avatar", description="Get's the avatar from the user")
async def avatar_app(ctx, user:discord.Member):
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

@bot.user_command(name="User Profile")
async def whois_app(ctx, user:discord.Member):
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
  emb = discord.Embed(title="GitHub:", description="[Here's the repository!](https://github.com/ClearFly-Official/ClearBot)",color=cfc)
  await ctx.respond(embed=emb)

@fun.command(name="8ball", description="Ask the bot some questions!")
async def VIIIball(ctx, question):
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
async def spam(ctx, amount: int,text):
  channel = bot.get_channel(1001405648828891187)
  user = ctx.author
  global confirm
  confirm = 0
  if amount > 100:
      class Spam(discord.ui.View):
          def __init__(self):
            super().__init__(timeout=10.0)

          @discord.ui.button(custom_id="okbutton", style=discord.ButtonStyle.green, emoji="<:yes:765068298004987904>")
          async def button_callback(self, button, interaction):
            global confirm
            confirm = 1
            channel = bot.get_channel(1001405648828891187)
            await interaction.response.send_message(f"Ok, spamming {ctx.channel} {amount} times", ephemeral=True)
            embed = discord.Embed(title=f"**{user}** spammed `{ctx.channel}` **{amount} times**(after confirmation) with the following text:", description=text, color=cfc)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await channel.send(embed=embed)
            for i in range(amount):
              await ctx.send(text)
          @discord.ui.button(custom_id="nobutton", style=discord.ButtonStyle.danger, emoji="<:No:744714930946572371>")
          async def second_button_callback(self, button, interaction):
            global confirm
            confirm = 1
            await interaction.response.send_message(f"Ok, cancelling spam.", ephemeral=True)
            await ctx.edit(view=None)

          async def on_timeout(self):
            global confirm
            if confirm == 0:
              await ctx.edit(view=None)
              await ctx.respond("You waited too long, run the command again to spam!", ephemeral=True)
            else:
              return

      embed=discord.Embed(title="**Do you want to continue?**", description=f"You are spamming **{amount} times**, that's a lot!", color=cfc)
      await ctx.respond(embed=embed,view=Spam(),ephemeral=True)
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
  if slowmode > 21600:
    await ctx.respond("Max slowmode is 21600 seconds!")
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
    global confirm
    confirm = 0
    channel = bot.get_channel(1001405648828891187)
    if amount > 100:
      class MyView1(discord.ui.View):
          def __init__(self):
            super().__init__(timeout=15.0)

          @discord.ui.button(custom_id="okbutton", style=discord.ButtonStyle.green, emoji="<:yes:765068298004987904>")
          async def button_callback(self, button, interaction):
            global confirm 
            confirm = 1
            channel = bot.get_channel(1001405648828891187)
            await interaction.response.send_message(f"Ok, purging {amount} messages.", ephemeral=True)
            await ctx.channel.purge(limit=amount, check=lambda message: not message.pinned)
            embed = discord.Embed(title=f"{ctx.author} purged **{amount}** messages in `{ctx.channel}` after confirmation!", color=cfc)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            await channel.send(embed=embed)
            await ctx.edit(view=None)
          @discord.ui.button(custom_id="nobutton", style=discord.ButtonStyle.danger, emoji="<:No:744714930946572371>")
          async def second_button_callback(self, button, interaction):
            global confirm
            confirm = 1
            await interaction.response.send_message(f"Ok, cancelling purge.", ephemeral=True)
            await ctx.edit(view=None)

          async def on_timeout(self):
            global confirm
            if confirm == 0:
              await ctx.edit(view=None)
              await ctx.respond("You waited too long, run the command again to purge!", ephemeral=True)
            else:
              return
      embed=discord.Embed(title="**Do you want to continue?**", description=f"You are purging **{amount} messages**, that's a lot!", color=cfc)
      await ctx.respond(embed=embed,view=MyView1(),ephemeral=True)
    else:
      await ctx.channel.purge(limit=amount, check=lambda message: not message.pinned)
      await ctx.respond(f"Purging {amount} messages.", ephemeral=True)
      embed = discord.Embed(title=f"{ctx.author} purged **{amount}** messages in `{ctx.channel}`!", color=cfc)
      embed.set_thumbnail(url=ctx.author.avatar.url)
      await channel.send(embed=embed)

@fun.command(name="dadjoke", description="Gives a dadjoke")
async def dadjoke(ctx):
  dadjoke = Dadjoke()
  embed = discord.Embed(title=f"{dadjoke.joke}", color=cfc)
  await ctx.respond(embed=embed)





@math.command(name="basic", description="Do some basic math.")
@option("type", description="The type of basic math you want to do.", choices=["Addition","Subtraction","Multiplication","Division"])
@option("input1", description="The first number.")
@option("input2", description="The second number.")
async def basic(ctx, type,input1:int, input2:int):
  if type == "Addition":
    embed = discord.Embed(description=f"{input1} + {input2} = **{input1+input2}**", color=cfc)
    await ctx.respond(embed=embed)
  if type == "Subtraction":
    embed = discord.Embed(description=f"{input1} - {input2} = **{input1-input2}**", color=cfc)
    await ctx.respond(embed=embed)
  if type == "Multiplication":
    embed = discord.Embed(description=f"{input1} x {input2} = **{input1*input2}**", color=cfc)
    await ctx.respond(embed=embed)
  if type == "Division":
    if input2 == 0:
      await ctx.respond("You can't divide by 0!")
    else:
      embed = discord.Embed(description=f"{input1} : {input2} = **{input1/input2}**", color=cfc)
      await ctx.respond(embed=embed)

@math.command(name="advanced", description="Do some more advanced math.")
@option("type", description="The type of advanced math you want to do.", choices=["Square root", "Power"])
@option("input", description="The first number")
@option("power", description="The exponent (not needed for sqrt)", required=False)
async def advanced(ctx, type, input: int, exponent:int = None):
  if input > 2500:
    await ctx.respond("Too big of a number!")
    return
  if exponent == None:
    pass
  else:
    if exponent > 1000:
      await ctx.respond("Too big of an exponent!")
      return
  if type == "Square root":
    embed = discord.Embed(title=f"The square root of {input} is", description=f"**{sqrt(input)}**", color=cfc)
    await ctx.respond(embed=embed)
  if type == "Power" and exponent == None:
    await ctx.respond("You need to give a exponent...")
  if type == "Power":
    embed = discord.Embed(title=f"{input} to the power of {exponent} is",description=f"**{input**exponent}**", color=cfc)
    await ctx.respond(embed=embed)

@fun.command(name="roast", description="Roast whoever you'd like!")
@option("member", description="The person you'd like to roast")
async def roast(ctx, member: discord.Member):
  roasts = [
    "Your face made the onion cry.",
    "I’m jealous of people who don’t know you.",
    "If I had a face like yours, I’d sue my parents.",
    "You sound reasonable… Time to up my medication.",
    "I might be crazy, but crazy is better than stupid.",
    "My middle finger gets a boner every time I see you.",
    "If your brain was made of chocolate, it wouldn't fill an M&M.",
    "You're not funny, but your life, now that's a joke.",
    "If laughter is the best medicine, your face must be curing the world.",
    "If you are going to be two faced, at least make one of them pretty.",
    "You're as bright as a black hole, and twice as dense.",
    "I may love to shop but I'm not buying your bullshit.",
    "I'm not saying I hate you, but I would unplug your life support to charge my phone.",
    "You shouldn't play hide and seek, no one would look for you.",
    "You're so fat, when you wear a yellow rain coat people scream \"taxi\".",
    "If I gave you a penny for your thoughts, I'd get change.",
    "If you really want to know about mistakes, you should ask your parents.",
    "Don't feel sad, don't feel blue, Frankenstein was ugly too.",
    "There's only one problem with your face, I can see it.",
    "There are more calories in your stomach than in the local supermarket!",
    "You're so ugly, the only dates you get are on a calendar",
    "I heard your parents took you to a dog show and you won.",
    "Why don't you check eBay and see if they have a life for sale.",
    "Why don't you slip into something more comfortable -- like a coma.",
    "Is there an app I can download to make you disappear?",
    "Keep rolling your eyes. Maybe you’ll find your brain back there.",
    "I suggest you do a little soul searching. You might just find one.",
    "Maybe you should eat make-up so you’ll be pretty on the inside too.",
    "I keep thinking you can’t get any dumber and you keep proving me wrong.",
    "Why is it acceptable for you to be an idiot but not for me to point it out?",
    "Everyone brings happiness to a room. I do when I enter, you do when you leave.",
    "I thought I had the flu, but then I realized your face makes me sick to my stomach.",
    "When karma comes back to punch you in the face, I want to be there in case it needs help.",
    "I’m not an astronomer but I am pretty sure the earth revolves around the sun and not you.",
    "If you’re going to be a smart ass, first you have to be smart, otherwise you’re just an ass.",
    "Do yourself a favor and ignore anyone who tells you to be yourself. Bad idea in your case.",
    "Your crazy is showing. You might want to tuck it back in.",
  ]
  output = random.choice(roasts)
  if member.id == 1001249135774666823:
    await ctx.respond("Why do you want to roast me :sob:")
  else:
    await ctx.respond(f"{member.mention} {output}")

class ButtonGame(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  global b, isPressed
  b = 0
  isPressed = 0

  @discord.ui.button(label="1", style=discord.ButtonStyle.green)
  async def first_button_callback(self, button, interaction):
    global b, isPressed
    b = 1
    isPressed = 1
    opts = [1, 2, 3, 1, 2, 3]
    output = random.choice(opts)
    for child in self.children:
      child.disabled = True
    if output == b:
        await interaction.response.send_message(":partying_face: You guessed right, congrats!")
    else:
      if isPressed == 1:
        await interaction.response.send_message(f":disappointed_relieved: You guessed wrong, the right answer was {output}")

  @discord.ui.button(label="2", style=discord.ButtonStyle.green)
  async def second_button_callback(self, button, interaction):
    global b, isPressed
    b = 2
    isPressed = 1
    for child in self.children:
      child.disabled = True
    opts = [1, 2, 3, 1, 2, 3]
    output = random.choice(opts)
    if output == b:
        await interaction.response.send_message(":partying_face: You guessed right, congrats!")
    else:
      if isPressed == 1:
        await interaction.response.send_message(f":disappointed_relieved: You guessed wrong, the right answer was {output}")

  @discord.ui.button(label="3", style=discord.ButtonStyle.green)
  async def third_button_callback(self, button, interaction):
    global b, isPressed
    b = 3
    isPressed = 1
    opts = [1, 2, 3, 1, 2, 3]
    for child in self.children:
      child.disabled = True
    output = random.choice(opts)
    if output == b:
        await interaction.response.send_message(":partying_face: You guessed right, congrats!")
    else:
      if isPressed == 1:
        await interaction.response.send_message(f":disappointed_relieved: You guessed wrong, the right answer was {output}")
  
  async def on_timeout(self, interaction):
    if isPressed == 0:
      await interaction.response.edit_message(view=self)
      await interaction.response.send_message("You waited too long, run the command again to play the game!", ephemeral=True)
    else:
      await interaction.response.edit_message(view=self)
  


@fun.command(name="buttongame", description="Play a game with buttons!")
async def bgame(ctx):
  embed = discord.Embed(title="Choose a button!", color=cfc)
  await ctx.respond(embed=embed, view=ButtonGame())

#Might use the cities in the future(weather cmd maybe)
cities=['A Coruña', 'Aachen', 'Aarhus', 'Abbeville', 'Aberdeen (UK)', 'Aberdeen (South Dakota)', 'Aberdeen (Washington)', 'Abidjan', 'Abilene', 'Abu Dhabi', 'Abuja', 'Acapulco', 'Accra', 'Adamstown', 'Addis Ababa', 'Adelaide', 'Adelboden', 'Agadir', 'Agde', 'Agen', 'Agios Nikolaos', 'Agra', 'Agrigento', 'Agropoli', 'Ahmedabad', 'Aigues-Mortes', 'Aix-en-Provence', 'Aix-les-Bains', 'Ajaccio', 'Ajman', 'Akron', 'Al Ain', 'Alanya', 'Alaró', 'Albacete', 'Albany', 'Albenga', 'Albi', 'Albufeira', 'Albuquerque', 'Alcudia', 'Aleppo', 'Alessandria', 'Ålesund', 'Alexandria (U.S.)', 'Alexandria (Egypt)', 'Algeciras', 'Alghero', 'Algiers', 'Alicante', 'Alkmaar', 'Allentown', 'Almaty', 'Alofi', "Alpe d'Huez", 'Alta Badia', 'Altea', 'Altoona', 'Amalfi', 'Amapala', 'Amarillo', 'Amersfoort', 'Amiens', 'Amman', 'Amsterdam', 'Anaheim', 'Anchorage', 'Ancona', 'Andalo', 'Andermatt', 'Andorra la Vella', 'Andratx', 'Andria', 'Angers', 'Angoulême', 'Ankara', 'Ann Arbor', 'Annapolis', 'Annecy', 'Antalya', 'Antananarivo', 'Antibes', 'Antigua Guatemala', 'Antwerp', 'Anzio', 'Ao Nang', 'Aosta', 'Apeldoorn', 'Apia', 'Appleton', 'Aqaba', 'Aracaju', 'Arcachon', 'Arenzano', 'Arequipa', 'Arezzo', 'Argostoli', 'Arica', 'Arles', 'Arlington (Virginia)', 'Arlington (Texas)', 'Armagh', 'Arnhem', 'Arosa', 'Arras', 'Arrecife', 'Artà', 'Asbury Park', 'Ascoli Piceno', 'Ascona', 'Ashdod', 'Ashgabat', 'Ashkelon', 'Asmara', 'Aspen', 'Asti', 'Astoria', 'Asunción', 'Atafu', 'Athens', 'Athlone', 'Atlanta', 'Atlantic City', 'Auckland', 'Augsburg', 'Augusta (Georgia)', 'Augusta (Maine)', 'Aurora (Colorado)', 'Aurora (Illinois)', 'Austin', 'Auxerre', 'Avalon (California)', 'Avalon (New Jersey)', 'Avarua', 'Aveiro', 'Avellino', 'Avignon', 'Avila Beach', 'Avoriaz', 'Axamer Lizum', 'Ayia Napa', 'Azusa', 'Bad Gastein', 'Bad Hofgastein', 'Baden', 'Baghdad', 'Baiona', 'Bakersfield', 'Baku', 'Baltimore', 'Bamako', 'Bandar Seri Begawan', 'Bandol', 'Bangalore', 'Bangkok', 'Bangor', 'Bangui', 'Banjul', 'Bar', 'Bar Harbor', 'Barcelona', 'Bari', 'Barletta', 'Barstow', 'Basel', 'Basseterre', 'Basse-Terre', 'Bastia', 'Bata', 'Bath', 'Baton Rouge', 'Batumi', 'Bayonne', 'Beaulieu-sur-Mer', 'Beaumont', 'Beaune', 'Beersheba', 'Beijing', 'Beirut', 'Belek', 'Belfast', 'Belfort', 'Belgrade', 'Belize City', 'Bellingham', 'Bellinzona', 'Belluno', 'Belmopan', 'Belo Horizonte', 'Bemidji', 'Benalmadena', 'Bend', 'Bendigo', 'Benevento', 'Benicàssim', 'Benidorm', 'Bergamo', 'Bergen', 'Bergerac', 'Berkeley', 'Berlin', 'Bern', 'Besançon', 'Bethlehem', 'Beverly Hills', 'Béziers', 'Biarritz', 'Biel/Bienne', 'Bielefeld', 'Biella', 'Bilbao', 'Billings', 'Biloxi', 'Birmingham (UK)', 'Birmingham (U.S.)', 'Bishkek', 'Bismarck', 'Bissau', 'Blanes', 'Bled', 'Blois', 'Bloomington', 'Blumenau', 'Boca Chica', 'Boca Raton', 'Bochum', 'Bodrum', 'Bogotá', 'Boise', 'Bologna', 'Bolzano', 'Bonifacio', 'Bonn', 'Bordeaux', 'Bordighera', 'Bormio', 'Boston', 'Boulder', 'Boulogne-sur-Mer', 'Bourges', 'Bowling Green', 'Boynton Beach', 'Bozeman', 'Bradenton', 'Bradford', 'Braga', 'Brampton', 'Brasilia', 'Bratislava', 'Braunschweig', 'Brazzaville', 'Breda', 'Bregenz', 'Brela', 'Bremen', 'Bremerhaven', 'Brescia', 'Brest', 'Briançon', 'Bridgeport', 'Bridgetown', 'Brighton', 'Brindisi', 'Brisbane', 'Bristol', 'Brixen', 'Brixental', 'Brno', 'Brookings', 'Brownsville', 'Bruges', 'Brussels', 'Bucharest', 'Budapest', 'Budva', 'Buenos Aires', 'Buffalo', 'Bujumbura', 'Burgas', 'Burlington', 'Burnt Pine', 'Butte', 'Cabo San Lucas', 'Cadaqués', 'Cádiz', 'Caen', 'Cagliari', 'Cagnes-sur-Mer', 'Cairns', 'Cairo', 'Cala Bona', "Cala d'Or", 'Cala Millor', 'Cala Ratjada', 'Calais', 'Calella', 'Calgary', 'Cali', 'Caloundra', 'Calp', 'Caltanissetta', 'Calvi', 'Cambridge (UK)', 'Cambridge (U.S.)', 'Cambrils', 'Camden', 'Campinas', 'Campobasso', 'Can Pastilla', 'Can Picafort', 'Canazei', 'Canberra', 'Cancun', 'Cannes', 'Cannon Beach', 'Canterbury', 'Canton', 'Canyamel', 'Capdepera', 'Cape Canaveral', 'Cape Coral', 'Cape May', 'Cape Town', 'Capitola', 'Caracas', 'Carbonia', 'Carcassonne', 'Cardiff', 'Carlisle', 'Carlsbad', 'Carmel-by-the-Sea', 'Carpi', 'Carpinteria', 'Carrara', 'Carson City', 'Cartagena (Colombia)', 'Cartagena (Spain)', 'Casablanca', 'Caserta', 'Casper', 'Cassis', 'Castellón de la Plana', 'Castelrotto', 'Castletown', 'Castries', 'Catania', 'Catanzaro', 'Caxias do Sul', 'Cayenne', 'Cedar Rapids', 'Celle', 'Cervinia', 'Cesena', 'Český Krumlov', 'Çeşme', 'Chamonix', 'Chandler', 'Chania', 'Charleroi', 'Charleston (West Virginia)', 'Charleston (South Carolina)', 'Charlestown', 'Charlotte', 'Charlotte Amalie', 'Charlottetown', 'Chartres', 'Chatham', 'Chattanooga', 'Chelmsford', 'Chemnitz', 'Chennai', 'Cherbourg', 'Chesapeake', 'Chester', 'Cheyenne', 'Chiang Mai', 'Chiang Rai', 'Chiavari', 'Chicago', 'Chichester', 'Chiclayo', 'Chieti', 'Chincoteague', 'Chioggia', 'Chios', 'Chișinău', 'Chonburi', 'Christchurch', 'Christiansted', 'Chula Vista', 'Chur', 'Cincinnati', 'Ciutadella de Menorca', 'Civitavecchia', 'Clarksville', 'Clearwater', 'Clermont-Ferrand', 'Cleveland', 'Cockburn Town', 'Cocoa Beach', 'Coconut Creek', 'Coimbra', 'Collioure', 'Colmar', 'Cologne', 'Colombo', 'Colón', 'Colonia del Sacramento', 'Colorado Springs', 'Columbia (South Carolina)', 'Columbia (Missouri)', 'Columbus', 'Como', 'Conakry', 'Concepción', 'Concord', 'Conil de la Frontera', 'Conway', 'Copenhagen', 'Coral Springs', 'Córdoba (Argentina)', 'Córdoba (Spain)', 'Corfu', 'Corinth', 'Cork', 'Coro', 'Corpus Christi', 'Corralejo', "Cortina d'Ampezzo", 'Cosenza', 'Costa Adeje', 'Cottbus', 'Courchevel', 'Courmayeur', 'Coventry', 'Covington', 'Coxen Hole', 'Coyhaique', 'Cozumel', 'Crans-Montana', 'Cremona', 'Crotone', 'Cruz Bay', 'Cuenca (Ecuador)', 'Cuenca (Spain)', 'Cumaná', 'Cuneo', 'Cusco', 'Da Nang', 'Dachau', 'Dahab', 'Dakar', 'Dallas', 'Damascus', 'Dana Point', 'Dar es Salaam', 'Darmstadt', 'Darwin', 'Daugavpils', 'Dauphin Island', 'Davenport', 'Davos', 'Dayton', 'Daytona Beach', 'Deauville', 'Decatur', 'Deerfield Beach', 'Del Mar', 'Delft', 'Delhi', 'Delray Beach', 'Den Bosch', 'Denia', 'Denton', 'Denver', 'Derby', 'Derry', 'Des Moines', 'Detroit', 'Dhaka', 'Didim', 'Dieppe', 'Dijon', 'Dili', 'Djibouti', 'Dodoma', 'Doha', 'Dolomiti Superski', 'Dordrecht', 'Dorfgastein', 'Dortmund', 'Dothan', 'Douala', 'Douglas', 'Dover (Delaware)', 'Dover (New Hampshire)', 'Dresden', 'Dubai', 'Dublin', 'Dubrovnik', 'Duisburg', 'Duluth', 'Dundalk', 'Dundee', 'Dunedin', 'Dunkirk', 'Durham (UK)', 'Durham (U.S.)', 'Dushanbe', 'Düsseldorf', 'Eastbourne', 'Eau Claire', 'Edgartown', 'Edinburgh', 'Edmonton', 'Eilat', 'Eindhoven', 'El Paso', 'Elche', 'Elizabeth', 'Elko', 'Ellmau', 'Elm', 'Empuriabrava', 'Encinitas', 'Engelberg', 'Enna', 'Enschede', 'Épinal', 'Erfurt', 'Erie', 'Erlangen', 'Esbjerg', 'Espace Killy', 'Essaouira', 'Essen', 'Estepona', 'Eugene', 'Eureka', 'Evansville', 'Everett', 'Exeter', 'Èze', 'Faenza', 'Fairbanks', 'Fakaofo', 'Falmouth', 'Famagusta', 'Fano', 'Fargo', 'Faro', 'Fayetteville (North Carolina)', 'Fayetteville (Arkansas)', 'Fermo', 'Fernandina Beach', 'Ferrara', 'Fethiye', 'Fez', 'Fieberbrunn', 'Filzmoos', 'Finale Ligure', 'Fiumicino', 'Flagstaff', 'Flaine', 'Flint', 'Florence', 'Florence (Alabama)', 'Flores', 'Foggia', 'Folgarida', 'Fontana', 'Forlì', 'Fort Collins', 'Fort Lauderdale', 'Fort Myers', 'Fort Smith', 'Fort Wayne', 'Fort Worth', 'Fort-de-France', 'Forte dei Marmi', 'Foz do Iguaçu', 'Frankfort', 'Frankfurt am Main', 'Franklin', 'Frederick', 'Fredericton', 'Frederiksted', 'Freeport', 'Freetown', 'Freiburg', 'Fremont', 'Fresno', 'Fribourg', 'Frosinone', 'Fuengirola', 'Fujairah', 'Fukuoka', 'Funafuti', 'Funchal', 'Gaborone', 'Gainesville', 'Galtür', 'Galway', 'Gandia', 'Garden Grove', 'Garland', 'Gastonia', 'Gatineau', 'Gaza City', 'Gdansk', 'Gdynia', 'Geelong', 'Gelsenkirchen', 'Geneva', 'Genoa', 'George Town (Cayman Islands)', 'George Town (Malaysia)', 'Georgetown', 'Ghent', 'Gijón', 'Gilbert', 'Girona', 'Gitega', 'Giza', 'Glasgow', 'Glendale (Arizona)', 'Glendale (California)', 'Gloucester', 'Gold Coast', 'Gorizia', 'Dachstein-West', 'Gothenburg', 'Göttingen', 'Gouda', 'Granada (Spain)', 'Granada (Nicaragua)', 'Grand Forks', 'Grand Island', 'Grand Junction', 'Grand Prairie', 'Grand Rapids', 'Granville', 'Grasse', 'Graz', 'Great Falls', 'Greeley', 'Green Bay', 'Greensboro', 'Greenville NC', 'Greenville SC', 'Grenoble', 'Grindelwald', 'Groningen', 'Grossarl', 'Grosseto', 'Grover Beach', 'Gstaad', 'Guadalajara', 'Guadalupe', 'Guangzhou', 'Guatemala City', 'Guayaquil', 'Guimarães', 'Gulf Shores', 'Gulfport', 'Gustavia', 'Haarlem', 'Haifa', 'Half Moon Bay', 'Halifax', 'Halle', 'Hamburg', 'Hamilton (Bermuda)', 'Hamilton (Canada)', 'Hamilton (New Zealand)', 'Hampton', 'Hanford', 'Hangzhou', 'Hannover', 'Hanoi', 'Harare', 'Hargeisa', 'Harrisburg', 'Hartford', 'Hasselt', 'Hastings', 'Hat Yai', 'Hattiesburg', 'Havana', 'Heidelberg', 'Heilbronn', 'Heiligenblut', 'Helena', 'Helsinki', 'Henderson', 'Heraklion', 'Herceg Novi', 'Hereford', 'Hermosa Beach', 'Hervey Bay', 'Hialeah', 'Hillsboro', 'Hinterglemm', 'Hinterstoder', 'Hiroshima', 'Hoi An', 'Hobart', 'Ho Chi Minh City', 'Holbrook', 'Hollywood (Florida)', 'Honfleur', 'Hong Kong', 'Honiara', 'Honolulu', 'Horsens', 'Hot Springs', 'Houston', 'Hua Hin', 'Hue', 'Huntington', 'Huntington Beach', 'Huntsville', 'Hurghada', 'Hvar', 'Hyères', 'Ibiza Town', 'Imola', 'Imperia', 'Inca', 'Indianapolis', 'Ingolstadt', 'Innsbruck', 'Interlaken', 'Inverness', 'Ioannina', 'Iqaluit', 'Iquitos', 'Irvine', 'Irving', 'Ischgl', 'Isernia', 'Lahore', 'Islamorada', 'Istanbul', 'İzmir', 'Izola', 'Jackson', 'Jackson (Tennessee)', 'Jacksonville', 'Jaipur', 'Jefferson City', 'Jena', 'Jerez de la Frontera', 'Jersey City', 'Jerusalem', 'Johannesburg', 'Johnson City', 'Joinville', 'Jonesboro', 'Juan Griego', 'Juan-les-Pins', 'Juba', 'Juiz de Fora', 'Juneau', 'Jungfrau', 'Jupiter', 'Jūrmala', 'Kabul', 'Kaiserslautern', 'Kalamata', 'Kalamazoo', 'Kampala', 'Kanchanaburi', 'Kansas City', 'Kansas City (Kansas)', 'Kappl', 'Kaprun', 'Islamabad', 'Karlovy Vary', 'Karlsruhe', 'Kassel', 'Kastoria', 'Kathmandu', 'Kaunas', 'Kavala', 'Kearney', 'Keene', 'Kemer', 'Kenosha', 'Key Largo', 'Key West', 'Khao Lak', 'Khartoum', 'Kiel', 'Kigali', 'Kilkenny', 'Kingman', 'Kingston (Jamaica)', 'Kingston (Norfolk Island)', 'Kingston upon Hull', 'Kingstown', 'Kinshasa', 'Kissimmee', 'Kitzbühel', 'Klagenfurt', 'Klaipėda', 'Knoxville', 'Kobe', 'Koblenz', 'Kolding', 'Kolkata', 'Komotini', 'Koper', 'Koror', 'Kos', 'Košice', 'Kotor', 'Krabi', 'Krakow', 'Kralendijk', 'Krefeld', 'Kuah', 'Kuala Lumpur', 'Kuşadası', 'Kutná Hora', 'Kuwait City', 'Kyiv', 'Kyoto', 'Kyrenia', 'La Ceiba', 'La Ciotat', 'La Clusaz', 'La Laguna', 'La Maddalena', 'La Manga', 'La Paz', 'La Plagne', 'La Plata', 'La Rochelle', 'La Romana', 'La Serena', 'La Seyne-sur-Mer', 'La Spezia', 'La Thuile', 'Laax', 'Labasa', 'Lafayette (Indiana)', 'Lafayette (Louisiana)', 'Lagos (Nigeria)', 'Lagos (Portugal)', 'Laguna Beach', 'Karachi', 'Lakeland', 'Lalitpur', 'Lamezia Terme', 'Lancaster', 'Lancaster (U.S.)', 'Landshut', 'Lansing', "L'Aquila", 'Laredo', 'Largo', 'Larnaca', 'Las Cruces', 'Las Palmas', 'Las Vegas', 'Latina', 'Lausanne', 'Lautoka', 'Laval', 'Lawton', 'Layton', 'Le Havre', 'Le Lavandou', 'Le Mans', 'Le Puy-en-Velay', 'Lecce', 'Lecco', 'Lech', 'Leeds', 'Legnano', 'Leicester', 'Leiden', 'Leipzig', 'Lemgo', 'Leogang', 'León', 'Les Arcs', 'Les Deux Alpes', 'Les Gets', 'Les Houches', 'Les Menuires', 'Leuven', 'Leverkusen', 'Lexington', 'Liberec', 'Libreville', 'Lichfield', 'Liège', 'Lienz', 'Liepāja', 'Lille', 'Lilongwe', 'Lima', 'Limassol', 'Limerick', 'Limoges', 'Lincoln', 'Lincoln', 'Lindos', 'Linz', 'Lisbon', 'Lisburn', 'Little Rock', 'Liverpool', 'Livigno', 'Livorno', 'Ljubljana', 'Lloret de Mar', 'Llucmajor', 'Loano', 'Locarno', 'Lodi', 'Lodz', 'Logan', 'Logroño', 'Lomé', 'London (Canada)', 'London (UK)', 'Londrina', 'Long Beach', 'Long Beach (New York)', 'Long Branch', 'Longview (Texas)', 'Longview (Washington)', 'Lorain', 'Los Alamos', 'Los Angeles', 'Los Cabos', 'Los Cristianos', 'Louisville', 'Lourdes', 'Loutraki', 'Louvain-la-Neuve', 'Lowell', 'Luanda', 'Lubbock', 'Lübeck', 'Lublin', 'Lucca', 'Lucerne', 'Lugano', 'Luganville', 'Lund', 'Lusaka', 'Luxembourg', 'Luxor', 'Lyon', 'Maastricht', 'Macerata', 'Machu Picchu', 'Macon', 'Madera', 'Madison', 'Madonna di Campiglio', 'Madrid', 'Magaluf', 'Magdeburg', 'Mahón', 'Mainz', 'Majuro', 'Makarska', 'Malabo', 'Malaga', 'Maldonado', 'Malé', 'Malia', 'Malibu', 'Malmö', 'Manacor', 'Managua', 'Manama', 'Manchester (UK)', 'Manchester (U.S.)', 'Máncora', 'Manhattan Beach', 'Manhattan, KS', 'Mannheim', 'Manosque', 'Mantua', 'Maputo', 'Mar del Plata', 'Maracaibo', 'Marathon', 'Marbella', 'Maria Alm', 'Maribor', 'Marigot', 'Markham', 'Marmaris', 'Maroochydore', 'Marquette', 'Marrakesh', 'Marsa Alam', 'Marsala', 'Marseille', 'Martigues', 'Masaya', 'Maseru', 'Maspalomas', 'Massa', 'Matera', 'Mayrhofen', 'Mazara del Vallo', 'Mbabane', 'McKinney', 'Mechelen', 'Medellín', 'Medford', 'Megève', 'Melbourne (Australia)', 'Melbourne (U.S.)', 'Memphis', 'Menton', 'Merano', 'Merced', 'Meribel', 'Mérida (Spain)', 'Mérida (Venezuela)', 'Meridian', 'Mesa', 'Messina', 'Mestre', 'Metz', 'Mexico City', 'Miami', 'Middelburg', 'Midland', 'Mijas', 'Milan', 'Milford', 'Millau', 'Milwaukee', 'Mindelo', 'Minneapolis', 'Minot', 'Minsk', 'Miramar', 'Mishawaka', 'Mississauga', 'Missoula', 'Moab', 'Mobile', 'Modena', 'Modesto', 'Modica', 'Moena', 'Mogadishu', 'Mogi das Cruzes', 'Mombasa', 'Monaco City', 'Mönchengladbach', 'Monrovia (Liberia)', 'Monrovia (U.S.)', 'Mons', 'Monschau', 'Monte Carlo', 'Monte Rosa', 'Montego Bay', 'Montepulciano', 'Monterey', 'Montevideo', 'Montgomery', 'Montluçon', 'Montpelier', 'Montpellier', 'Montreal', 'Montreux', 'Monza', 'Moraira', 'Moreno Valley', 'Morgantown', 'Moroni', 'Morro Bay', 'Morzine', 'Moscow', 'Mount Vernon', 'Mountain View', 'Moutier', 'Mulhouse', 'Mumbai', 'Munich', 'Münster', 'Murcia', 'Murfreesboro', 'Murter', 'Mykonos', 'Mytilene', 'Nadi', 'Nafplio', 'Nagoya', 'Nags Head', 'Nairobi', 'Namur', 'Nancy', 'Nantes', 'Napa', 'Naples (Italy)', 'Naples (U.S.)', 'Narbonne', 'Narva', 'Nashua', 'Nashville', 'Nassau', 'Naxos', 'Nazareth', "N'Djamena", 'Negril', 'Neiafu', 'Nelson', 'Nerja', 'Netanya', 'Nevers', 'New Haven', 'New London', 'New Orleans', 'New Smyrna Beach', 'New York City', 'Newark', 'Newcastle (Australia)', 'Newcastle (UK)', 'Newport (UK)', 'Newport (Rhode Island)', 'Newport (Vermont)', 'Newport Beach', 'Newport News', 'Newry', 'Ngerulmud', 'Nha Trang', 'Niagara Falls', 'Niamey', 'Nice', 'Nicosia', 'Nijmegen', 'Nimes', 'Niort', 'Noosa Heads', 'Norfolk', 'Normal', 'Norman', 'North Las Vegas', 'North Port', 'Norwalk', 'Norwich', 'Nottingham', 'Nouakchott', 'Novara', 'Novigrad', 'Nukuʻalofa', 'Nukunonu', 'Nuoro', 'Nürnberg', 'Nur-Sultan', 'Nuuk', 'Nyon', 'Oakland', 'Oaxaca', 'Obergurgl', 'Oberhausen', 'Ocala', 'Ocean City', 'Ocean Grove', 'Oceanside', 'Ocho Rios', 'Odense', 'Odessa', 'Ogden', 'Oia', 'Oklahoma City', 'Olbia', 'Oldenburg', 'Olomouc', 'Olympia', 'Omaha', 'Omoa', 'Opatija', 'Orange Beach', 'Oranjestad (Aruba)', 'Oranjestad (Sint Eustatius)', 'Orem', 'Oristano', 'Orlando', 'Orléans', 'Ortisei', 'Osaka', 'Oshkosh', 'Oslo', 'Osnabrück', 'Ostrava', 'Ottawa', 'Ouagadougou', 'Oulu', 'Ourense', 'Overland Park', 'Oviedo', 'Owensboro', 'Oxford', 'Oxnard', 'Pacific Grove', 'Paderborn', 'Padova', 'Pago Pago', 'Palanga', 'Palavas-les-Flots', 'Palermo', 'Palikir', 'Palm Bay', 'Palm Beach', 'Palm Springs', 'Palma de Mallorca', 'Palma Nova', 'Palmetto', 'Palo Alto', 'Pamplona', 'Panama City (U.S.)', 'Panama City (Panama)', 'Paphos', 'Paradiski', 'Paralia', 'Paramaribo', 'Parikia', 'Paris', 'Parkersburg', 'Parma', 'Pärnu', 'Pasadena', 'Passo del Tonale', 'Passo Rolle', 'Paterson', 'Patras', 'Pattaya', 'Pau', 'Pavia', 'Peel', 'Peguera', 'Pembroke Pines', 'Peniscola', 'Pensacola', 'Peoria', 'Perast', 'Périgueux', 'Perpignan', 'Perros-Guirec', 'Perth (Australia)', 'Perth (UK)', 'Perugia', 'Pesaro', 'Pescara', 'Pescasseroli', 'Petah Tikva', 'Peterborough', 'Petra', 'Petrovac', 'Pforzheim', 'Phang Nga', 'Phetchabun', 'Philadelphia', 'Philipsburg', 'Phoenix', 'Phuket City', 'Piacenza', 'Pierre', 'Pine Bluff', 'Piraeus', 'Piran', 'Pisa', 'Pistoia', 'Pittsburgh', 'Placencia', 'Plano', 'Playa Blanca', 'Playa de las Américas', 'Playa del Carmen', 'Pleasure Point', 'Plovdiv', 'Plymouth', 'Plzeň', 'Podgorica', 'Pointe-à-Pitre', 'Poitiers', 'Pollença', 'Pompano Beach', 'Pontevedra', 'Pordenone', 'Poreč', 'Porlamar', 'Port Angeles', 'Port Charlotte', "Port d'Andratx", 'Port Louis', 'Port Moresby', 'Port of Spain', 'Port St. Lucie', 'Port Townsend', 'Port Vila', 'Port-au-Prince', 'Portimão', 'Portland (Oregon)', 'Portland (Maine)', 'Porto', 'Porto Cervo', 'Porto Cristo', 'Porto Torres', 'Portocolom', 'Portoferraio', 'Portofino', 'Porto-Novo', 'Portorož', 'Porto-Vecchio', 'Portsmouth (UK)', 'Portsmouth (U.S.)', 'Positano', 'Potenza', 'Potsdam', 'Poznan', 'Pozzuoli', 'Prague', 'Praia', 'Praia da Rocha', 'Prato', 'Prescott', 'Preston', 'Pretoria', 'Pristina', 'Propriano', 'Protaras', 'Providence', 'Provincetown', 'Provo', 'Pueblo', 'Puerto Baquerizo Moreno', 'Puerto Cortés', 'Puerto de la Cruz', 'Puerto la Cruz', 'Puerto Plata', 'Puerto Rico de Gran Canaria', 'Puerto Vallarta', 'Pula', 'Punta Arenas', 'Punta Cana', 'Punta del Este', 'Punta Gorda', 'Pyeongchang', 'Pyongyang', 'Quarteira', 'Quebec', 'Quetzaltenango', 'Quimper', 'Quito', 'Rabat', 'Racine', 'Ragusa', 'Railay Beach', 'Raleigh', 'Ramallah', 'Ramsey', 'Rancho Cucamonga', 'Randers', 'Rapallo', 'Rapid City', 'Ras al-Khaimah', 'Ras Sedr', 'Ratingen', 'Ravello', 'Ravenna', 'Rayong', 'Reading', 'Redding', 'Redondo Beach', 'Regensburg', 'Reggio Calabria', 'Reggio Emilia', 'Regina', 'Rehovot', 'Reims', 'Rennes', 'Reno', 'Rethymno', 'Reus', 'Reutlingen', 'Reykjavik', 'Rhodes', 'Richmond', 'Rieti', 'Riga', 'Rijeka', 'Rimini', 'Rio de Janeiro', 'Riomaggiore', 'Rishon LeZion', 'Rivas', 'Riverside', 'Riviera Maya', 'Road Town', 'Roanoke', 'Rocamadour', 'Rochester (Minnesota)', 'Rochester (New York)', 'Rock Hill', 'Rockford', 'Rockville', 'Rodez', 'Rogers', 'Rome', 'Ronda', 'Rosario', 'Roseau', 'Roskilde', 'Rostock', 'Roswell', 'Rotterdam', 'Roubaix', 'Rouen', 'Rovigo', 'Rovinj', 'Rutland', 'Sa Coma', 'Sa Pobla', 'Saalbach', 'Saarbrücken', 'Saas-Fee', 'Sacramento', 'Safaga', 'Saint Paul', 'Saint Petersburg', 'Saint-Brieuc', 'Sainte-Maxime', 'Saintes-Maries-de-la-Mer', 'Saint-Étienne', 'Saint-Jean-Cap-Ferrat', 'Saint-Laurent-du-Maroni', 'Saint-Malo', 'Saint-Tropez', 'Salamanca', 'Salem (Oregon)', 'Salem (Massachusetts)', 'Salerno', 'Salinas', 'Salisbury', 'Salou', 'Salt Lake City', 'Salta', 'Salvador', 'Salzburg', 'Samaná', 'San Angelo', 'San Antonio', 'San Bernardino', 'San Clemente', 'San Cristóbal', 'San Diego', 'San Francisco', 'San José (Costa Rica)', 'San Jose (U.S.)', 'San Juan', 'San Juan del Sur', 'San Lorenzo', 'San Luis Obispo', 'San Marino', 'San Mateo', 'San Miguel', 'San Pedro', 'San Pedro de Atacama', 'San Pedro Sula', 'San Rafael', 'San Salvador', 'San Sebastián', 'Sanaa', 'Sanford', 'Sanremo', 'Sant Antoni de Portmany', 'Santa Ana (U.S.)', 'Santa Ana (El Salvador)', 'Santa Barbara', 'Santa Clara', 'Santa Clarita', 'Santa Cruz', 'Santa Cruz de la Sierra', 'Santa Cruz de Tenerife', 'Santa Eulària des Riu', 'Santa Fe', 'Santa Lucía', 'Santa Margherita Ligure', 'Santa Maria (Cape Verde)', 'Santa Maria (U.S.)', 'Santa Monica', 'Santa Pola', 'Santa Ponsa', 'Santa Rosa', 'Santa Tecla', 'Santander', 'Santanyí', 'Santiago (Chile)', 'Santiago (Dominican Rep.)', 'Santiago de Compostela', 'Santo Domingo', 'Sao Paulo', 'São Tomé', 'Sapporo', 'Sarajevo', 'Sarasota', 'Saratoga Springs', "S'Arenal", 'Sarlat-la-Canéda', 'Saskatoon', 'Sassari', 'Saumur', 'Savannah', 'Savona', 'Savusavu', 'Schaffhausen', 'Schenectady', 'Schladming', 'Scottsdale', 'Scranton', 'Sea Isle City', 'Seal Beach', 'Seaside', 'Seattle', 'Sedona', 'Seefeld', 'Segovia', 'Seoul', 'Serre Chevalier', 'Sète', 'Seville', 'Shanghai', 'Sharjah', 'Sharm el-Sheikh', 'Sheffield', 'Shenzhen', 'Shreveport', 'Šiauliai', 'Šibenik', 'Side', 'Siegen', 'Siena', 'Sineu', 'Singapore', 'Sion', 'Sioux City', 'Sioux Falls', 'Sitges', 'Skiathos', 'Skopje', 'Sofia', 'Sölden', 'Söll', 'Soller', 'Solothurn', 'Sondrio', 'Sopot', 'Sorocaba', 'Sorrento', 'South Bend', 'Southampton', 'Split', 'Spokane', 'Springdale', 'Springfield (Illinois)', 'Springfield (Massachusetts)', 'Springfield (Missouri)', 'Springfield (Oregon)', 'St Albans', "St George's (Bermuda)", 'St. Albans', 'St. Anton', 'St. Augustine', 'St. Cloud', 'St. Gallen', 'St. George', "St. George's (Grenada)", "St. John's (Antigua and Barbuda)", "St. John's (Canada)", 'St. Louis', 'St. Moritz', 'St. Petersburg (U.S.)', 'Stamford', 'Stanley', 'Stavanger', 'Stillwater', 'Stirling', 'Stockholm', 'Stockton', 'Stoke-on-Trent', 'Stone Harbor', 'Strasbourg', 'Stuttgart', 'Sucre', 'Suez', 'Sukhothai', 'Sumter', 'Sunderland', 'Sunnyvale', 'Sunshine Coast', 'Superior', 'Surrey', 'Suva', 'Sveti Stefan', 'Swansea', 'Sydney', 'Syracuse (Italy)', 'Syracuse (U.S.)', 'Szczecin', 'Taba', 'Tacoma', 'Taipei', 'Tallahassee', 'Tallinn', 'Tampa', 'Tampere', 'Tamworth', 'Tangier', 'Taormina', 'Taranto', 'Tarifa', 'Tarragona', 'Tartu', 'Tashkent', 'Tauplitz', 'Tauranga', 'Tavira', 'Tbilisi', 'Tegucigalpa', 'Tel Aviv', 'Temecula', 'Tempe', 'Teramo', 'Terni', 'Texarkana AR', 'Texarkana TX', 'The Bottom', 'The Hague', 'The Valley', 'The Woodlands', 'Thessaloniki', 'Thimphu', 'Tignes', 'Tijuana', 'Tilburg', 'Tinos', 'Tirana', 'Tivat', 'Tivoli', 'Tokyo', 'Toledo (Spain)', 'Toledo (U.S.)', 'Tooele', 'Toowoomba', 'Topeka', 'Toronto', 'Torre del Greco', 'Torre del Mar', 'Torremolinos', 'Torrevieja', 'Tórshavn', 'Toruń', 'Tossa de Mar', 'Toulon', 'Toulouse', 'Tours', 'Townsville', 'Trani', 'Trapani', 'Trento', 'Trenton', 'Treviso', 'Trier', 'Trieste', 'Tripoli', 'Trogir', 'Tromsø', 'Trondheim', 'Trouville-sur-Mer', 'Troy', 'Troyes', 'Trujillo', 'Tucson', 'Tui', 'Tulsa', 'Tulum', 'Turin', 'Turku', 'Tuscaloosa', 'Twin Falls', 'Two Harbors', 'Tybee Island', 'Tyler', 'Udine', 'Udon Thani', 'Ukiah', 'Ulaanbaatar', 'Ulcinj', 'Ulm', 'Umag', 'Uppsala', 'Urbino', 'Urubamba', 'Ushuaia', 'Utica', 'Utrecht', 'Vaduz', 'Val d’Isère', 'Val di Fassa', 'Val Gardena', 'Val Thorens', 'Valence', 'Valencia (Spain)', 'Valencia (Venezuela)', 'Valladolid', 'Valldemossa', 'Valle Isarco', 'Valletta', 'Valparaíso', 'Vancouver (Canada)', 'Vancouver (U.S.)', 'Varazze', 'Varese', 'Varna', 'Vaughan', 'Vejle', 'Venice (Italy)', 'Venice (U.S.)', 'Ventimiglia', 'Ventspils', 'Ventura', 'Verbania', 'Verbier', 'Vercelli', 'Vero Beach', 'Verona', 'Versailles', 'Vevey', 'Viareggio', 'Vibo Valentia', 'Viborg', 'Vicenza', 'Vichy', 'Victoria (Canada)', 'Victoria (Seychelles)', 'Victorville', 'Vienna', 'Vigo', 'Vilamoura', 'Villach', 'Villefranche-sur-Mer', 'Vilnius', 'Viña del Mar', 'Virginia Beach', 'Visalia', 'Viterbo', 'Vitoria-Gasteiz', 'Volos', 'Vrsar', 'Waco', 'Wakefield', 'Warsaw', 'Warth', 'Washington D.C.', 'Waterford', 'Watertown', 'Watsonville', 'Waukegan', 'Waukesha', 'Wellington (New Zealand)', 'Wellington (U.S.)', 'Wengen', 'Weno', 'West Lafayette', 'West Palm Beach', 'Westendorf', 'Westminster', 'Weston', 'Wheeling', 'White Plains', 'Whitehorse', 'Wichita', 'Wichita Falls', 'Wiesbaden', 'Wildwood', 'Wilkes-Barre', 'Willemstad', 'Williams', 'Wilmington (Delaware)', 'Wilmington (North Carolina)', 'Winchester', 'Windhoek', 'Windsor', 'Winnipeg', 'Winslow', 'Winston–Salem', 'Winterthur', 'Wolfsburg', 'Wollongong', 'Wolverhampton', 'Woodburn', 'Worcester (UK)', 'Worcester (U.S.)', 'Worthing', 'Wroclaw', 'Wuppertal', 'Würzburg', 'Yakima', 'Yamoussoukro', 'Yaoundé', 'Yaren', 'Yellowknife', 'Yerevan', 'Yokohama', 'Yonkers', 'York (UK)', 'York (U.S.)', 'Youngstown', 'Yuma', 'Zadar', 'Zagreb', 'Zakopane', 'Zanzibar', 'Zaragoza', 'Zell am See', 'Zell am Ziller', 'Zermatt', 'Zug', 'Zurich', 'Zwickau', 'Zwolle']

async def get_cities(ctx: discord.AutocompleteContext):
    return [location for location in cities if location.startswith(ctx.value.upper())]

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

async def get_airports_o(ctx: discord.AutocompleteContext):
    return [origin for origin in airports if origin.startswith(ctx.value.upper())]

async def get_airports_d(ctx: discord.AutocompleteContext):
    return [destination for destination in airports if destination.startswith(ctx.value.upper())]
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
    await channel.send(f"{interaction.user.mention} continue here, run </va training:1038015187011260436> and input your desired destination and origin.")
@va.command(name="roles", description="roles")
@commands.has_role(1006725140933001246)
async def varoles(ctx):
  embed = discord.Embed(title="The ClearFly VA", description="""
  **How to fly for the VA**

-Click the button below

======**GENERAL TRAINING**======

{-Run the command </va training:1038015187011260436>
{-Enter your desired origin and destination
{-Wait for an instructor to approve and assign you required information
{-Do the flight witht the C172(steam gauges)
{-Share screenshots of the flight, in one of those screenshots there should be the G430 with the flightplan __clearly visible__
⌞______**2X**______⌟
-------------------------------------------------------------------
{-Run the command </va training:1038015187011260436> again
{-Enter your desired origin and destination
{-Wait for an instructor to approve and assign you required information
{-Do the flight witht the C172(G1000)
{-Share screenshots of the flight, let us see that you can use the autopilot
⌞______**2X**______⌟
-------------------------------------------------------------------
-An instructor will check you off, so you're ready to go to the next phase, type rating!

======**TYPE RATING**======

-Run the command </va training:1038015187011260436>
-Choose the aircraft you want in the dropdown menu
{-Run the command </va training:1038015187011260436> again
{-Enter your desired origin and destination
{-Wait for an instructor to approve and assign you required information
{-Share screenshots of the flight were we can see that you are able to use the plane(this includes autopilot except if you're fitted without any navigation system on the B732)
⌞______**2X**______⌟
-An instructor will check you off once again for the final time, you can then fly as much as you want for the VA!""", color=cfc)
  await ctx.send(embed=embed, view=InfoB4training
())
  await ctx.respond("however, your mom", ephemeral=True)

class TypeView(discord.ui.View):
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
                label="Airbus A300-600",
                description="By iniSimulations"
            ),
            discord.SelectOption(
                label="Airbus A300-600F",
                description="By iniSimulations"
            )
        ]
    )
    async def select_callback(self, select, interaction):
      config = configparser.ConfigParser()

      if select.values[0] == "Boeing 737-200":
        embed = discord.Embed(title="You have selected the Boeing 737-200 as your type rating.", description="Run  </va training:1038015187011260436> again to file your first flight.", color=cfc)
        await interaction.response.send_message(embed=embed)
        config.read(f"ClearFly_VA/users/{interaction.user.id}/student.ini")
        config.set("Student","typed", "1")
        config.set("Student","type", "B732")
        with open(f"ClearFly_VA/users/{interaction.user.id}/student.ini", "w") as configfile:
            config.write(configfile)
      
      if select.values[0] == "Boeing 737-800":
        embed = discord.Embed(title="You have selected the Boeing 737-800 as your type rating.", description="Run  </va training:1038015187011260436> again to file your first flight.", color=cfc)
        await interaction.response.send_message(embed=embed)
        config.read(f"ClearFly_VA/users/{interaction.user.id}/student.ini")
        config.set("Student","typed", "1")
        config.set("Student","type", "B738")
        with open(f"ClearFly_VA/users/{interaction.user.id}/student.ini", "w") as configfile:
            config.write(configfile)
      
      if select.values[0] == "Airbus A300-600":
        embed = discord.Embed(title="You have selected the Airbus A300-600 as your type rating.", description="Run  </va training:1038015187011260436> again to file your first flight.", color=cfc)
        await interaction.response.send_message(embed=embed)
        config.read(f"ClearFly_VA/users/{interaction.user.id}/student.ini")
        config.set("Student","typed", "1")
        config.set("Student","hasAccess", "0")
        config.set("Student","type", "A306")
        with open(f"ClearFly_VA/users/{interaction.user.id}/student.ini", "w") as configfile:
            config.write(configfile)
      
      if select.values[0] == "Airbus A300-600F":
        embed = discord.Embed(title="You have selected the Airbus A300-600F as your type rating.", description="Run  </va training:1038015187011260436> again to file your first flight.", color=cfc)
        await interaction.response.send_message(embed=embed)
        config.read(f"ClearFly_VA/users/{interaction.user.id}/student.ini")
        config.set("Student","typed", "1")
        config.set("Student","type", "A306F")
        with open(f"ClearFly_VA/users/{interaction.user.id}/student.ini", "w") as configfile:
            config.write(configfile)
@va.command(name="training", description="Start your career in the ClearFly VA!")
@option("origin", description="The airport(ICAO) you will fly from.")
@option("destination", description="The airport(ICAO) you will fly to.")
async def vatrain(ctx, origin, destination):
  origin = origin.upper()
  destination = destination.upper()
  user = ctx.author
  config = configparser.ConfigParser()
  guild = bot.get_guild(965419296937365514)
  role = guild.get_role(1040918463763468369)
  if os.path.exists(f"ClearFly_VA/users/{user.id}/student.ini"):
    config.read(f"ClearFly_VA/users/{user.id}/student.ini")
    if config.get("Student", "hasAccess") == "1":
      if config.get("Student", "typed") == "0":
        embed = discord.Embed(title="Choose the aircraf you want to fly!", description="In order to fly for the VA you will need to get a type rating too, to do this select the aircraft you want below and you will be prompted to give origin and a destination. An instructor will approve your flight(just like in your general training), you will need to do 2 flights and then an instructor will check you off once again and then you're good to go to do as many flights for the VA as you want!", color=cfc)
        await ctx.respond(embed=embed,view=TypeView())
      else:
        if config.get("Student", "ready") == "1":
          await ctx.respond("Filing flight.")
          actype = config.get("Student", "type")
          embed = discord.Embed(title="Flight Filed!",description="**Wait for a <@&1040918528565444618> to assign you the required information before flying!**\n\n Show screenshots of you doing the flight for confirmation too!", color=cfc)
          await ctx.edit(content="Filing flight..")
          embed.add_field(name="Flight information:", value=f"""
```
Departure:{origin}
Arrival:{destination}
```
Have a nice and safe flight!
                    """)
          await ctx.edit(content="Filing flight...")
          if os.path.exists(f"ClearFly_VA/users/{user.id}"):
              f = open(f"ClearFly_VA/users/{user.id}/type.txt","a")
              f.write(f"\nType Training {actype} {origin}-{destination}")
              f.close()
          else:
              os.mkdir(f"ClearFly_VA/users/{user.id}")
              f = open(f"ClearFly_VA/users/{user.id}/type.txt","a")
              f.write(f"\nType Training {actype} {origin}-{destination}")
              f.close()
          await ctx.edit(content="Uploading to database.")
          await ctx.edit(content="Uploading to database..")
          config.set("Student", "ready", "0")
          await ctx.edit(content="Uploading to database...")
          with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
              config.write(configfile)
          await ctx.edit(content=None, embed=embed)
          await ctx.send(f"<@&1040918528565444618> someone needs to get in the air for their flight, give them the required info!")
        else:
          await ctx.respond("Wait for an instructor to approve your current flight and after you have done that one you can do another one.")
          return
    else:
      if role in ctx.author.roles:
          icaoprefix = ["K", "E", "L", "P", "T"]
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
                await ctx.edit(content="You have flown 4 times already, wait to get checked off!")
                return
              if config.get("Student", "ready") == "0":
                await ctx.edit(content="Wait for an instructor to approve your current flight and after you have done that one you can do another one.")
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
          sleep(0.1)
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
          await ctx.edit(content="Filing flight..")
          embed = discord.Embed(title="Flight Filed!",description="**Wait for a <@&1040918528565444618> to assign you the required information before flying!**\n\n Show screenshots of you doing the flight for confirmation too!", color=cfc)
          embed.add_field(name=phasetxt, value=f"""
```
Departure:{origin}
Arrival:{destination}
```
Have a nice and safe flight!
                    """)
          await ctx.edit(content="Filing flight...")
          await ctx.edit(content="Filing flight.")
          if os.path.exists(f"ClearFly_VA/users/{user.id}"):
              f = open(f"ClearFly_VA/users/{user.id}/student.txt","a")
              f.write(f"\nTraining {phase}({paneltype}) {origin}-{destination}")
              f.close()
          else:
              os.mkdir(f"ClearFly_VA/users/{user.id}")
              f = open(f"ClearFly_VA/users/{user.id}/student.txt","a")
              f.write(f"\nTraining {phase}({paneltype}) {origin}-{destination}")
              f.close()
          await ctx.edit(content="Uploading to database.")
          await ctx.edit(content="Uploading to database..")
          await ctx.edit(content="Uploading to database...")
          await ctx.edit(content=None, embed=embed)
          await ctx.send(f"<@&1040918528565444618> someone needs to get in the air for their {phasen} flight, give them the required info!")
      else:
        embed = discord.Embed(title="Error 403!", description="You do not have the CF student role. \nGet it in {channel here} before using this command!", color=errorc)
        await ctx.respond(embed=embed)

  else:
    if role in ctx.author.roles:
      icaoprefix = ["K", "E", "L", "P", "T"]
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
        if config.get("Student", "ready") == "0":
          await ctx.edit(content="Wait for an instructor to approve your current flight and after you have done that one you can do another one.")
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
      sleep(0.1)
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
      await ctx.edit(content="Filing flight..")
      embed = discord.Embed(title="Flight Filed!",description="**Wait for a <@&1040918528565444618> to assign you the required information before flying!**\n\n Show screenshots of you doing the flight for confirmation too!", color=cfc)
      embed.add_field(name=phasetxt, value=f"""
      ```
      Departure:{origin}
      Arrival:{destination}
      ```
      Have a nice and safe flight!
                """)
      await ctx.edit(content="Filing flight...")
      await ctx.edit(content="Filing flight.")
      if os.path.exists(f"ClearFly_VA/users/{user.id}"):
          f = open(f"ClearFly_VA/users/{user.id}/student.txt","a")
          f.write(f"\nTraining {phase}({paneltype}) {origin}-{destination}")
          f.close()
      else:
          os.mkdir(f"ClearFly_VA/users/{user.id}")
          f = open(f"ClearFly_VA/users/{user.id}/student.txt","a")
          f.write(f"\nTraining {phase}({paneltype}) {origin}-{destination}")
          f.close()
      await ctx.edit(content="Uploading to database.")
      await ctx.edit(content="Uploading to database..")
      await ctx.edit(content="Uploading to database...")
      await ctx.edit(content=None, embed=embed)
      await ctx.send(f"<@&1040918528565444618> someone needs to get in the air for their {phasen} flight, give them the required info!")
    else:
      embed = discord.Embed(title="Error 403!", description="You do not have the <@&1040918463763468369> role. \nGet it in <#965686982304997466> before using this command!", color=errorc)
      await ctx.respond(embed=embed)

@instructor.command(name="approve", description="Approve a student's flight and give the required info to them.")
@option("comments", required=False)
async def vaapprove(ctx, user: discord.Member, route, crzalt, comments):
  guild = bot.get_guild(965419296937365514)
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
async def vacheckoff(ctx, user: discord.Member):
  guild = bot.get_guild(965419296937365514)
  role = guild.get_role(1040918528565444618)
  if role in user.roles:
    config = configparser.ConfigParser()
    config.read(f"ClearFly_VA/users/{user.id}/student.ini")
    guild = bot.get_guild(965419296937365514)
    role = guild.get_role(1040918463763468369)
    role2 = guild.get_role(1013933799777783849)
    channel = bot.get_channel(1013934267966967848)
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
      with open(f"ClearFly_VA/users/{user.id}/type.txt", "r") as f:
        lines = len(f.readlines())
      if lines == 3:
        if config.get("Student", "end") == "0":
          config.set("Student", "end", "1")
          await user.remove_roles(role)
          await user.add_roles(role2)
          if config.get("Student", "type") == "B732":
            role3 = guild.get_role(1040918288525438996)
          if config.get("Student", "type") == "B738":
            role3 = guild.get_role(1040918323573047366)
          if config.get("Student", "type") == "A306":
            role3 = guild.get_role(1040918215188037633)
          if config.get("Student", "type") == "A306F":
            role3 = guild.get_role(1040918248100737054)
          await user.add_roles(role3)
          config.set("Student","hasAccess","1")
          with open(f"ClearFly_VA/users/{user.id}/student.ini", "w") as configfile:
                config.write(configfile)
          embed = discord.Embed(title=f"{user} has been checked off.", color=cfc)
          await ctx.respond(embed=embed, ephemeral=True)
          embed = discord.Embed(title=f"{user} has fully finished training!", description=f"Congratulations {user.mention}!\n Now you can fly as much as you want for the VA!", colour=cfc, timestamp=datetime.now())
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
@va.command(name="file", descriprion="File a flight that you will do for the Clearfly VA.")
@option("aircraft", description="The aircraft you will use for the flight.(for more aircraft send a dm to WolfAir)", choices=["B732", "B738", "A306", "A306F"])
@option("origin", description="The airport(ICAO) you will fly from.", autocomplete=get_airports_o)
@option("destination", description="The airport(ICAO) you will fly to.", autocomplete=get_airports_d)
async def file(ctx, aircraft, origin, destination):
  config = configparser.ConfigParser()
  if os.path.exists(f"ClearFly_VA/users/{ctx.author.id}/student.ini"):
    config.read(f"ClearFly_VA/users/{ctx.author.id}/student.ini")
    if config.get("Student", "end") == "1":
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
      if aircraft == "B732":
        cf3 = 1
      if aircraft == "B738":
        cf3 = 2
      if aircraft == "A306":
        cf3 = 3
      if aircraft == "A306F":
        cf3 = 4
      if not aircraft == config.get("Student", "type"):
          embed=discord.Embed(title="Error 503!", description="You need to have a type rating of this aircraft if you want to fly it!", color=errorc)
          await ctx.respond(embed=embed)
          return
      user = ctx.author
      await ctx.respond("Filing flight.")
      sleep(0.1)
      await ctx.edit(content="Filing flight..")
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
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1038060095902330952/1038065978019430430/FJS_732_TwinJet_icon11_thumb.png")
      if aircraft == "B738":
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1038060053896364063/1038065018983432242/b738_4k_icon11_thumb.png")
      if aircraft == "A300":
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1013239106198835300/1015290004001542164/A300_P_V2_-_2022-08-31_00.37.05.PNG")
      if aircraft == "A300F":
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1038063084733997178/1038065483234164837/A300_F_V2_icon11_thumb.png")
      await ctx.edit(content=None, embed=embed)
    else:
        embed=discord.Embed(title="Error 503!", description="You need to train before using this command", color=errorc)
        await ctx.respond(embed=embed)
  else:
        embed=discord.Embed(title="Error 503!", description="You need to train before using this command", color=errorc)
        await ctx.respond(embed=embed)

@va.command(name="cancel", description="Cancels and removes your last filed flight.")
async def cancel(ctx):
  config = configparser.ConfigParser()
  if os.path.exists(f"ClearFly_VA/users/{ctx.author.id}/student.ini"):
    config.read(f"ClearFly_VA/users/{ctx.author.id}/student.ini")
    if config.get("Student", "end") == "1":
      with open(f"ClearFly_VA/users/{ctx.author.id}/data.txt", "r+", encoding = "utf-8") as file:

        file.seek(0, os.SEEK_END)

        pos = file.tell() - 1

        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()
      embed = discord.Embed(title="Flight canceled!", color=cfc)
      await ctx.respond(embed=embed)
    else:
        embed=discord.Embed(title="Error 503!", description="You need to train before using this command", color=errorc)
        await ctx.respond(embed=embed)
  else:
        embed=discord.Embed(title="Error 503!", description="You need to train before using this command", color=errorc)
        await ctx.respond(embed=embed)
@va.command(name="flights", descripiton="Fetches flights a user has done.")
async def flights(ctx, user: discord.Member = None):
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
            await ctx.respond(f"Loading {user}'s Filed flights.")
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


@bot.user_command(name="User VA Flights")
async def flights_app(ctx, user: discord.Member):
  if os.path.exists(".onpc"):
      guild = bot.get_guild(965419296937365514)
      cfpilot = guild.get_role(1040918463763468369)
      if cfpilot in ctx.author.roles:
          await ctx.respond(f"Loading {user}'s Filed flights.")
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
          embed = discord.Embed(title="Error 403!", description="You do not have the <@&1040918463763468369> role. \nGet it in <#965686982304997466> before using this command!", color=errorc)
          await ctx.respond(embed=embed)
  else:
      embed=discord.Embed(title="Error 503!", description="The bot is currently not hosted on <@668874138160594985>'s computer, so I'm unable to save data, tell him and he'll host it for you.", color=errorc)
      await ctx.respond(embed=embed)
@va.command(name="stats", description="Show general statistics about the whole VA.")
async def vastats(ctx):
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

  if __name__ == "__main__":
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
  if __name__ == "__main__":
                  cmnac = movestr(cmnac)
  if __name__ == "__main__":
                  cmnac = delstr(cmnac)
                  cmnac = delstr(cmnac)
  def most_frequent(List):
            return max(set(List), key = List.count)
  def most_frequent(List):
            return max(set(List), key = List.count)

  if __name__ == "__main__":
    cmndestoutput = list(filter(None, cmndestoutput))
    cmndest = most_frequent(cmndestoutput)
  cmnac = f"{most_frequent(cmnac)}".replace(",","")
  embed = discord.Embed(title="ClearFly VA Statistics", color=cfc)
  embed.add_field(name="Total Flights:", value=f" {output}")
  if cmnac == "":
    embed.add_field(name="Most Common Aircraft:", value=f"Not enough data available")
  else:
    embed.add_field(name="Most Common Aircraft:", value=f" {cmnac}")
  embed.add_field(name="Most Common Destination:", value=f" {cmndest}")
  embed.add_field(name="_ _", value="\n*Notice: Both 'Most Common Aircraft' and 'Most Common Destination' will have a random selected value of 2 or more elements with the same frequency if that is the case.*", inline=True)
  await ctx.respond(embed=embed)

@va.command(name="leaderboard", description="Get the leaderboard of who flew the most flights!")
async def valb(ctx):
  output = []
  for index, filename in enumerate(glob.glob('ClearFly_VA/users/*/data.txt')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        nof = f"{int(len(f.readlines()))-1}"
        filen = filename.replace("ClearFly_VA/users/", f"")
        id=os.path.dirname(filen)
        user = bot.get_user(int(id))
        line = f"| Flights flown:{nof} {user.name}\n"
        output.append(line)
  output.sort(reverse=True)
  def movestr(lst):
    return [
        f"{' '.join(elem.split()[3:]).rstrip()} {' '.join(elem.split()[:3])}\n"
        for elem in lst
    ]
        
  if __name__ == "__main__":
          output = movestr(output)
  foutput = [f'{index} | {i}' for index, i in enumerate(output, 1)]
  embed = discord.Embed(title="ClearFly VA Leaderboard", description=f"""
  ```
{"".join(foutput)}
  ```
  """, color=cfc)
  await ctx.respond(embed=embed)



class VALivs(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(label="See more screenshots", style=discord.ButtonStyle.blurple, row=1)
  async def button_callback(self, button, interaction):
    await interaction.response.send_message("https://cdn.discordapp.com/attachments/1013239106198835300/1015310203832516731/FJS_732_TwinJet_-_2022-09-02_13.20.01.png\nhttps://cdn.discordapp.com/attachments/1013239106198835300/1015290133601320980/b738_4k_-_2022-08-29_16.09.22.PNG\nhttps://cdn.discordapp.com/attachments/1013239106198835300/1015290004001542164/A300_P_V2_-_2022-08-31_00.37.05.PNG\nhttps://cdn.discordapp.com/attachments/1013239106198835300/1030891826179231835/A300_F_V2_-_2022-10-15_18.07.50.png\nhttps://cdn.discordapp.com/attachments/1019564716416303184/1037312155566997564/b738_4k_-_2022-11-02_11.27.20.png", ephemeral=True)
@va.command(name="liveries", description="Looking to fly for the ClearFly VA? Here are the liveries to get you started!")
async def valivs(ctx):
  button1 = Button(label="Boeing 737-800 by Zibo", style=discord.ButtonStyle.url, url="https://drive.google.com/drive/folders/1WcoZpmFNk7jfraZE3VEzl6JRPcRzg7sZ?usp=sharing")
  button2 = Button(label="Airbus A300-600 by IniSimulations", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/1vdIOYlcM_2kNhooD_CTDE8UpoJ7mIvkk/view?usp=share_link")
  button3 = Button(label="Airbus A300-600F by IniSimulations", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/1w6kd3H0VBiWoTlmcvvvyte5wbqHE7i5k/view?usp=share_link")
  button4 = Button(label="Boeing 737-200 by FlyJSim", style=discord.ButtonStyle.url, url="https://drive.google.com/file/d/1o1vQk_HG1iJhJH1t_Z8cLBimDwxG90-C/view?usp=share_link")
  view = VALivs()
  view.add_item(button1)
  view.add_item(button2)
  view.add_item(button3)
  view.add_item(button4)
  embed=discord.Embed(title="ClearFly VA Official Liveries:",color=cfc)
  await ctx.respond(embed=embed, view=view)


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


class MyView4(discord.ui.View):
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
async def faq(ctx):
  embed = discord.Embed(title="Announcement Pings", description="Click on 📣 for announcement pings.\n*(click again to remove.)*", color=cfc)
  emb = discord.Embed(title="Update Pings", description="Click on 🛠 for update pings.\n*(click again to remove.)*", color=cfc)
  embva = discord.Embed(title="ClearFly VA pilot", description="Click on ✈️ to be part of the Official ClearFly VA!\n*(click again to remove.)*", color=cfc)
  await ctx.respond("Button roles posted!",ephemeral=True)
  await ctx.send(embed=embed,view=MyView3())
  await ctx.send(embed=emb,view=MyView4())

###################################
##Help cmd, Stats cmd and bot.run##
###################################

@utility.command(name="ping",description="Shows the latency speed of the bot.")
async def ping(ctx):
    emb = discord.Embed(title="Bot's latency", description=f"The bot's latency is {round(bot.latency*1000)}ms!", color=cfc)
    await ctx.respond(embed=emb)

bot.launch_time = datetime.utcnow()

@utility.command(name="stats",description="Show statistics about the bot and server.")
async def stats(ctx):
  f = open("main.py", "r")
  lines = len(f.readlines())
  delta_uptime = datetime.utcnow() - bot.launch_time
  hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)
  embed = discord.Embed(title = "**Bot Stats**", description =    f"""
```rb
Creator: Matt3o0#4000
Uptime: {days}d {hours}h {minutes}m {seconds}s
LinesOfCode: {lines}
```
  """, color = cfc)
  servers = len(bot.guilds)
  members = 0
  for guild in bot.guilds:
    members += guild.member_count - 1
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

class HelpView(discord.ui.View):
    @discord.ui.select( 
        placeholder = "Command type", 
        min_values = 1, 
        max_values = 1, 
        options = [ 
            discord.SelectOption(
                label="Utility",
                description="Commands that serve a use"
            ),
            discord.SelectOption(
                label="Fun",
                description="Commands that are meant to be fun"
            ),
            discord.SelectOption(
                label="VA",
                description="VA related commands"
            ),
            discord.SelectOption(
              label="Leveling",
              description="Commands related to leveling"
            ),
            discord.SelectOption(
              label="Admin",
              description="Commands for admins only"
            )
        ]
    )
    async def select_callback(self, select, interaction):
      if select.values[0] == "Utility":
          embutil = discord.Embed(title = "**Help**",color = cfc)
          embutil.add_field(name="**Utility commands**", value=f"""
```
/help : Shows this information.
/report : Report a user or situation to the team.
```
```yaml
/utility stats : Show statistics about the bot and server.
/utility ping : Shows the latency speed of the bot.
/utility who-is : Shows all kind of information about a user.
/utility the-team : Shows The ClearFly Team!
/utility avatar : Shows your avatar.
/utility github : Shows the bot's GitHub repository.
/utility math basic: Do some basic math.
/utility math advanced: Do some advanced math.
/utility level: Get someone's level.
```
                """)
          await interaction.response.edit_message(embed=embutil)
      if select.values[0] == "Fun":
          embfun = discord.Embed(title = "**Help**",color = cfc)
          embfun.add_field(name="**Fun commands**", value=f"""
```yaml
/fun ascii : Converts text in to ascii.
/fun 8ball : Ask the bot some questions!
/fun dadjoke: Gets you a dadjoke.
/fun roast: Roast whoever you'd like!
/fun buttongame: Play a game with buttons!
```
              """)
          await interaction.response.edit_message(embed=embfun)
      if select.values[0] == "VA":
          guild = bot.get_guild(965419296937365514)
          role = guild.get_role(1040918528565444618)
          embva = discord.Embed(title = "**Help**",color = cfc)
          if role in interaction.user.roles:
            embva.add_field(
              name="**ClearFly Virtual Airline**",
              value=f"""
*notice: most va commands are disabled at the moment, more info in <#1013934267966967848>
```yaml
-------Instructor-------
/va instructor approve : Approve a student's flight and give the required info to them.
/va instructor check-off : Check off a user to end their training
--------Training--------
/va training : Start your career in the ClearFly VA!
-----After Training-----
/va file : File a flight you are gonna do for the ClearFly VA.
/va flights : Fetches information about all flights a user has done.
/va leaderboard : Get the leaderboard of who flew the most flights!
/va liveries : Get all liveries to get your journey started.
```
                          """, inline=False)
          else:
            embva.add_field(
              name="**ClearFly Virtual Airline**",
              value=f"""
*notice: most va commands are disabled at the moment, more info in <#1013934267966967848>
```yaml
--------Training--------
/va training : Start your career in the ClearFly VA!
-----After Training-----
/va file : File a flight you are gonna do for the ClearFly VA.
/va flights : Fetches information about all flights a user has done.
/va leaderboard : Get the leaderboard of who flew the most flights!
/va liveries : Get all liveries to get your journey started.
```
                          """, inline=False)
      if select.values[0] == "Leveling":
          embva = discord.Embed(title = "**Help**",color = cfc)
          embva.add_field(
              name="**Leveling Commands**",
              value=f"""
```yaml
/level userlevel : Gets the provided user's level.
/level leaderboard : See the leaderboard of the whole server.
```
                          """, inline=False)
          await interaction.response.edit_message(embed=embva)
      if select.values[0] == "Admin":
        guild = bot.get_guild(965419296937365514)
        adminrole = guild.get_role(1006725140933001246)
        if adminrole in interaction.user.roles:
          embad = discord.Embed(title = "**Help**",color = cfc)
          embad.add_field(
              name="**Admin Commands**",
              value=f"""
```yaml
/admin spam : Spam the channel to oblivion.
/admin purge : Delete messages from a channel.
/admin echo : Send a message as the bot.
/admin slowmode : Set the slow mode of a channel.
/admin embed : Send an embed as the bot.
```
                          """, inline=False)
          await interaction.response.edit_message(embed=embad)
        else:
          ember = discord.Embed(title="Error 403!", description="You are not an admin, you can't use these commands!", color=errorc)
          await interaction.response.edit_message(embed=ember)
@bot.command(name="help", description="Need help? This is the right command!")
async def help(ctx):
  embed = discord.Embed(title="Help!", description="Select the type of command in the drop down for help.", color=cfc)
  await ctx.respond(embed=embed, view=HelpView())
#############################################
bot.run(os.getenv('TOKEN'))
