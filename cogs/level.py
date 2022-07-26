import discord
import os
import configparser
import glob
import re
from numerize import numerize as n
from PIL import Image, ImageDraw, ImageFont
from discord import option
from discord.ext import commands

#cfc = 0x2681b4 #<- default color
#cfc = 0xcc8d0e # <- halloween color
cfc = 0x00771d # <- christmas color
errorc = 0xFF0000


class LevelingCommands(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    leveling = discord.SlashCommandGroup(name="level", description="Commands related to leveling")

    @leveling.command(name="userlevel", description="Gets the provided user's level.")
    @option("user", description="The user you want level information about.")
    async def userlevel(self, ctx, user: discord.Member = None):
        await ctx.defer()
        config = configparser.ConfigParser()
        x1, y1 = 860, 547
        x2, y2 = 2740, 710
        img = Image.open("images/userlevelClear.png")
        if user == None:
            await ctx.author.avatar.save("images/avatarorigin.png")
            avatarorigin = Image.open("images/avatarorigin.png")
            avatar = avatarorigin.resize((256, 256))
            avatar.save("images/avatar.png")
            avatar = Image.open("images/avatar.png")
            if os.path.exists(f"Leveling/users/{ctx.author.id}/data.ini"):
                config.read(f"Leveling/users/{ctx.author.id}/data.ini")
                lvlprog = config.get("Level", "lvlprog")
                lvl = config.get("Level", "lvl")
                topprog = config.get("Level", "topprog")
                h,w = avatar.size
                avmask = Image.new('L', (h, w), 0)
                clear = Image.new('RGBA', (h, w), 1)
                draw = ImageDraw.Draw(avmask)
                draw.ellipse((0,0,256, 256), fill=255)
                masked = Image.composite(avatar, clear, mask=avmask)
                font = ImageFont.truetype("fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf", size=100, layout_engine=ImageFont.Layout.BASIC)
                fontbig = ImageFont.truetype("fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf", size=150, layout_engine=ImageFont.Layout.BASIC)
                img.paste(masked.resize((612, 612)), (49, 82), mask=masked.resize((612, 612)))
                I1 = ImageDraw.ImageDraw(img)
                I1.text((860, 120), str(ctx.author.name), fill=(255, 255, 255), font=fontbig)
                I1.text((2310, 120), f"#{ctx.author.discriminator}", fill=(200, 200, 200), font=fontbig)
                I1.text((900, 380), f"LVL: {n.numerize(int(lvl))}", fill=(255, 255, 255), font=font)
                x3, y3 = x1, y1
                x4, y4 = x1+((x2-x1)*(int(lvlprog)/int(topprog))), y2
                I1.text((2000,380), f"XP: {n.numerize(int(lvlprog))} / {n.numerize(int(topprog))}", fill=(255, 255, 255), font=font)
                bar = Image.new('RGBA', img.size, 1)
                I3 = ImageDraw.ImageDraw(bar)
                I3.ellipse((x1-((y2-y1)/2), y1, x1+((y2-y1)/2), y2), fill=(119, 0, 18))
                I3.ellipse((x2-((y2-y1)/2), y1, x2+((y2-y1)/2), y2), fill=(119, 0, 18))
                I3.rectangle((x1, y1, x2, y2), fill=(119, 0, 18))
                I3.rectangle((x3, y3, x4, y4), fill=(0, 119, 29))
                I3.ellipse((x1-((y2-y1)/2), y1, x1+((y2-y1)/2), y2), fill=(0, 119, 29))
                I3.ellipse((x4-((y2-y1)/2), y1, x4+((y2-y1)/2), y4), fill=(0, 119, 29))
                img.paste(bar, mask=bar)
                img.save("images/userlevel.png")
                file = discord.File(f"images/userlevel.png", filename="userlevel.png")
                embed = discord.Embed(color=cfc)
                embed.set_image(url=f"attachment://userlevel.png")
                await ctx.respond(embed=embed, file=file)
            else:
                embed = discord.Embed(title="Error 404!", description="This most probably means that you never sent a message (slash commands or messages before the introduction of leveling don't count in this server).", color=errorc)
                await ctx.respond(embed=embed)
        else:
            await user.avatar.save("images/avatarorigin.png")
            avatarorigin = Image.open("images/avatarorigin.png")
            avatar = avatarorigin.resize((256, 256))
            avatar.save("images/avatar.png")
            avatar = Image.open("images/avatar.png")
            if os.path.exists(f"Leveling/users/{user.id}/data.ini"):
                config.read(f"Leveling/users/{user.id}/data.ini")
                lvlprog = config.get("Level", "lvlprog")
                lvl = config.get("Level", "lvl")
                topprog = config.get("Level", "topprog")
                h,w = avatar.size
                avmask = Image.new('L', (h, w), 0)
                clear = Image.new('RGBA', (h, w), 1)
                draw = ImageDraw.Draw(avmask)
                draw.ellipse((0,0,256, 256), fill=255)
                masked = Image.composite(avatar, clear, mask=avmask)
                font = ImageFont.truetype("fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf", size=100, layout_engine=ImageFont.Layout.BASIC)
                fontbig = ImageFont.truetype("fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf", size=150, layout_engine=ImageFont.Layout.BASIC)
                img.paste(masked.resize((612, 612)), (49, 82), mask=masked.resize((612, 612)))
                I1 = ImageDraw.ImageDraw(img)
                I1.text((860, 120), str(user.name), fill=(255, 255, 255), font=fontbig)
                I1.text((2310, 120), f"#{user.discriminator}", fill=(200, 200, 200), font=fontbig)
                I1.text((900, 380), f"LVL: {n.numerize(int(lvl))}", fill=(255, 255, 255), font=font)
                x3, y3 = x1, y1
                x4, y4 = x1+((x2-x1)*(int(lvlprog)/int(topprog))), y2
                I1.text((2000,380), f"XP: {n.numerize(int(lvlprog))} / {n.numerize(int(topprog))}", fill=(255, 255, 255), font=font)
                bar = Image.new('RGBA', img.size, 1)
                I3 = ImageDraw.ImageDraw(bar)
                I3.ellipse((x1-((y2-y1)/2), y1, x1+((y2-y1)/2), y2), fill=(119, 0, 18))
                I3.ellipse((x2-((y2-y1)/2), y1, x2+((y2-y1)/2), y2), fill=(119, 0, 18))
                I3.rectangle((x1, y1, x2, y2), fill=(119, 0, 18))
                I3.rectangle((x3, y3, x4, y4), fill=(0, 119, 29))
                I3.ellipse((x1-((y2-y1)/2), y1, x1+((y2-y1)/2), y2), fill=(0, 119, 29))
                I3.ellipse((x4-((y2-y1)/2), y1, x4+((y2-y1)/2), y4), fill=(0, 119, 29))
                img.paste(bar, mask=bar)
                img.save("images/userlevel.png")
                file = discord.File(f"images/userlevel.png", filename="userlevel.png")
                embed = discord.Embed(color=cfc)
                embed.set_image(url=f"attachment://userlevel.png")
                await ctx.respond(embed=embed, file=file)
            else:
                if user.bot == True:
                    embed = discord.Embed(title="Error 404!", description="I didn't found any data of leveling, because the provided user is a bot. They don't get to use this amazing leveling system!", color=errorc)
                    await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(title="Error 404!", description="This most probably means that you never sended a message(slash commands or messages before the introduction of leveling don't count) in this server.", color=errorc)
                    await ctx.respond(embed=embed)

    @discord.user_command(name="User Level", description="Gets the provided user's level.")
    async def userlevel_app(self, ctx, user: discord.Member = None):
        await ctx.defer()
        config = configparser.ConfigParser()
        x1, y1 = 860, 547
        x2, y2 = 2740, 710
        img = Image.open("images/userlevelClear.png")
        if user == None:
            await ctx.author.avatar.save("images/avatarorigin.png")
            avatarorigin = Image.open("images/avatarorigin.png")
            avatar = avatarorigin.resize((256, 256))
            avatar.save("images/avatar.png")
            avatar = Image.open("images/avatar.png")
            if os.path.exists(f"Leveling/users/{ctx.author.id}/data.ini"):
                config.read(f"Leveling/users/{ctx.author.id}/data.ini")
                lvlprog = config.get("Level", "lvlprog")
                lvl = config.get("Level", "lvl")
                topprog = config.get("Level", "topprog")
                h,w = avatar.size
                avmask = Image.new('L', (h, w), 0)
                clear = Image.new('RGBA', (h, w), 1)
                draw = ImageDraw.Draw(avmask)
                draw.ellipse((0,0,256, 256), fill=255)
                masked = Image.composite(avatar, clear, mask=avmask)
                font = ImageFont.truetype("fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf", size=100, layout_engine=ImageFont.Layout.BASIC)
                fontbig = ImageFont.truetype("fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf", size=150, layout_engine=ImageFont.Layout.BASIC)
                img.paste(masked.resize((612, 612)), (49, 82), mask=masked.resize((612, 612)))
                I1 = ImageDraw.ImageDraw(img)
                I1.text((860, 120), str(ctx.author.name), fill=(255, 255, 255), font=fontbig)
                I1.text((2310, 120), f"#{ctx.author.discriminator}", fill=(200, 200, 200), font=fontbig)
                I1.text((900, 380), f"LVL: {n.numerize(int(lvl))}", fill=(255, 255, 255), font=font)
                x3, y3 = x1, y1
                x4, y4 = x1+((x2-x1)*(int(lvlprog)/int(topprog))), y2
                I1.text((2000,380), f"XP: {n.numerize(int(lvlprog))} / {n.numerize(int(topprog))}", fill=(255, 255, 255), font=font)
                bar = Image.new('RGBA', img.size, 1)
                I3 = ImageDraw.ImageDraw(bar)
                I3.ellipse((x1-((y2-y1)/2), y1, x1+((y2-y1)/2), y2), fill=(119, 0, 18))
                I3.ellipse((x2-((y2-y1)/2), y1, x2+((y2-y1)/2), y2), fill=(119, 0, 18))
                I3.rectangle((x1, y1, x2, y2), fill=(119, 0, 18))
                I3.rectangle((x3, y3, x4, y4), fill=(0, 119, 29))
                I3.ellipse((x1-((y2-y1)/2), y1, x1+((y2-y1)/2), y2), fill=(0, 119, 29))
                I3.ellipse((x4-((y2-y1)/2), y1, x4+((y2-y1)/2), y4), fill=(0, 119, 29))
                img.paste(bar, mask=bar)
                img.save("images/userlevel.png")
                file = discord.File(f"images/userlevel.png", filename="userlevel.png")
                embed = discord.Embed(color=cfc)
                embed.set_image(url=f"attachment://userlevel.png")
                await ctx.respond(embed=embed, file=file)
            else:
                embed = discord.Embed(title="Error 404!", description="This most probably means that you never sended a message(slash commands or messages before the introduction of leveling don't count) in this server.", color=errorc)
                await ctx.respond(embed=embed)
        else:
            await user.avatar.save("images/avatarorigin.png")
            avatarorigin = Image.open("images/avatarorigin.png")
            avatar = avatarorigin.resize((256, 256))
            avatar.save("images/avatar.png")
            avatar = Image.open("images/avatar.png")
            if os.path.exists(f"Leveling/users/{user.id}/data.ini"):
                config.read(f"Leveling/users/{user.id}/data.ini")
                lvlprog = config.get("Level", "lvlprog")
                lvl = config.get("Level", "lvl")
                topprog = config.get("Level", "topprog")
                h,w = avatar.size
                avmask = Image.new('L', (h, w), 0)
                clear = Image.new('RGBA', (h, w), 1)
                draw = ImageDraw.Draw(avmask)
                draw.ellipse((0,0,256, 256), fill=255)
                masked = Image.composite(avatar, clear, mask=avmask)
                font = ImageFont.truetype("fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf", size=100, layout_engine=ImageFont.Layout.BASIC)
                fontbig = ImageFont.truetype("fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf", size=150, layout_engine=ImageFont.Layout.BASIC)
                img.paste(masked.resize((612, 612)), (49, 82), mask=masked.resize((612, 612)))
                I1 = ImageDraw.ImageDraw(img)
                I1.text((860, 120), str(user.name), fill=(255, 255, 255), font=fontbig)
                I1.text((2310, 120), f"#{user.discriminator}", fill=(200, 200, 200), font=fontbig)
                I1.text((900, 380), f"LVL: {n.numerize(int(lvl))}", fill=(255, 255, 255), font=font)
                x3, y3 = x1, y1
                x4, y4 = x1+((x2-x1)*(int(lvlprog)/int(topprog))), y2
                I1.text((2000,380), f"XP: {n.numerize(int(lvlprog))} / {n.numerize(int(topprog))}", fill=(255, 255, 255), font=font)
                bar = Image.new('RGBA', img.size, 1)
                I3 = ImageDraw.ImageDraw(bar)
                I3.ellipse((x1-((y2-y1)/2), y1, x1+((y2-y1)/2), y2), fill=(119, 0, 18))
                I3.ellipse((x2-((y2-y1)/2), y1, x2+((y2-y1)/2), y2), fill=(119, 0, 18))
                I3.rectangle((x1, y1, x2, y2), fill=(119, 0, 18))
                I3.rectangle((x3, y3, x4, y4), fill=(0, 119, 29))
                I3.ellipse((x1-((y2-y1)/2), y1, x1+((y2-y1)/2), y2), fill=(0, 119, 29))
                I3.ellipse((x4-((y2-y1)/2), y1, x4+((y2-y1)/2), y4), fill=(0, 119, 29))
                img.paste(bar, mask=bar)
                img.save("images/userlevel.png")
                file = discord.File(f"images/userlevel.png", filename="userlevel.png")
                embed = discord.Embed(color=cfc)
                embed.set_image(url=f"attachment://userlevel.png")
                await ctx.respond(embed=embed, file=file)
            else:
                if user.bot == True:
                    embed = discord.Embed(title="Error 404!", description="I didn't found any data of leveling, because the provided user is a bot. They don't get to use this amazing leveling system!", color=errorc)
                    await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(title="Error 404!", description="This most probably means that you never sended a message(slash commands or messages before the introduction of leveling don't count) in this server.", color=errorc)
                    await ctx.respond(embed=embed)

    @leveling.command(name="leaderboard", description="See the leaderboard of the whole server.")
    async def lb(self, ctx):
        if os.path.exists(".onpc"):
            await ctx.defer()
            output = []
            nameoutput = []
            index = 1
            config = configparser.ConfigParser()
            img = Image.open(f"images/lbClear.png")
            for index, filename in enumerate(glob.glob('Leveling/users/*/*')):
                with open(os.path.join(os.getcwd(), filename), 'r') as f:
                    config.read(f"{filename}")
                    lvl = int(config.get("Level", "lvl"))
                    lvlprog = int(config.get("Level", "lvlprog"))
                    topprog = int(config.get("Level", "topprog"))
                    filen = filename.replace("Leveling/users/", f"")
                    id=os.path.dirname(filen)
                    user = self.bot.get_user(int(id))
                    line = f"""
          {lvlprog+topprog*lvl} LVL: {lvl} XP: {lvlprog}/{n.numerize(topprog)}\n
          """
                    output.append(line)
                    line2 = f"""
          {lvlprog+topprog*lvl} {user.name[:50]}\n
          """
                    nameoutput.append(line2)
            def atoi(text):
                return int(text) if text.isdigit() else text
            def natural_keys(text):
                return [ atoi(c) for c in re.split('(\d+)',text) ]
            output.sort(key=natural_keys, reverse=True)
            nameoutput.sort(key=natural_keys, reverse=True)
            def delstr(lst):
                return [
                    f"{' '.join(elem.split()[1:]).rstrip()}"
                    for elem in lst
                ]
                
            output = delstr(output)
            nameoutput = delstr(nameoutput)

            nameoutput = [f'{index}       {i}' for index, i in enumerate(nameoutput, 1)]
            output = [direction + '\n\n' for direction in output]
            nameoutput = [direction + '\n\n' for direction in nameoutput]
            embed = discord.Embed(title="ClearFly Level Leaderboard", description=f"""
Chat to earn xp!
            """, color=cfc)
            I1 = ImageDraw.Draw(img)
            font = ImageFont.truetype("fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf", size=44, layout_engine=ImageFont.Layout.BASIC)
            I1.text((800, 30), "".join(output[:10]), fill=(255, 255, 255), font=font)
            I1.text((27,30), "".join(nameoutput[:10]), fill=(255, 255, 255), font=font)
            img.save(f"images/lb.png")
            file = discord.File(f"images/lb.png", filename="lb.png")
            embed.set_image(url=f"attachment://lb.png")
            await ctx.respond(embed=embed, file=file)
        else:
            output = []
            index = 1
            config = configparser.ConfigParser()
            for index, filename in enumerate(glob.glob('Leveling/users/*/*')):
                with open(os.path.join(os.getcwd(), filename), 'r') as f:
                    config.read(f"{filename}")
                    lvl = int(config.get("Level", "lvl"))
                    lvlprog = int(config.get("Level", "lvlprog"))
                    topprog = int(config.get("Level", "topprog"))
                    filen = filename.replace("Leveling/users/", f"")
                    lbn = index+1
                    id=os.path.dirname(filen)
                    user = self.bot.get_user(int(id))
                    line = f"{lvlprog+topprog*lvl} | Level:{lvl} XP:{lvlprog}/{topprog} {user.name}\n"
                    output.append(line)
            def atoi(text):
                return int(text) if text.isdigit() else text
            def natural_keys(text):
                return [ atoi(c) for c in re.split('(\d+)',text) ]
            output.sort(key=natural_keys, reverse=True)
            def delstr(lst):
                return [
                f"{' '.join(elem.split()[1:]).rstrip()}"
                for elem in lst
            ]
                
            output = delstr(output)

            def movestr(lst):
                return [
                f"{' '.join(elem.split()[3:]).rstrip()} {' '.join(elem.split()[:3])}\n"
                for elem in lst
            ]
                
            output = movestr(output)

            foutput = [f'{index} | {i}' for index, i in enumerate(output, 1)]
            embed = discord.Embed(title="ClearFly Level Leaderboard", description=f"""
Chat more to go higher on the list!
```
{"".join(foutput[:10])}
```
            """, color=cfc)
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(LevelingCommands(bot))
