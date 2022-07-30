########################
#-Made by Matt3o0#4764-#
########################
from doctest import debug_script
import discord
import os
import platform
import pyfiglet
from dateutil.parser import isoparse
from datetime import datetime
from discord.ext import commands, tasks
from discord.ext.commands import (BadArgument, Bot, BucketType,
                                  clean_content, command, cooldown)


cfc = 0x4f93cf


intents = discord.Intents.all()
intents.members = True
intents.reactions = True

bot = discord.Bot(command_prefix=',', intents=intents)



@bot.listen()
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="/help"),status=discord.Status.online)
    print("The bot is ready for usage!")

@bot.listen()
async def on_member_join(member):
    channel = bot.get_channel(965600413376200726)
    memberid = member.id
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




@bot.command(name="echo",description="Send a message as the bot.(Admin only)")
@commands.has_role(965422406036488282)
async def echo(ctx, text):
    await ctx.respond('posted your message!',ephemeral  = True)
    await ctx.channel.send(text)
    pfp = ctx.author.avatar.url
    channel = bot.get_channel(1001405648828891187)
    emb = discord.Embed(title=f"{ctx.author} used echo:", description=text, color = 0x4f93cf)
    emb.set_thumbnail(url=pfp)
    await channel.send(embed=emb)
    print(ctx.author, "used echo:", text)

@bot.command(name="embed",description="Send an embed as the bot.(Admin only)")
@commands.has_role(965422406036488282)
async def embed(ctx, title, description):
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

@bot.command(name="help", description="Help command for the bot.")
async def embed(ctx):
    emb = discord.Embed(title = "**Help**",color = cfc)
    emb.add_field(name="**Available commands**", value=f"""
*more to come soon!*
```
/stats : Show statistics about the bot and server.
/ping : Shows the latency speed of the bot.
/help : Shows this information.
/the-team : Shows The ClearFly Team!
/avatar : Shows your avatar.
/ascii : Converts text in to ascii.
/who-is : Shows all kind of information about a user.
```
  """)

    emb.add_field(
            name="**Available commands (Admin only)**",
            value=f"""
```
/echo : Send a message as the bot.
/embed : Send an embed as the bot.
```
            """
      )
    await ctx.respond(embed=emb)

@bot.command(name='the-team', description='Shows The ClearFly Team!')
async def team(ctx):
  emb = discord.Embed(title="**The ClearFly Team:**",color=cfc)
  logo = "https://cdn.discordapp.com/attachments/927609657655177238/992887468410024026/ClearFly_Logo.png"
  emb.add_field(name="WolfAir",value="Founder & Modeler",inline=False)
  emb.add_field(name="Matt3o0",value="Bot Creator & Admin",inline=False)
  emb.add_field(name="DJ",value="Admin",inline=False)
  emb.set_thumbnail(url=logo)
  await ctx.respond(embed=emb)

@bot.command(name="avatar",description="Shows your avatar.")
async def avatar(ctx, user: discord.Member = None):
  if user == None:
    author = ctx.author
    pfp = author.avatar.url
    embed = discord.Embed(title="Your avatar!", color=cfc)
    embed.set_image(url=pfp)
    await ctx.respond(embed=embed)
  else:
    userAvatarUrl = user.avatar.url    
    embed = discord.Embed(title=f"{user}'s avatar!", color=cfc)
    embed.set_image(url=userAvatarUrl)
    await ctx.respond(embed=embed)

@bot.command(name="ascii",description="Convert texts into ascii")
async def ascii(ctx, text):
  try:
    ascii = pyfiglet.figlet_format(text)
    await ctx.respond(f"```{ascii}```")
  except Exception as e:
    await ctx.respond(f'Error:\n{e}', ephemeral  = True)

@bot.command(name="who-is", description="Shows all kind of information about a user")
async def whois(ctx, user: discord.Member = None):
  if user == None:
    author = ctx.author
    acccreatee = author.created_at
    accjoine = author.joined_at
    pfp = author.avatar.url
    embed = discord.Embed(title=f"**Your information**", color=cfc)
    embed.add_field(name="**General Information:**", value=f"""
    **Account created on:**{acccreatee}
    **Account joined this server on:**{accjoine}
    """)
    embed.set_image(url=pfp)
    await ctx.respond(embed=embed)
  else:
    acccreate = user.created_at
    accjoin = user.joined_at
    pfpe = user.avatar.url
    embed = discord.Embed(title=f"**{user}'s information**", color=cfc)
    embed.add_field(name="**General Information:**", value=f"""
    **Account created on:**{acccreate}
    **Account joined this server on:**{accjoin}
    """)
    embed.set_image(url=pfpe)
    await ctx.respond(embed=embed)
##############################
##no more commands down here##
##############################

@bot.command(name="ping",description="Shows the latency speed of the bot.")
async def ping(ctx):
    emb = discord.Embed(title="Bot's latency", description=f"The bot's latency is {round(bot.latency*1000)}ms!", color=0x4f93cf)
    await ctx.respond(embed=emb)

bot.launch_time = datetime.utcnow()

@bot.command(name="stats",description="Show statistics about the bot and server.")
async def stats(ctx):
  delta_uptime = datetime.utcnow() - bot.launch_time
  hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)
  embed = discord.Embed(title = "**Bot Stats**", description =    f"""
```yaml
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
```yaml
Members: {members}
```
            """,
            inline=False
      )
  await ctx.respond(embed = embed)

#############################################

bot.run(os.environ['TOKEN'])