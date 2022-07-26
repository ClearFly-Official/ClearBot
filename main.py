########################
#-Made by Matt3o0#4764-#
########################
import discord
import os

intents = discord.Intents.all()

bot = discord.Bot()
client = discord.Client()

@bot.event
async def on_ready():
    print("I'm ready for usage!")

@bot.event 
async def on_member_join(member):
     channel = bot.get_channel(1001401783689678868)
     emb = discord.Embed(description=f"Thanks {member.mention} for joining!")
     emb.set_image(url=userAvatarUrl)
     await channel.send(embed=emb)

@bot.command(name="echo",description="Send a message as the bot.")
async def echo(ctx, text):
    await ctx.respond('posted your message!',ephemeral  = True)
    await ctx.channel.send(text)
    channel = bot.get_channel(1001405648828891187)
    emb = discord.Embed(title=f"{ctx.author} used echo:", description=text)
    emb.set_image(url=pfp)
    await channel.send(embed=emb)
    print(ctx.author, "used echo:", text)


bot.run(os.environ['TOKEN'])