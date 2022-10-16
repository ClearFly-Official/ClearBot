########################
#-Made by Matt3o0#4000-#
########################
from glob import glob
import discord
import os
import platform
import pyfiglet
import requests
import random
import ConfigParser
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


load_dotenv()

cfc = 0x4f93cf
errorc = 0xFF0000
intents = discord.Intents.all()
intents.members = True
intents.reactions = True

bot = discord.Bot(command_prefix=',', intents=discord.Intents.all())
fun = bot.create_group(name="fun",description="Commands that are supposed to be fun")
va = bot.create_group(name="va",description="Commands related to the ClearFly Virtual Airline")
admin = bot.create_group(name="admin", description="Commands for admins")
utility = bot.create_group(name="utility", description="Commands related to utility")
weather = utility.create_subgroup(name="weather", description="Commands in testing.")
math = utility.create_subgroup(name="math", description="Commands related to math")


@bot.listen()
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Starting up."),status=discord.Status.online)
    sleep(0.5)
    await bot.change_presence(activity=discord.Game(name="Starting up.."),status=discord.Status.online)
    sleep(0.5)
    await bot.change_presence(activity=discord.Game(name="Starting up..."),status=discord.Status.online)
    channel=bot.get_channel(1001405648828891187)
    now = discord.utils.format_dt(datetime.now())
    embed=discord.Embed(title="I started up!", description=f"""
    Started bot up on {now}
    """,color=0x00FF00)
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
      "If it ain't Boeing, I'm not going.",
      "I'm tired",
      "Nuke airbus smh"
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
  emb = discord.Embed(title=f"{member} left.", color=cfc, description=f"Joined on {discord.utils.format_dt(member.joined_at)}")
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
  emb = discord.Embed(title="GitHub:", description="[Here's the repository!](https://github.com/duvbolone/ClearBot)",color=cfc)
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
  print(member)
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
    opts = [1, 2, 3]
    output = random.choice(opts)
    for child in self.children:
      child.disabled = True
    if output == b:
        await interaction.response.send_message(":partying_face: You guessed right, congrats!\n\n *play again with /fun buttongame!*")
    else:
      if isPressed == 1:
        await interaction.response.send_message(f"You guessed wrong, the right answer was {output}\n\n *play again with /fun buttongame!*")

  @discord.ui.button(label="2", style=discord.ButtonStyle.green)
  async def second_button_callback(self, button, interaction):
    global b, isPressed
    b = 2
    isPressed = 1
    for child in self.children:
      child.disabled = True
    opts = [1, 2, 3]
    output = random.choice(opts)
    if output == b:
        await interaction.response.send_message(":partying_face: You guessed right, congrats!\n\n *play again with /fun buttongame!*")
    else:
      if isPressed == 1:
        await interaction.response.send_message(f"You guessed wrong, the right answer was {output}\n\n *play again with /fun buttongame!*")

  @discord.ui.button(label="3", style=discord.ButtonStyle.green)
  async def third_button_callback(self, button, interaction):
    global b, isPressed
    b = 3
    isPressed = 1
    opts = [1, 2, 3]
    for child in self.children:
      child.disabled = True
    output = random.choice(opts)
    if output == b:
        await interaction.response.send_message(":partying_face: You guessed right, congrats!\n\n *play again with /fun buttongame!*")
    else:
      if isPressed == 1:
        await interaction.response.send_message(f"You guessed wrong, the right answer was {output}\n\n *play again with /fun buttongame!*")
  
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



class VALivs(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(label="See more screenshots", style=discord.ButtonStyle.blurple, row=1)
  async def button_callback(self, button, interaction):
    ctx = discord.ApplicationContext
    await interaction.response.send_message("Here you go! \n\nXP12: \nhttps://cdn.discordapp.com/attachments/965419865521393704/1017527654745919528/b738_4k_-_2022-09-08_22.07.57.png \n\nXP11:\nhttps://cdn.discordapp.com/attachments/965419865521393704/1016006462805389432/b738_-_2022-09-04_11.26.10.png \n https://cdn.discordapp.com/attachments/965419865521393704/1015948512984322059/b738_-_2022-09-04_13.35.41.png https://cdn.discordapp.com/attachments/965419865521393704/1015948511973494854/b738_-_2022-09-04_12.53.17.png https://cdn.discordapp.com/attachments/965419865521393704/1015948512250306581/b738_-_2022-09-04_13.35.20.png ", ephemeral=True)

@va.command(name="liveries", description="Looking to fly for the ClearFly VA? Here are the liveries to get you started!")
async def valivs(ctx):
  button1 = Button(label="Boeing 737-800 by Zibo", style=discord.ButtonStyle.url, url="https://drive.google.com/drive/u/1/folders/1DEzn_jPgyME-U1FrUs3eX4QTwsgwbfpD")
  button2 = Button(label="Airbus A300-600 by IniSimulations", style=discord.ButtonStyle.url, url="https://drive.google.com/drive/u/1/folders/16n0cnwkTeGWBhUQJZhXtNz4oq4n4Pe86")
  button3 = Button(label="Airbus A300-600F by IniSimulations", style=discord.ButtonStyle.url, url="https://drive.google.com/drive/u/0/folders/1JIT5dhLsPHI95-v36iETxolSYZHq-aku")
  button4 = Button(label="Boeing 737-200 by FlyJSim", style=discord.ButtonStyle.url, url="https://drive.google.com/drive/u/1/folders/1g-vZsECHyHQMbjwnasxHwj0TXjxfLQ0P")
  view = VALivs()
  view.add_item(button1)
  view.add_item(button2)
  view.add_item(button3)
  view.add_item(button4)
  embed=discord.Embed(title="ClearFly VA Official Liveries:",color=cfc)
  embed.set_image(url="https://cdn.discordapp.com/attachments/801910364831744071/1031268854795604008/VALivsOverview.png")
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
          embva = discord.Embed(title = "**Help**",color = cfc)
          embva.add_field(
              name="**ClearFly Virtual Airline**",
              value=f"""
```yaml
/va file : File a flight you are gonna do for the ClearFly VA.
/va flights : Fetches information about all flights a user has done.
/va overview : Get an overview over all flights in the va.
/va liveries : Get all liveries to get your journey started.
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
