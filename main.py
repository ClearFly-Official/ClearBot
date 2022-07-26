########################
#-Made by Matt3o0#4764-#
########################
import discord
import os

intents = discord.Intents.all()

bot = discord.Bot()
client = discord.Client()


@client.listen()
async def on_ready()
    print("I'm ready for usage!")


@client.listen()
async def on_message(message):
    if message.content == "hi":
        await message.send("hi")


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