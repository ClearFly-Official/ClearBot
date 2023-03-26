import discord
import os
import configparser
import glob
import re
import pymongo
from pilmoji import Pilmoji
from numerize import numerize as n
from PIL import Image, ImageDraw, ImageFont
from discord import option
from discord.ext import commands
from main import cfc, errorc

client = pymongo.MongoClient(os.environ["MONGODB_URI"])
db = client["ClearBotDB"]
lvlcol = db["leveling"]

class LevelingCommands(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    leveling = discord.SlashCommandGroup(
        name="level", description="Commands related to leveling"
    )

    @commands.Cog.listener()
    async def on_ready(self):
        print("| Leveling cog loaded sucessfully")

    @leveling.command(
        name="userlevel", description="🥇 Gets the provided user's level."
    )
    @option("user", description="The user you want level information about.")
    async def userlevel(
        self, ctx: discord.ApplicationContext, user: discord.Member = None
    ):
        await ctx.defer()
        if user == None:
            user = ctx.author
        usrs = []
        for usr in lvlcol.find():
            usrs.append(usr.get(id))
        if user.id in usrs:
            usrdata = lvlcol.find_one({"id":user.id})
            x1, y1 = 860, 547
            x2, y2 = 2740, 710
            img = Image.open("images/userlevelClear.png")
            await user.display_avatar.save("images/avatarorigin.png")
            avatarorigin = Image.open("images/avatarorigin.png")
            avatar = avatarorigin.resize((256, 256))
            avatar.save("images/avatar.png")
            avatar = Image.open("images/avatar.png")
            lvlnom = usrdata.get("nom", 0)
            lvl = usrdata.get("level", 0)
            lvldenom = usrdata.get("denom", 1)
            h, w = avatar.size
            avmask = Image.new("L", (h, w), 0)
            clear = Image.new("RGBA", (h, w), 1)
            draw = ImageDraw.Draw(avmask)
            draw.ellipse((0, 0, 256, 256), fill=255)
            masked = Image.composite(avatar, clear, mask=avmask)
            font = ImageFont.truetype(
                "fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf",
                size=100,
                layout_engine=ImageFont.Layout.BASIC,
            )
            fontbig = ImageFont.truetype(
                "fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf",
                size=150,
                layout_engine=ImageFont.Layout.BASIC,
            )
            img.paste(
                masked.resize((612, 612)), (49, 82), mask=masked.resize((612, 612))
            )
            with Pilmoji(img) as pilmoji:
                pilmoji.text(
                    (860, 120), str(user.name), fill=(255, 255, 255), font=fontbig
                )
                pilmoji.text(
                    (2310, 120),
                    f"#{user.discriminator}",
                    fill=(200, 200, 200),
                    font=fontbig,
                    emoji_position_offset=(0, 10),
                )
                pilmoji.text(
                    (900, 380),
                    f"LVL: {n.numerize(int(lvl))}",
                    fill=(255, 255, 255),
                    font=font,
                    emoji_position_offset=(0, 10),
                )
                x3, y3 = x1, y1
                x4, y4 = x1 + ((x2 - x1) * (int(lvlnom) / int(lvldenom))), y2
                pilmoji.text(
                    (2000, 380),
                    f"XP: {n.numerize(int(lvlnom))} / {n.numerize(int(lvldenom))}",
                    fill=(255, 255, 255),
                    font=font,
                    emoji_position_offset=(0, 10),
                )
            bar = Image.new("RGBA", img.size, 1)
            I3 = ImageDraw.ImageDraw(bar)
            I3.ellipse(
                (x1 - ((y2 - y1) / 2), y1, x1 + ((y2 - y1) / 2), y2), fill=(9, 57, 97)
            )
            I3.ellipse(
                (x2 - ((y2 - y1) / 2), y1, x2 + ((y2 - y1) / 2), y2), fill=(9, 57, 97)
            )
            I3.rectangle((x1, y1, x2, y2), fill=(9, 57, 97))
            I3.rectangle((x3, y3, x4, y4), fill=(38, 129, 180))
            I3.ellipse(
                (x1 - ((y2 - y1) / 2), y1, x1 + ((y2 - y1) / 2), y2),
                fill=(38, 129, 180),
            )
            I3.ellipse(
                (x4 - ((y2 - y1) / 2), y1, x4 + ((y2 - y1) / 2), y4),
                fill=(38, 129, 180),
            )
            img.paste(bar, mask=bar)
            img.save("images/userlevel.png")
            file = discord.File(f"images/userlevel.png", filename="userlevel.png")
            embed = discord.Embed(color=cfc)
            embed.set_image(url=f"attachment://userlevel.png")
            await ctx.respond(embed=embed, file=file)
        else:
            if user.bot == True:
                embed = discord.Embed(
                    title="Error 404!",
                    description="I didn't found any data of leveling, because the provided user is a bot. They don't get to use this amazing leveling system!",
                    color=errorc,
                )
                await ctx.respond(embed=embed)
            else:
                if user == None:
                    embed = discord.Embed(
                        title="Error 404!",
                        description=f"This most probably means that you never sent a message in this server.",
                        color=errorc,
                    )
                else:
                    embed = discord.Embed(
                        title="Error 404!",
                        description=f"This most probably means that {user.mention} never sent a message in this server.",
                        color=errorc,
                    )
                await ctx.respond(embed=embed)

    @discord.user_command(
        name="User Level", description="🥇 Gets the provided user's level."
    )
    async def userlevel_app(
        self, ctx: discord.ApplicationContext, user: discord.Member = None
    ):
        await ctx.defer()
        if user == None:
            user = ctx.author
        usrs = []
        for usr in lvlcol.find():
            usrs.append(usr.get(id))
        if user.id in usrs:
            usrdata = lvlcol.find_one({"id":user.id})
            x1, y1 = 860, 547
            x2, y2 = 2740, 710
            img = Image.open("images/userlevelClear.png")
            await user.display_avatar.save("images/avatarorigin.png")
            avatarorigin = Image.open("images/avatarorigin.png")
            avatar = avatarorigin.resize((256, 256))
            avatar.save("images/avatar.png")
            avatar = Image.open("images/avatar.png")
            lvlnom = usrdata.get("nom", 0)
            lvl = usrdata.get("level", 0)
            lvldenom = usrdata.get("denom", 1)
            h, w = avatar.size
            avmask = Image.new("L", (h, w), 0)
            clear = Image.new("RGBA", (h, w), 1)
            draw = ImageDraw.Draw(avmask)
            draw.ellipse((0, 0, 256, 256), fill=255)
            masked = Image.composite(avatar, clear, mask=avmask)
            font = ImageFont.truetype(
                "fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf",
                size=100,
                layout_engine=ImageFont.Layout.BASIC,
            )
            fontbig = ImageFont.truetype(
                "fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf",
                size=150,
                layout_engine=ImageFont.Layout.BASIC,
            )
            img.paste(
                masked.resize((612, 612)), (49, 82), mask=masked.resize((612, 612))
            )
            with Pilmoji(img) as pilmoji:
                pilmoji.text(
                    (860, 120), str(user.name), fill=(255, 255, 255), font=fontbig
                )
                pilmoji.text(
                    (2310, 120),
                    f"#{user.discriminator}",
                    fill=(200, 200, 200),
                    font=fontbig,
                    emoji_position_offset=(0, 10),
                )
                pilmoji.text(
                    (900, 380),
                    f"LVL: {n.numerize(int(lvl))}",
                    fill=(255, 255, 255),
                    font=font,
                    emoji_position_offset=(0, 10),
                )
                x3, y3 = x1, y1
                x4, y4 = x1 + ((x2 - x1) * (int(lvlnom) / int(lvldenom))), y2
                pilmoji.text(
                    (2000, 380),
                    f"XP: {n.numerize(int(lvlnom))} / {n.numerize(int(lvldenom))}",
                    fill=(255, 255, 255),
                    font=font,
                    emoji_position_offset=(0, 10),
                )
            bar = Image.new("RGBA", img.size, 1)
            I3 = ImageDraw.ImageDraw(bar)
            I3.ellipse(
                (x1 - ((y2 - y1) / 2), y1, x1 + ((y2 - y1) / 2), y2), fill=(9, 57, 97)
            )
            I3.ellipse(
                (x2 - ((y2 - y1) / 2), y1, x2 + ((y2 - y1) / 2), y2), fill=(9, 57, 97)
            )
            I3.rectangle((x1, y1, x2, y2), fill=(9, 57, 97))
            I3.rectangle((x3, y3, x4, y4), fill=(38, 129, 180))
            I3.ellipse(
                (x1 - ((y2 - y1) / 2), y1, x1 + ((y2 - y1) / 2), y2),
                fill=(38, 129, 180),
            )
            I3.ellipse(
                (x4 - ((y2 - y1) / 2), y1, x4 + ((y2 - y1) / 2), y4),
                fill=(38, 129, 180),
            )
            img.paste(bar, mask=bar)
            img.save("images/userlevel.png")
            file = discord.File(f"images/userlevel.png", filename="userlevel.png")
            embed = discord.Embed(color=cfc)
            embed.set_image(url=f"attachment://userlevel.png")
            await ctx.respond(embed=embed, file=file)
        else:
            if user.bot == True:
                embed = discord.Embed(
                    title="Error 404!",
                    description="I didn't found any data of leveling, because the provided user is a bot. They don't get to use this amazing leveling system!",
                    color=errorc,
                )
                await ctx.respond(embed=embed)
            else:
                if user == None:
                    embed = discord.Embed(
                        title="Error 404!",
                        description=f"This most probably means that you never sent a message in this server.",
                        color=errorc,
                    )
                else:
                    embed = discord.Embed(
                        title="Error 404!",
                        description=f"This most probably means that {user.mention} never sent a message in this server.",
                        color=errorc,
                    )
                await ctx.respond(embed=embed)

    @leveling.command(
        name="leaderboard", description="📊 See the leaderboard of the whole server."
    )
    async def lb(self, ctx: discord.ApplicationContext):
            await ctx.defer()
            output = []
            nameoutput = []
            img = Image.open(f"images/lbClear.png")
            for usr in lvlcol.find():
                lvl = usr.get("level", 0)
                lvlnom = usr.get("nom", 0)
                lvldenom = usr.get("denom", 0)
                user = await self.bot.fetch_user(int(usr.get("id", 0)))
                line = f"""
      {lvlnom+lvldenom*lvl} LVL: {lvl} XP: {lvlnom}/{n.numerize(lvldenom)}\n
        """
                output.append(line)
                line2 = f"""
        {lvlnom+lvldenom*lvl} {user.name}\n
      """
                nameoutput.append(line2)

            def atoi(text):
                return int(text) if text.isdigit() else text

            def natural_keys(text):
                return [atoi(c) for c in re.split("(\d+)", text)]

            output.sort(key=natural_keys, reverse=True)
            nameoutput.sort(key=natural_keys, reverse=True)

            def delstr(lst):
                return [f"{' '.join(elem.split()[1:]).rstrip()}" for elem in lst]

            output = delstr(output)
            nameoutput = delstr(nameoutput)

            nameoutput = [f"{index}       {i}" for index, i in enumerate(nameoutput, 1)]
            output = [direction + "\n\n" for direction in output]
            nameoutput = [direction + "\n\n" for direction in nameoutput]
            embed = discord.Embed(
                title="ClearFly Level Leaderboard",
                description=f"""
Chat to earn xp!
            """,
                color=cfc,
            )
            font = ImageFont.truetype(
                "fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf",
                size=43,
                layout_engine=ImageFont.Layout.BASIC,
            )
            with Pilmoji(img) as pilmoji:
                pilmoji.text(
                    (800, 30),
                    "".join(output[:10]),
                    fill=(255, 255, 255),
                    font=font,
                    emoji_position_offset=(0, 20),
                )
                pilmoji.text(
                    (27, 30),
                    "".join(nameoutput[:10]),
                    fill=(255, 255, 255),
                    font=font,
                    emoji_position_offset=(0, 20),
                )
            img.save(f"images/lb.png")
            file = discord.File(f"images/lb.png", filename="lb.png")
            embed.set_image(url=f"attachment://lb.png")
            await ctx.respond(embed=embed, file=file)


def setup(bot):
    bot.add_cog(LevelingCommands(bot))