import re
import aiofiles
import aiohttp
import discord
import os
import configparser
import random
import pymongo
import feedparser
import time
from discord.ext import commands, tasks
from datetime import datetime
from main import cfc, errorc


adminids = [668874138160594985, 871893179450925148, 917477940650971227]
client = pymongo.MongoClient(os.environ["MONGODB_URI"])
db = client["ClearBotDB"]
rss = db["RSS"]
lvlcol = db["leveling"]
trescol = rss["Tresholdx"]
sfcol = rss["SimpleFlying"]
fsnews = 1066124540318588928  # *CB test 1001401783689678868
avnews = 1073311685357604956


class DeleteMsgView(discord.ui.View):
    def __init__(self, bot, auth):
        self.bot = bot
        self.auth = auth
        super().__init__(timeout=240.0, disable_on_timeout=True)

    @discord.ui.button(
        label="Delete Message",
        style=discord.ButtonStyle.danger,
    )
    async def button_callback(self, button, interaction: discord.Interaction):
        if interaction.user.id == self.auth.id:
            await interaction.message.delete()
        else:
            await interaction.response.send_message(
                "You did not send the link, so you can't delete the snippet!",
                ephemeral=True,
            )


class Listeners(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.presence.start()
        self.rssfeedtres1.start()
        self.rssfeedtres2.start()
        self.rssfeedtres3.start()
        self.resetRShownSubms.start()
        channel = self.bot.get_channel(1001405648828891187)
        now = discord.utils.format_dt(datetime.now())
        if os.path.exists(".onpc"):
            embed = discord.Embed(
                title="I started up!",
                description=f"""
Started bot up on {now}
*Data save available*
            """,
                color=0x00FF00,
            )
            await channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="I started up!",
                description=f"""
Started bot up on {now}
*Data save unavailable*
            """,
                color=0x00FF00,
            )
            await channel.send(embed=embed)
        print("| listeners cog loaded sucessfully")

    @tasks.loop(minutes=10)
    async def presence(self):
        statements = [
            "Give me Baby Boeing 😩",
            "Boeing > Airbus",
            "How are you doing?",
            "Use me please.",
            "How can I assist you today?",
            "BABY BOEINGGGG",
            "If it ain't Boeing, I ain't going.",
            "I'm tired",
            "Nuke airbus smh",
            "Boeing supremacy",
            "*Sends missile to Airbus hq*",
            "Wolfair = Chad",
            "Deep™",
            "What ya looking at 🤨",
            "What about you stfu.",
            "Goofy ah",
            "There's an impostor among us.",
            "Bored",
        ]
        await self.bot.change_presence(
            activity=discord.Game(name=f"/help | {random.choice(statements)}"),
            status=discord.Status.online,
        )

    @tasks.loop(seconds=60)
    async def rssfeedtres1(self):
        channel = self.bot.get_channel(fsnews)
        blog_feed = feedparser.parse("https://www.thresholdx.net/news/rss.xml")
        feed = dict(blog_feed.entries[0])
        lastID = trescol.find()
        ids = []
        for id in lastID:
            ids.append(id)
        if ids == []:
            ids = [{"lastID": None}]
        if ids[0]["lastID"] == feed.get("id"):
            return
        else:
            trescol.update_one({"_id": "lastID"}, {"$set": {"lastID": feed.get("id")}})
            await channel.send(
                f"""
**{feed.get('title')}**

{feed.get('link')}
                """
            )

    @tasks.loop(seconds=60)
    async def rssfeedtres2(self):
        channel = self.bot.get_channel(fsnews)
        blog_feed = feedparser.parse("https://www.thresholdx.net/opinion/rss.xml")
        feed = dict(blog_feed.entries[0])
        lastID = trescol.find()
        ids = []
        for id in lastID:
            ids.append(id)
        if ids == []:
            ids = [{"lastIDopinion": None}]
        if ids[1]["lastIDopinion"] == feed.get("id"):
            return
        else:
            trescol.update_one(
                {"_id": "lastIDopinion"}, {"$set": {"lastIDopinion": feed.get("id")}}
            )
            await channel.send(
                f"""
**{feed.get('title')}**

{feed.get('link')}
                """
            )

    @tasks.loop(seconds=60)
    async def rssfeedtres3(self):
        channel = self.bot.get_channel(fsnews)
        blog_feed = feedparser.parse("https://www.thresholdx.net/article/rss.xml")
        feed = dict(blog_feed.entries[0])
        lastID = trescol.find()
        ids = []
        for id in lastID:
            ids.append(id)
        if ids == []:
            ids = [{"lastIDarticle": None}]
        if ids[2]["lastIDarticle"] == feed.get("id"):
            return
        else:
            trescol.update_one(
                {"_id": "lastIDarticle"}, {"$set": {"lastIDarticle": feed.get("id")}}
            )
            await channel.send(
                f"""
**{feed.get('title')}**

{feed.get('link')}
                """
            )

    @tasks.loop(seconds=60)
    async def rssfeedsf1(self):
        channel = self.bot.get_channel(avnews)
        blog_feed = feedparser.parse("https://simpleflying.com/feed")
        feed = dict(blog_feed.entries[0])
        lastID = sfcol.find()
        ids = []
        for id in lastID:
            ids.append(id)
        if ids == []:
            ids = [{"lastID": None}]
        if ids[0]["lastID"] == feed.get("id"):
            return
        else:
            sfcol.update_one({"_id": "lastID"}, {"$set": {"lastID": feed.get("id")}})
            await channel.send(
                f"""
**{feed.get('title').replace('&quot;', '"')}**

{feed.get('link')}
                """
            )

    @tasks.loop(hours=36.0)
    async def resetRShownSubms(self):
        self.bot.rshownsubms = []

    @commands.Cog.listener("on_message")
    async def levellisten(self, message):
        nowlvlnom = 0
        if message.channel.id == 966077223260004402:
            return
        if message.channel.id == 965600413376200726:
            return
        if message.author.bot:
            return
        else:
            usrs = []
            for usr in lvlcol.find():
                usrs.append(usr.get("id"))
            if message.author.id in usrs:
                usrdata = lvlcol.find_one({"id": message.author.id})
                belvlnom = usrdata.get("nom", 0)
                last = usrdata.get("last_msg", 0)
                now = round(time.time())
                if (now - int(last)) < 5:
                    return
                else:
                    lvlcol.update_one(
                        {"id": message.author.id}, {"$set": {"last_msg": now}}
                    )
                if len(message.content) == 0:
                    nowlvlnom = int(belvlnom) + 1
                if len(message.content) > 0:
                    nowlvlnom = int(belvlnom) + 1
                if len(message.content) > 10:
                    nowlvlnom = int(belvlnom) + 2
                if len(message.content) > 25:
                    nowlvlnom = int(belvlnom) + 5
                if len(message.content) > 50:
                    nowlvlnom = int(belvlnom) + 7
                if len(message.content) > 75:
                    nowlvlnom = int(belvlnom) + 10
                lvl = usrdata.get("level", 0)
                denom = usrdata.get("denom", 0)
                lvlcol.update_one(
                    {"id": message.author.id}, {"$set": {"nom": nowlvlnom}}
                )
                if int(nowlvlnom) >= int(denom):
                    lvlcol.update_one({"id": message.author.id}, {"$set": {"nom": 0}})
                    lvlcol.update_one(
                        {"id": message.author.id}, {"$set": {"level": lvl + 1}}
                    )
                    if int(lvl) == 0:
                        lvl = 1
                    lvlcol.update_one(
                        {"id": message.author.id},
                        {"$set": {"denom": int(denom) + (int(lvl) * 20)}},
                    )
                    lvlp = usrdata.get("level", "N/A")
                    await message.channel.send(
                        f"{message.author.mention} :partying_face: You reached level {lvlp}!"
                    )
            else:
                lvlcol.insert_one(
                    {
                        "id": message.author.id,
                        "level": lvl,
                        "nom": 1,
                        "denom": 25,
                        "last_msg": round(time.time()),
                    }
                )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(965600413376200726)
        emb = discord.Embed(
            title=f"Welcome to ClearFly!",
            description=f"Hey there, {member.mention}! Be sure to read the <#1002194493304479784> to become a member and gain full access to the server! Thanks for joining!",
            color=cfc,
        )
        await channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(1001405648828891187)
        emb = discord.Embed(
            title=f"{member} left.",
            color=cfc,
            description=f"Joined on {discord.utils.format_dt(member.joined_at)}",
        )
        pfp = member.display_avatar.url
        emb.set_thumbnail(url=pfp)
        await channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        class ViewRawMessage(discord.ui.View):
            def __init__(self, bot):
                self.bot = bot
                super().__init__(timeout=None)

            @discord.ui.button(
                label="View Raw Contents", style=discord.ButtonStyle.primary
            )
            async def viewRawButtonCallback(self, button, interaction):
                if message.content == "":
                    message.content = "None"
                message.content = message.content.replace("```", "`` `")
                await interaction.response.send_message(
                    f"""
Message Content:
```md
{message.content}
```
                """,
                    ephemeral=True,
                )

        if message.author.bot == False:
            channel = self.bot.get_channel(1001405648828891187)
            msgcontent = message.clean_content
            if msgcontent == "":
                msgcontent = "None"
            msgatr = message.author.mention
            msgcnl = message.channel.mention
            embs = []
            if message.attachments != []:
                for attach in message.attachments:
                    if attach.content_type[:5] == "image":
                        embs.append(
                            discord.Embed(
                                title="Attachment deleted",
                                url=attach.url,
                                colour=cfc,
                            )
                            .set_image(url=attach.url)
                            .set_footer(
                                text="If the image doesn't load, try opening it in your browser by clicking the title."
                            )
                        )
                    else:
                        embs.append(
                            discord.Embed(
                                title="Attachment deleted",
                                url=attach.url,
                                description="*Attachment is* ***not*** *image*",
                                colour=cfc,
                            ).set_footer(
                                text="If the image doesn't load, try opening it in your browser by clicking the title."
                            )
                        )
            pfp = message.author.display_avatar.url
            embed = discord.Embed(title="Message Deleted", color=cfc)
            embed.add_field(name="Content", value=f"{msgcontent[:1024]}", inline=False)
            embed.add_field(name="Author", value=f"{msgatr}", inline=True)
            embed.add_field(name="Channel", value=f"{msgcnl}", inline=True)
            embed.add_field(
                name="Other Information",
                value=f"""
Pinned: **{message.pinned}**
Type: **{message.type}**
ID: **{message.id}**
                """,
            )
            embed.set_thumbnail(url=pfp)
            embs.append(embed)
            await channel.send(embeds=embs, view=ViewRawMessage(self.bot))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        class ViewRawMessage(discord.ui.View):
            def __init__(self, bot):
                self.bot = bot
                super().__init__(timeout=None)

            @discord.ui.button(
                label="View Raw Contents", style=discord.ButtonStyle.primary
            )
            async def viewRawButtonCallback(self, button, interaction):
                if before.content == "":
                    before.content = "None"
                if after.content == "":
                    after.content = "None"
                before.content, after.content = before.content.replace(
                    "```", "` ` `"
                ), after.content.replace("```", "`` `")
                await interaction.response.send_message(
                    f"""
Before:
```md
{before.content}
```
After:
```md
{after.content}
```
                """,
                    ephemeral=True,
                )

        if before.author.bot == False:
            if before.content == after.content:
                pass
            else:
                channel = self.bot.get_channel(1001405648828891187)
                msgeditb = before.clean_content
                msgedita = after.clean_content
                msgatr = before.author.mention
                msgcnl = before.channel.mention
                pfp = before.author.display_avatar.url
                emb = discord.Embed(
                    title="Message Edited",
                    color=cfc,
                    url=f"https://discord.com/channels/965419296937365514/{after.channel.id}/{after.id}",
                )
                emb.add_field(
                    name="Content before", value=f"{msgeditb[:1024]}", inline=False
                )
                emb.add_field(
                    name="Content after", value=f"{msgedita[:1024]}", inline=False
                )
                emb.add_field(name="Author", value=f"{msgatr}", inline=True)
                emb.add_field(name="Channel", value=f"{msgcnl}", inline=True)
                emb.add_field(
                    name="Other Information",
                    value=f"""
Pinned: **{after.pinned}**
Type: **{after.type}**
ID: **{after.id}**
                """,
                )
                emb.set_thumbnail(url=pfp)
                await channel.send(embed=emb, view=ViewRawMessage(self.bot))

    @commands.Cog.listener()
    async def on_guild_channel_update(
        self, before: discord.channel, after: discord.channel
    ):
        channel = self.bot.get_channel(1001405648828891187)
        embed = discord.Embed(title=f"Channel Updated", colour=cfc)
        embed.add_field(name="", value=after.mention, inline=False)
        if before.name != after.name:
            embed.add_field(
                name="Name",
                value=f"""
Before: **{before.name}**
After: **{after.name}**
            """,
                inline=False,
            )
        if (str(before.type) or str(after.type)) == "text":
            if before.topic != after.topic:
                embed.add_field(
                    name="Topic",
                    value=f"""
Before:
> {before.topic}
After:
> {after.topic}
            """,
                    inline=False,
                )
            if before.slowmode_delay != after.slowmode_delay:
                embed.add_field(
                    name="Slowmode",
                    value=f"""
Before: **{before.slowmode_delay}**s
After: **{after.slowmode_delay}**s
                """,
                    inline=False,
                )
        if before.permissions_synced != after.permissions_synced:
            embed.add_field(
                name="Synced Permissions",
                value=f"""
Before: **{before.permissions_synced}**
After: **{after.permissions_synced}**
            """,
                inline=False,
            )
        if before.category != after.category:
            embed.add_field(
                name="Category",
                value=f"""
Before: **{before.category}**
After: **{after.category}**
            """,
                inline=False,
            )
        if before.overwrites != after.overwrites:
            permoverwritesB = {}
            permoverwritesA = {}
            out = []
            for key, val in before.overwrites.items():
                itobj = iter(before.overwrites[key])
                for perm in before.overwrites[key]:
                    it = next(itobj)
                    if it[1] == None:
                        continue
                    else:
                        permoverwritesB.setdefault(key.id, []).append(it)
            for key, val in after.overwrites.items():
                itobj = iter(after.overwrites[key])
                for perm in after.overwrites[key]:
                    it = next(itobj)
                    if it[1] == None:
                        continue
                    else:
                        permoverwritesA.setdefault(key.id, []).append(it)
            permoverwrites = {}
            for id in permoverwritesA:
                diffA = set(permoverwritesA[id]) - set(permoverwritesB[id])
                diffB = set(permoverwritesB[id]) - set(permoverwritesA[id])
                permoverwrites.setdefault(id, []).append(diffA)
                if (list(diffA) == []) and (list(diffB) == []):
                    continue
                else:
                    perms = []
                    if self.bot.get_user(id):
                        mention = f"<@{id}>"
                    else:
                        mention = f"<@&{id}>"
                    for perm in list(permoverwrites[id])[0]:
                        if list(diffB) == []:
                            diffB = {(perm, "None")}
                        if list(diffA) == []:
                            diffA = {(perm, "None")}
                        perms.append(
                            str(perm[0])
                            + " : "
                            + str(list(diffB)[0][1])
                            + " -> "
                            + str(perm[1])
                        )
                    fperm = (
                        "\n".join(perms)
                        .replace("True", "✅")
                        .replace("False", "❌")
                        .replace("None", "◻️")
                    )
                    out.append(
                        f"""
{mention}
{fperm}
                        """
                    )
            embed.add_field(name="Permissions", value="\n".join(out), inline=False)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.bot == False:
            channel = self.bot.get_channel(1001405648828891187)
            if before.name != after.name:
                embed = discord.Embed(
                    title=f"{before} changed their name to `{after.name}`.", colour=cfc
                )
                embed.set_thumbnail(url=after.display_avatar.url)
                await channel.send(embed=embed)
            if before.display_name != after.display_name:
                embed = discord.Embed(
                    title=f"{before} changed their nickname to `{after.display_name}`.",
                    colour=cfc,
                )
                embed.set_thumbnail(url=after.display_avatar.url)
                await channel.send(embed=embed)
            if before.discriminator != after.discriminator:
                embed = discord.Embed(
                    title=f"{before} changed their discriminator to `{after.discriminator}`.",
                    colour=cfc,
                )
                embed.set_thumbnail(url=after.display_avatar.url)
                await channel.send(embed=embed)
            if before.roles != after.roles:
                embed = discord.Embed(
                    title=f"{before} got their roles changed.", colour=cfc
                )
                brole = [str(role.id) for role in before.roles]
                brole = ["<@&" + str(role) for role in brole]
                brole = [str(role) + ">" for role in brole]
                arole = [str(role.id) for role in after.roles]
                arole = ["<@&" + str(role) for role in arole]
                arole = [str(role) + ">" for role in arole]
                difr = set(brole) - set(arole)
                difa = set(arole) - set(brole)
                if difr == set():
                    difr = None
                else:
                    difr = "\n".join(list(difr))
                if difa == set():
                    difa = None
                else:
                    difa = "\n".join(list(difa))
                embed.add_field(name="Roles removed:", value=difr)
                embed.add_field(name="Roles added:", value=difa)
                embed.set_thumbnail(url=after.display_avatar.url)
                await channel.send(embed=embed)
            if before.display_avatar != after.display_avatar:
                embed = discord.Embed(
                    title=f"{before} changed their avatar to the following image.",
                    colour=cfc,
                )
                embed.set_image(url=after.display_avatar.url)
                await channel.send(embed=embed)
        else:
            pass

    @commands.Cog.listener("on_message")
    async def scamcheck(self, message):
        class BanView(discord.ui.View):
            def __init__(self, bot):
                self.bot = bot
                super().__init__(timeout=None)

            @discord.ui.button(
                label=f"Ban {message.author}", style=discord.ButtonStyle.danger
            )
            async def button_callback(self, button, interaction):
                try:
                    await message.author.ban(
                        reason=f"{message.author} sent a scam, confirmed by {interaction.user}"
                    )
                    embed = discord.Embed(
                        title=f"Successfully banned `{message.author}`", colour=0x00FF00
                    )
                    await interaction.response.send_message(embed=embed)
                except Exception as error:
                    embed = discord.Embed(
                        title=f"While trying to ban `{message.author}`, I got the following error:",
                        description=f"\n```{error}\n```",
                        colour=errorc,
                    )
                    await interaction.response.send_message(embed=embed)

        def scamChecker(string):
            change = 0
            blacklist = ["@everyone", "@here", "porn", "nudes", "crypto", "free nitro"]
            for i in blacklist:
                if blacklist[change] in string:
                    return True
                change += 1

        if message.author.id not in adminids:
            if scamChecker(message.clean_content):
                await message.reply(
                    content="Your message included blacklisted words, and has been deleted."
                )
                channel = self.bot.get_channel(1001405648828891187)
                embed = discord.Embed(
                    title=f"`{message.author}` might have sent a scam",
                    description=message.content,
                    colour=errorc,
                )
                await message.delete(reason=f"{message.author} might have sent a scam.")
                await channel.send(embed=embed, view=BanView(bot=self.bot))
            else:
                pass
        else:
            pass

    @commands.Cog.listener("on_message")
    async def github_snippet(self, message):
        if not message.author.bot:
            match = re.search(
                r"https?://github\.com/[\w-]+/[\w-]+/[\w./-]+#L(\d+)-L(\d+)",
                message.content,
            )
            if match:
                random.seed(message.content)
                snip_id = random.randint(0, 100)
                url = match.group()
                start_line = match.group(1)
                end_line = match.group(2)
                if (int(end_line) - int(start_line)) > 25:
                    return
                raw_url = url.replace(
                    "github.com", "raw.githubusercontent.com"
                ).replace("/blob", "")
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(raw_url) as r:
                        async with aiofiles.open(f"snip{snip_id}.txt", "wb") as f:
                            await f.write(await r.content.read())
                async with aiofiles.open(f"snip{snip_id}.txt", "r") as f:
                    snip = await f.readlines()

                file_name = url.split("/")[len(url.split("/")) - 1].split("#")[0]
                syntaxh = file_name.split(".")[1]
                out_snip = "".join(snip[int(start_line) - 1 : int(end_line)])
                await message.reply(
                    f"""
`{url.split("/")[3]}/{url.split("/")[4]}`: `{file_name}` line **{start_line}**-**{end_line}**
```{syntaxh}
{out_snip}
```
                """,
                    view=DeleteMsgView(bot=self.bot, auth=message.author),
                )
                os.remove(f"snip{snip_id}.txt")

    @commands.Cog.listener()
    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error: discord.DiscordException
    ):
        notHandled = True
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Take a break!",
                description=error,
                colour=errorc,
            )
            await ctx.respond(embed=embed)
            notHandled = False
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Missing required permissions",
                description="You're not authorised to use this command!",
                colour=errorc,
            )
            await ctx.respond(embed=embed)
            notHandled = False
        if isinstance(error, commands.MissingRole):
            embed = discord.Embed(
                title="Missing required roles",
                description="You're not authorised to use this command!",
                colour=errorc,
            )
            await ctx.respond(embed=embed)
            notHandled = False
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="Owner only command",
                description="This command is for the owner of the bot only, so not for you!",
                colour=errorc,
            )
            await ctx.respond(embed=embed)
            notHandled = False
        if notHandled == True:
            embed = discord.Embed(
                title="Something went wrong...",
                description=f"```{error}```",
                colour=errorc,
            )
            await ctx.respond(embed=embed)
            raise error


def setup(bot):
    bot.add_cog(Listeners(bot=bot))
