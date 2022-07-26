########################
#-Made by Matt3o0#4764-#
########################
import discord
import os

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot()
client = commands.Bot(command_prefix=',', intents=intents)


@bot.listen()
async def on_ready():
    print("I'm ready for usage!")


@bot.listen()
async def on_member_join():
    print("pog")

@client.listen()
async def on_member_join(member):
    await member.send(f'Welcome to ClearFly, {member.mention}! Read the <#965610363842351144> to become a member and gain full access to the server. Thanks for joining!')


@bot.command(name="echo",description="Send a message as the bot.")
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