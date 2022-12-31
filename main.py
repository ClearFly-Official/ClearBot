###################
#-Made by Matt3o0-#
###################

import discord#Py-cord
import os
import random
from dotenv import load_dotenv
from discord.ext import tasks
from datetime import datetime 
from discord.ext import commands

bot = discord.Bot(intents=discord.Intents.all())
load_dotenv()
bot_start_time = datetime.utcnow()
#cfc = 0x2681b4 #<- default color
#cfc = 0xcc8d0e # <- halloween color
cfc = 0x00771d # <- christmas color
errorc = 0xFF0000

@bot.listen()
async def on_ready():
        channel = bot.get_channel(1001405648828891187)
        now = discord.utils.format_dt(datetime.now())
        if os.path.exists(".onpc"):
            embed = discord.Embed(title="I started up!", description=f"""
            Started bot up on {now}
            *Data save available*
            """,color=0x00FF00)
            await channel.send(embed=embed)
        else:
            embed=discord.Embed(title="I started up!", description=f"""
            Started bot up on {now}
            *Data save unavailable*
            """,color=0x00FF00)
            await channel.send(embed=embed)
        presence.start()
        print("The bot is ready for usage!")

@tasks.loop(minutes=10)
async def presence():
        statements_=[
        "Give me Baby Boeing 😩",
        "Boeing > Airbus",
        "How are you doing?",
        "Use me please.",
        "How can I assist you today?",
        "BABY BOEINGGGG",
        "If it ain't Boeing, I'm not going.",
        "I'm tired",
        "Nuke airbus smh",
        "Boeing supremacy",
        "*Sends missile to Airbus hq*",
        "Wolfair is my daddy:)",
        "Deep™",
        "What ya looking at 🤨",
        ]
        statements = ["🎉 Happy new year!"]
        await bot.change_presence(activity=discord.Game(name=f"/help | {random.choice(statements)}"),status=discord.Status.online)


cogs = os.listdir("cogs")
cogs = [x.split('.')[0] for x in cogs]
cogs.remove("__pycache__")

for cog in cogs:
    bot.load_extension(f"cogs.{cog}")
  
bot.run(os.getenv('TOKEN'))