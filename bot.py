import datetime
import os
import re
import sqlite3

import aiofiles
import aiosqlite
import discord
import requests
from discord.ext.pages import PaginatorButton


class UserObject(discord.Object):
    def __init__(self) -> None:
        self.id = 0
        self.name = "N/A"
        self.display_name = "N/A"
        self.global_name = "N/A"
        super().__init__(self.id)


class ClearBot(discord.Bot):
    def __init__(self, *args, **kwargs) -> None:
        self.color = self.embed_color
        self.dev_mode = os.path.exists(".dev")

        self.start_time = datetime.datetime.utcnow()
        self.cog_list = [
            x.split(".")[0] for x in os.listdir("cogs") if x.endswith(".py")
        ]

        resp = requests.get("https://github.com/mwgg/Airports/raw/master/airports.json")
        self.airports = resp.json()

        self.airports_ac = []

        for ap in self.airports:
            icao = self.airports[ap].get("icao")
            iata = self.airports[ap].get("iata")
            name = self.airports[ap].get("name")

            self.airports_ac.append(
                f"{icao if icao else 'N/A'}, {iata if iata else 'N/A'}, {name if name else 'N/A'}"
            )

        self.airports_icao = [
            self.airports[ap].get("icao")
            for ap in self.airports
            if self.airports[ap].get("icao")
        ]

        con = sqlite3.connect("main.db")
        # 0 = normal
        # 1 = halloween
        # 2 = Christmas
        self.theme = int(
            con.execute("SELECT value FROM config WHERE key='theme'").fetchone()[0]
        )
        con.close()

        self.paginator_buttons = [
            PaginatorButton("first", label="<<", style=discord.ButtonStyle.secondary),
            PaginatorButton("prev", label="<", style=discord.ButtonStyle.danger),
            PaginatorButton(
                "page_indicator", style=discord.ButtonStyle.gray, disabled=True
            ),
            PaginatorButton("next", label=">", style=discord.ButtonStyle.primary),
            PaginatorButton("last", label=">>", style=discord.ButtonStyle.secondary),
        ]

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

    async def setup_server(self) -> bool:
        file1 = discord.File(
            f"images/banners/{self.theme}/rules.png", filename="rules.png"
        )
        file2 = discord.File(f"images/banners/{self.theme}/faq.png", filename="faq.png")
        embed1 = discord.Embed(color=self.color()).set_image(
            url="attachment://rules.png"
        )
        embed2 = discord.Embed(
            color=self.color(),
            description="""
**1.** Don’t post any inappropriate content.

**2.** Use channels for their intended use.

**3.** Do not spam mention members.

**4.** Do not be overly political.

**5.** Use common sense.

**6.** Follow the [Discord TOS](https://discord.com/terms) and [Community Guidelines](https://discord.com/guidelines).

**7.** Use </report:1018970055972757506> to let us know about anyone breaking the rules.
        """,
        )
        embed3 = discord.Embed(colour=self.color()).set_image(
            url="attachment://faq.png"
        )
        embed4 = discord.Embed(
            description="""
**Q: What happened to the 737-100?**
A: We decided that the project was announced way too early. It is still in active development and a "re-announcement" will be made when significant progress has been made by the team.
        """,
            color=self.color(),
        )
        embed5 = discord.Embed(
            title="Links",
            description="""
- [X-Plane.org Forums](https://forums.x-plane.org/index.php?/forums/topic/265735-clearfly-boeing-737-100/&page=99999999999)
- [Discord](https://discord.gg/jjpwtusf6n)
                               """,
            colour=self.color(),
        )

        def check(msg: discord.Message) -> bool:
            return msg.author.bot

        info = self.get_channel(self.channels.get("info", 0))
        if isinstance(info, discord.TextChannel):
            await info.purge(check=check)
            await info.send(
                embeds=[embed1, embed2], view=RulesView(bot=self), file=file1
            )
            await info.send(embeds=[embed3, embed4], file=file2)
            await info.send(embed=embed5)
            return True
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

            async with aiofiles.open(
                os.path.join("images", "logo", str(theme), "logo.png"), "rb"
            ) as f:
                await guild.edit(icon=await f.read())

            guild_success = await self.setup_server()

        return {"guild_success": guild_success, "failed_roles": failed}

    async def send_log(self, *args, **kwargs) -> None:
        logs = self.get_channel(self.channels.get("logs", 0))
        if isinstance(logs, discord.TextChannel):
            await logs.send(*args, **kwargs)

    def is_valid_url(self, url: str) -> bool:
        pattern = "(http|https):\/\/([0-z]*)\..*"

        return True if re.search(pattern, url) else False

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


class RulesView(discord.ui.View):
    def __init__(self, bot: ClearBot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(
        label="I have read and accept the rules",
        custom_id="rulebutton",
        style=discord.ButtonStyle.secondary,
        emoji="<:ClearFly:1054526148576559184>",
    )
    async def button_callback(self, button, interaction):
        guild = self.bot.get_guild(self.bot.server_id)
        if not guild:
            await interaction.response.send_message(
                "Something went wrong while trying to verify your roles...",
                ephemeral=True,
            )
            return

        role = guild.get_role(self.bot.roles.get("member", 0))
        if role in interaction.user.roles:
            await interaction.response.send_message(
                "You already accepted the rules!", ephemeral=True
            )
        else:
            author = interaction.user
            await author.add_roles(role)
            await interaction.response.send_message(
                "Rules accepted, have fun in the server!", ephemeral=True
            )
