###################
# -Made by Matt3o0-#
###################

import discord  # Py-cord
import os
from dotenv import load_dotenv
from datetime import datetime

bot = discord.Bot(intents=discord.Intents.all())
load_dotenv()
bot.start_time = datetime.utcnow()
bot.rshownsubms = []

cfc = 0x6DB2D9  # <- default color
# cfc = 0xcc8d0e # <- halloween color
# cfc = 0x00771d # <- christmas color
errorc = 0xFF0000
warningc = 0xFFAA00


@bot.listen()
async def on_ready():
    print(
        f"""
|-----------------------------
| CLEARBOT is ready for usage 
|-----------------------------"""
    )


cogs = os.listdir("cogs")
cogs = [x.split(".")[0] for x in cogs if x.endswith(".py")]

for cog in cogs:
    bot.load_extension(f"cogs.{cog}")

bot.run(os.getenv("TOKEN"))
