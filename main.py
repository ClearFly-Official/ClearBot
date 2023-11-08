import gc
import sys
import aiosqlite
import discord
import os
import sqlite3
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime


class UserObject(discord.Object):
    def __init__(self) -> None:
        self.id = 0
        self.name = "N/A"
        self.display_name = "N/A"
        self.global_name = "N/A"
        super().__init__(self.id)


class MissingPermissions(commands.CommandError):
    def __init__(self):
        super().__init__(f"User is not authorised.")


class UserVABanned(MissingPermissions):
    def __init__(self):
        super().__init__()


class ClearBot(discord.Bot):
    def __init__(self, *args, **kwargs) -> None:
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

        self.server_id = 965419296937365514
        self.bot_author = 668874138160594985
        self.bot_id = 0

        self.channels = {
            "info": 1002194493304479784,
            "arrivals": 965600413376200726,
            "fbo": 1013934267966967848,
            "va-overview": 1099712642916044881,
            "va-liveries": 1041057335449227314,
            "news": 1066124540318588928,
            "logs": 1001405648828891187,
            "dev-chat": 965655791468183612,
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

    def sendable_channel(
        self, channel
    ) -> discord.TextChannel | discord.VoiceChannel | None:
        if isinstance(channel, discord.StageChannel):
            return
        elif isinstance(channel, discord.ForumChannel):
            return
        elif isinstance(channel, discord.CategoryChannel):
            return
        elif not channel.can_send():
            return
        elif not channel:
            return
        else:
            return channel

    def user_object(
        self, user: discord.User | discord.Member | None
    ) -> UserObject | discord.Member | discord.User:
        if user:
            return user
        else:
            user_o = UserObject()
            return user_o

    def is_interaction_owner(
        self, interaction: discord.Interaction, user_id: int
    ) -> bool:
        if interaction.user:
            return interaction.user.id == user_id
        else:
            return False

    async def set_theme(self, author: str, theme: int = 0) -> dict[str, bool | list]:
        if not self.is_ready():
            return {"guild_success": False, "failed_roles": list(self.roles.items())}

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
                        failed.append(role.name)
                    else:
                        failed.append("Unknown Role")
            guild_success = True

        return {"guild_success": guild_success, "failed_roles": failed}

    async def send_log(self, *args, **kwargs) -> None:
        logs = self.get_channel(self.channels.get("logs", 0))
        if isinstance(logs, discord.TextChannel):
            await logs.send(*args, **kwargs)

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
    if bot.user:
        bot.bot_id = bot.user.id

    print(
        """
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


@bot.listen()
async def on_application_command_error(
    ctx: discord.ApplicationContext, error: discord.DiscordException
):
    notHandled = True
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="Take a break!",
            description=error,
            colour=bot.color(1),
        )
        await ctx.respond(embed=embed)
        notHandled = False
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Missing required permissions",
            description="You're not authorised to use this command!",
            colour=bot.color(1),
        )
        await ctx.respond(embed=embed)
        notHandled = False
    if isinstance(error, UserVABanned):
        embed = discord.Embed(
            title="You're banned from the VA!",
            description="Sadly you were banned from the ClearFly VA. You can't use any VA related commmands.",
            colour=bot.color(1),
        )
        await ctx.respond(embed=embed)
        notHandled = False
    if isinstance(error, ValueError):
        embed = discord.Embed(
            title="Incorrect Values",
            description="You gave some values that are incorrect/invalid to me, try again with correct ones!",
            colour=bot.color(1),
        )
        await ctx.respond(embed=embed)
        notHandled = False
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(
            title="Missing required roles",
            description="You're not authorised to use this command!",
            colour=bot.color(1),
        )
        await ctx.respond(embed=embed)
        notHandled = False
    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            title="Owner only command",
            description="This command is for the owner of the bot only, so not for you!",
            colour=bot.color(1),
        )
        await ctx.respond(embed=embed)
        notHandled = False
    if isinstance(error, commands.errors.NoPrivateMessage):
        embed = discord.Embed(
            title="This command cannot be used in DMs",
            colour=bot.color(1),
        )
        await ctx.respond(embed=embed)
        notHandled = False
    if notHandled:
        bot_author = bot.get_user(bot.bot_author)
        alert_emb = discord.Embed(
            title="Hey there!",
            colour=bot.color(),
            description=f"""
{ctx.author.mention} experienced some issues with me, please fix them as soon as possible! Error is provided below, more info can be found in the terminal.
```py
{error}
```
            """,
        )
        if not bot_author:
            bot_author_id = 0
        else:
            bot_author_id = bot_author.id

        if bot_author_id != ctx.author.id and bot_author:
            await bot_author.send(embed=alert_emb)
            embed = discord.Embed(
                title="Something went wrong...",
                description=f"""
We're sorry for the inconvenience. The bot author has been notified about this issue.
```{error}```
                    """,
                colour=bot.color(1),
            )
        else:
            embed = discord.Embed(
                title="Something went wrong...",
                description=f"""
See the terminal for more information.
```{error}```
                    """,
                colour=bot.color(1),
            )
        await ctx.respond(embed=embed)
        raise error


cogs = os.listdir("cogs")
cogs = [x.split(".")[0] for x in cogs if x.endswith(".py")]

if bot.dev_mode:
    args = sys.argv
    for arg in args:
        if arg.endswith(".py"):
            args.remove(arg)

    for arg in args:
        bot.load_extension(arg)

    bot.run(os.getenv("DEV_TOKEN"))
else:
    for cog in cogs:
        bot.load_extension(f"cogs.{cog}")

    bot.run(os.getenv("TOKEN"))
