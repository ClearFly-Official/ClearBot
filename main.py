###################
#-Made by Matt3o0-#
###################

import discord#Py-cord
import os
import random
from dotenv import load_dotenv
from cogs import va, admin#for view classes of cogs for persistent views
from discord.ext import tasks
from datetime import datetime 

load_dotenv()

bot = discord.Bot(intents=discord.Intents.all())


@bot.listen()
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Starting up."),status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name="Starting up.."),status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name="Starting up..."),status=discord.Status.online)
    channel=bot.get_channel(1001405648828891187)
    now = discord.utils.format_dt(datetime.now())
    if os.path.exists(".onpc"):
      embed=discord.Embed(title="I started up!", description=f"""
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
    bot.add_view(admin.MyView())
    bot.add_view(admin.MyView2())
    bot.add_view(admin.MyView3())
    bot.add_view(admin.MyView4())
    bot.add_view(va.InfoB4training())
    presence.start()
    statements=[
      "Give me Baby Boeing 😩",
      "Boeing > Airbus",
      "How are you doing?",
      "Use me please.",
      "How can I assist you today?",
    ]
    await bot.change_presence(activity=discord.Game(name=f"/help | {random.choice(statements)}"),status=discord.Status.online)
    print("The bot is ready for usage!")

@tasks.loop(minutes=5)
async def presence():
    statements=[
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
    await bot.change_presence(activity=discord.Game(name=f"/help | {random.choice(statements)}"),status=discord.Status.online)

cogs = [
    "listeners",
    "dev",
    "admin",
    "fun",
    "level",
    "utility",
    "va"
]
for cog in cogs:
    bot.load_extension(f"cogs.{cog}")
  
bot.run(os.getenv('TOKEN'))