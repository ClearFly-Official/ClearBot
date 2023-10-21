import gc
import aiosqlite
import discord
import os
import sqlite3
from dotenv import load_dotenv
from datetime import datetime


class ClearBot(discord.Bot):
    def __init__(self, *args, **kwargs):
        self.color = self.embed_color

        self.start_time = datetime.utcnow()
        self.cog_list = [
            x.split(".")[0] for x in os.listdir("cogs") if x.endswith(".py")
        ]

        con = sqlite3.connect("main.db")
        # 0 = normal
        # 1 = halloween
        # 2 = Christmas
        self.theme = int(
            con.execute("SELECT value FROM config WHERE key='theme'").fetchone()[0]
        )
        con.close()

        self.server_id = 965419296937365514
        self.bot_author = 668874138160594985

        self.channels = {
            "info": 1002194493304479784,
            "fbo": 1013934267966967848,
            "va-overview": 1099712642916044881,
            "news": 1066124540318588928,
        }
        self.roles = {
            "admin": 965422406036488282,
            "member": 1002200398905483285,
            "clearfly-pilot": 1013933799777783849,
            "count-god": 977868778815758356,
            "livery-painter": 1055919452086087720,
            "clearfly-livery-painter": 1055909461488844931,
            "clearfly-unofficial-painter": 1098964227689033759,
            "bot": 970019585858363482,
            "clearbot": 1001457701022343181,
        }

        self._colors = {
            0: {
                0: 0x6DB2D9,
                1: 0xCC8D0E,
                2: 0x00771D,
            },
            1: {0: 0xFF0000, 1: 0xFF0000, 2: 0xFF0000},
            2: {0: 0xFFAA00, 1: 0xFFAA00, 2: 0xFFAA00},
        }
        super().__init__(*args, **kwargs)

    def embed_color(self, type: int = 0) -> int:
        try:
            return self._colors[type][self.theme]
        except KeyError:
            return self._colors[0][self.theme]

    async def set_theme(self, theme: int = 0) -> None:
        async with aiosqlite.connect("main.db") as db:
            await db.execute(
                "UPDATE config SET value = ? WHERE key = 'theme'", (theme,)
            )
            await db.commit()


bot = ClearBot(intents=discord.Intents.all())
roles = bot.roles
load_dotenv()


@bot.listen()
async def on_ready():
    gc.collect()
    print(
        f"""
\033[34m|-----------------------------\033[0m
\033[34m|\033[96;1m CLEARBOT\033[0;36m is ready for usage \033[0m
\033[34m|-----------------------------\033[0m"""
    )


for cog in bot.cog_list:
    bot.load_extension(f"cogs.{cog}")

bot.run(os.getenv("TOKEN"))
