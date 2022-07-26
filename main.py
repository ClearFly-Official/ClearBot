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

bot.run(os.environ['TOKEN'])