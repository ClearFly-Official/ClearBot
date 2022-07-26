########################
#-Made by Matt3o0#4764-#
########################
import discord
import os

bot = discord.Bot()
client = discord.Client()

@bot.event
async def on_ready():
    print("I'm ready for usage!")

@bot.event 
async def on_member_join(member):
     channel=bot.get_channel(1001401783689678868)
     emb=discord.Embed(description=f"Thanks {member.mention} for joining!")
     emb.set_image(url=userAvatarUrl)
     await channel.send(embed=emb)

bot.run(os.environ['TOKEN'])