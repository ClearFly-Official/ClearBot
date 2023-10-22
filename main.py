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
        self.dev_mode = os.path.exists(".dev")

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

        self.logs: None | discord.TextChannel = None

        self.server_id = 965419296937365514
        self.bot_author = 668874138160594985

        self.channels = {
            "info": 1002194493304479784,
            "fbo": 1013934267966967848,
            "va-overview": 1099712642916044881,
            "news": 1066124540318588928,
            "logs": 1001405648828891187,
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

    async def set_theme(self, author: str, theme: int = 0) -> dict[str, bool | list]:
        async with aiosqlite.connect("main.db") as db:
            await db.execute(
                "UPDATE config SET value = ? WHERE key = 'theme'", (theme,)
            )
            await db.commit()

        self.theme = theme

        role_colors = {
            "*": {0: 0x6DB2D9, 1: 0xFEB32D, 2: 0x00A628},
            "member": {0: 0x2681B4, 1: 0xFD852D, 2: 0x00771D},
        }

        guild = self.get_guild(self.server_id)
        if not guild:
            guild = await self.fetch_guild(self.server_id)

        failed = []
        guild_success = False

        if guild:
            for name, role_id in self.roles.items():
                try:
                    if name == "member":
                        role = guild.get_role(role_id)
                        if role:
                            await role.edit(
                                color=role_colors["member"][self.theme],
                                reason=f"{author} asked for a theme ({self.theme_name}) change.",
                            )
                        else:
                            raise discord.DiscordException("Role not found")

                    elif name != "admin":
                        role = guild.get_role(role_id)
                        if role:
                            await role.edit(
                                color=role_colors["*"][self.theme],
                                reason=f"{author} asked for a theme ({self.theme_name}) change.",
                            )
                        else:
                            raise discord.DiscordException("Role not found")
                except Exception:
                    role = guild.get_role(role_id)
                    if role:
                        failed.append(role)
                    else:
                        failed.append("Unknown Role")
            guild_success = True

        return {"guild_success": guild_success, "failed_roles": failed}

    def sendable_channel(
        self, channel
    ) -> tuple[bool, discord.TextChannel | discord.VoiceChannel | None]:
        if isinstance(channel, discord.StageChannel):
            return (False, None)
        elif isinstance(channel, discord.ForumChannel):
            return (False, None)
        elif isinstance(channel, discord.CategoryChannel):
            return (False, None)
        elif not channel.can_send():
            return (False, None)
        elif not channel:
            return (False, None)
        else:
            return (True, channel)

    @property
    def theme_name(self):
        match self.theme:
            case 0:
                return "Default"
            case 1:
                return "Halloween"
            case 2:
                return "Christmas"
            case _:
                return "Unknown"


bot = ClearBot(intents=discord.Intents.all())
roles = bot.roles
load_dotenv()


@bot.listen()
async def on_ready():
    gc.collect()
    logs = bot.get_channel(bot.channels.get("logs", 0))

    if isinstance(logs, discord.TextChannel):
        bot.logs = logs

    print(
        r"""
\033[34m|-----------------------------------------\033[0m
\033[34m| \033[96m  ____ _                 ____        _   \033[0m
\033[34m| \033[96m / ___| | ___  __ _ _ __| __ )  ___ | |_ \033[0m
\033[34m| \033[96m| |   | |/ _ \/ _` | '__|  _ \ / _ \| __|\033[0m
\033[34m| \033[96m| |___| |  __/ (_| | |  | |_) | (_) | |_ \033[0m
\033[34m| \033[96m \____|_|\___|\__,_|_|  |____/ \___/ \__|\033[0m
\033[34m|-----------------------------------------\033[0m"""
    )
    if bot.dev_mode:
        print("| DEV MODE")


for cog in bot.cog_list:
    bot.load_extension(f"cogs.{cog}")

bot.run(os.getenv("DEV_TOKEN" if bot.dev_mode else "TOKEN"))
