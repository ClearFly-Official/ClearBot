########################
#-Made by Matt3o0#4764-#
########################
import discord
import os
import platform
from datetime import datetime
from discord.ext import commands, tasks
from discord.ext.commands import (BadArgument, Bot, BucketType,
                                  clean_content, command, cooldown)


#clearfly color embed = 0x4f93cf#

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(command_prefix=',', intents=intents)

print("I started up ig")
await bot.change_presence(activity=discord.Game(name="/help"),status=discord.Status.online) 

@bot.listen()
async def on_member_join(member):
    channel = bot.get_channel(965600413376200726)
    memberid = member.id
    emb = discord.Embed(title=f"Welcome to ClearFly!", description=f"Hey there, {member.mention}! Be sure to read the <#1002194493304479784> to become a member and gain full access to the sever! Thanks for joining!", color = 0x57a4cd)
    await channel.send(embed=emb)

@bot.listen()
async def on_reaction_add(reaction, user):
    Channel = bot.get_channel(1001514035868610702)
    if reaction.message.channel.id != Channel.id:
        return
    if reaction.emoji == "👍":
      Role = discord.utils.get(user.server.roles, name="test role")
      await user.add_roles(Role)

@bot.listen()
async def on_message_delete(self, message):
    embed = discord.Embed(title="Message Deleted")
    embed.add_field(name="Member: ", value=message.author.mention, inline=False)
    embed.add_field(name="Message: ", value=message.content, inline=True)
    embed.add_field(name="Channel: ", value=message.channel.mention, inline=False)

    await self.bot.get_channel(1001405648828891187).send(embed=embed)

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
    emb = discord.Embed(title = "Available commands(more to come soon!)", description =    f"""
```
/stats : Show statistics about the bot and server.
/ping : Shows the latency speed of the bot.
```
  """, color = 0x4f93cf)

    emb.add_field(
            name="**Available commands(Admin only)**",
            value=f"""
```
/echo : Send a message as the bot.
/embed : Send an embed as the bot.
```
            """
      )
    await ctx.respond(embed=emb)

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
  embed = discord.Embed(title = "Bot Stats", description =    f"""
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


bot.run(os.environ['TOKEN'])
