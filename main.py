########################
#-Made by Matt3o0#4764-#
########################
import discord
import os
from discord.ext import commands, tasks
from discord.ext.commands import (BadArgument, Bot, BucketType,
                                  clean_content, command, cooldown)

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot()
boti = commands.Bot(command_prefix=',', intents=intents)

print("I started up ig")

@boti.listen()
async def on_member_join(member):
    channel = boti.get_channel(965600413376200726)
    emb = discord.Embed(title=f"Welcome to ClearFly, {member}!", description=f"Read the <#965610363842351144> to become a member and gain full access to the server. Thanks for joining!", color = 0x57a4cd)
    await channel.send(embed=emb)


@bot.slash_command(name="echo",description="Send a message as the bot.")
async def echo(ctx, text):
    await ctx.respond('posted your message!',ephemeral  = True)
    await ctx.channel.send(text)
    pfp = ctx.author.avatar.url
    channel = bot.get_channel(1001405648828891187)
    emb = discord.Embed(title=f"{ctx.author} used echo:", description=text, color = 0x4f93cf)
    emb.set_thumbnail(url=pfp)
    await channel.send(embed=emb)
    print(ctx.author, "used echo:", text)


bot.run(os.environ['TOKEN'])