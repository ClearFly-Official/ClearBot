########################
#-Made by Matt3o0#4764-#
########################
import discord
import os

intents = discord.Intents.all()

bot = discord.Bot()
client = discord.Client()


@bot.listen()
async def on_ready():
    print("I'm ready for usage!")


@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "When release":
        await message.channel.send("When it's done... Read the FAQ before asking questions please!")
    else:
        return

@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "will 3D cabin":
        await message.channel.send("Yes! But read the FAQ before asking questions please!")
    else: 
        return
        
@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "will custom FMC":
        await messsage.channel.send("Most likely, read the FAQ before asking these questions tho!")
    else:
        return


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