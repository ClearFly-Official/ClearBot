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
client = pymongo.MongoClient(os.environ['MONGODB_URI'])
db = client["ClearBotDB"]
rss = db['RSS']
trescol = rss['Tresholdx']
fsacol = rss['FSAddonsXP']
fsnews =  1066124540318588928 #CB test 1001401783689678868

class Listeners(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.presence.start()
        self.rssfeed1.start()
        self.rssfeed2.start()
        print("| All tasks and listeners have started successfully")

    @tasks.loop(minutes=10)
    async def presence(self):
            statements =[
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
            "Bored"
            ]
            await self.bot.change_presence(activity=discord.Game(name=f"/help | {random.choice(statements)}"),status=discord.Status.online)
        
    @tasks.loop(seconds=60)
    async def rssfeed1(self):
            channel = self.bot.get_channel(fsnews)
            blog_feed = feedparser.parse("https://www.thresholdx.net/news/rss.xml" )
            feed = dict(blog_feed.entries[0])
            lastID = trescol.find()
            ids = []
            for id in lastID:
                ids.append(id)
            if ids == []:
                ids = [{'lastID':None}]
            if ids[0]['lastID'] == feed.get('id'):
                return
            else:
                trescol.update_one({"_id": "lastID"},{
                    "$set":{
                        "lastID": feed.get('id')
                    }
                })
                await channel.send(f"""
    **{feed.get('title')}**

    {feed.get('link')}
                """)

    @tasks.loop(seconds=60)
    async def rssfeed2(self):
            channel = self.bot.get_channel(fsnews)
            blog_feed = feedparser.parse("https://fsaddons.online/category/x-plane/rss" )
            feed = dict(blog_feed.entries[0])
            lastID = fsacol.find()
            ids = []
            for id in lastID:
                ids.append(id)
            if ids == []:
                ids = [{'lastID':None}]
            if ids[0]['lastID'] == feed.get('id'):
                return
            else:
                fsacol.update_one({"_id": "lastID"},{
                    "$set":{
                        "lastID": feed.get('id')
                    }
                })
                await channel.send(f"""
    **{feed.get('title')}**

    {feed.get('link')}
                """)

    @commands.Cog.listener('on_message')
    async def levellisten(self, message):
        nowlvlprog = 0
        config = configparser.ConfigParser()
        if message.channel.id == 966077223260004402:
            return
        if message.channel.id == 965600413376200726:
            return
        if message.author.bot:
            return
        else:
            if os.path.exists(f"Leveling/users/{message.author.id}/data.ini"):
                config.read(f"Leveling/users/{message.author.id}/data.ini")
                belvlprog = config.get("Level", "lvlprog")
                last = config.get("Level", "last")
                now = round(time.time())
                if (now - int(last)) < 5:
                    print("it was spam...")
                    return
                else:
                    print("not spam!")
                    config.set("Level", "last", f"{now}")
                if len(message.content) == 0:
                    nowlvlprog = int(belvlprog)+1
                if len(message.content) > 0:
                    nowlvlprog = int(belvlprog)+1
                if len(message.content) > 10:
                    nowlvlprog = int(belvlprog)+2
                if len(message.content) > 25:
                    nowlvlprog = int(belvlprog)+5
                if len(message.content) > 50:
                    nowlvlprog = int(belvlprog)+7
                if len(message.content) > 75:
                    nowlvlprog = int(belvlprog)+10
                lvlprog = config.get("Level", "lvlprog")
                lvl = config.get("Level", "lvl")
                topprog = config.get("Level", "topprog")
                config.set("Level","lvlprog", f"{nowlvlprog}")
                if int(lvlprog) >= int(topprog):
                    config.set("Level","lvlprog", "0")
                    config.set("Level","lvl", f"{int(lvl)+1}")
                    if int(lvl) == 0:
                        lvl = 1
                    config.set("Level","topprog", f"{int(topprog)+(int(lvl)*20)}")
                    lvlp = config.get("Level", "lvl")
                    await message.channel.send(f"{message.author.mention} :partying_face: You reached level {lvlp}!")
                with open(f"Leveling/users/{message.author.id}/data.ini", "w") as configfile:
                    config.write(configfile)
            else:
                os.mkdir(f"Leveling/users/{message.author.id}")
                config.add_section("Level")
                config.set("Level","lvlprog", "1")
                config.set("Level","lvl", "0")
                config.set("Level","topprog", "25")
                config.set("Level","last", f"{round(time.time())}")
                with open(f"Leveling/users/{message.author.id}/data.ini", "w") as configfile:
                    config.write(configfile)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(965600413376200726)
        emb = discord.Embed(title=f"Welcome to ClearFly!", description=f"Hey there, {member.mention}! Be sure to read the <#1002194493304479784> to become a member and gain full access to the server! Thanks for joining!", color = cfc)
        await channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(1001405648828891187)
        emb = discord.Embed(title=f"{member} left.", color=cfc, description=f"Joined on {discord.utils.format_dt(member.joined_at)}")
        pfp = member.avatar.url
        emb.set_thumbnail(url=pfp)
        await channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot == False:
            channel = self.bot.get_channel(1001405648828891187)
            msgdel = message.clean_content
            msgatr = message.author.mention
            msgcnl = message.channel.mention
            pfp = message.author.avatar.url
            emb = discord.Embed(title="**Message Deleted:**", color=cfc)
            emb.add_field(name="Content:", value=f"{msgdel[:1024]}", inline = False)
            emb.add_field(name="Author:", value=f"{msgatr}", inline = True)
            emb.add_field(name="Channel:", value=f"{msgcnl}", inline = True)
            emb.set_thumbnail(url=pfp)
            await channel.send(embed=emb)
        else:
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot == False:
            channel = self.bot.get_channel(1001405648828891187)
            msgeditb = before.clean_content
            msgedita = after.clean_content
            msgatr = before.author.mention
            msgcnl = before.channel.mention
            pfp = before.author.avatar.url
            emb = discord.Embed(title="**Message Edited:**", color=cfc)
            emb.add_field(name="Content before:", value=f"{msgeditb[:1024]}", inline = False)
            emb.add_field(name="Content after:", value=f"{msgedita[:1024]}", inline = False)
            emb.add_field(name="Author:", value=f"{msgatr}", inline = True)
            emb.add_field(name="Channel:", value=f"{msgcnl}, [link](https://discord.com/channels/965419296937365514/{after.channel.id}/{before.id})", inline = True)
            emb.set_thumbnail(url=pfp)
            await channel.send(embed=emb)
        else:
            pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.bot == False:
            channel = self.bot.get_channel(1001405648828891187)
            if before.name != after.name:
                embed = discord.Embed(title=f"{before} changed their name to `{after.name}`.", colour=cfc)
                embed.set_thumbnail(url=after.avatar.url)
                await channel.send(embed=embed)
            if before.display_name != after.display_name:
                embed = discord.Embed(title=f"{before} changed their nickname to `{after.display_name}`.", colour=cfc)
                embed.set_thumbnail(url=after.avatar.url)
                await channel.send(embed=embed)
            if before.discriminator != after.discriminator:
                embed = discord.Embed(title=f"{before} changed their discriminator to `{after.discriminator}`.", colour=cfc)
                embed.set_thumbnail(url=after.avatar.url)
                await channel.send(embed=embed)
            if before.roles != after.roles:
                embed = discord.Embed(title=f"{before} got their roles changed.", colour=cfc)
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
                embed.set_thumbnail(url=after.avatar.url)
                await channel.send(embed=embed)
            if before.avatar != after.avatar:
                embed = discord.Embed(title=f"{before} changed their avatar to the following image.", colour=cfc)
                embed.set_image(url=after.avatar.url)
                await channel.send(embed=embed)
        else:
            pass


    @commands.Cog.listener('on_message')
    async def scamcheck(self, message):
        class BanView(discord.ui.View):
            def __init__(self, bot):
                self.bot = bot
                super().__init__(timeout=None)

            @discord.ui.button(label=f"Ban {message.author}", style=discord.ButtonStyle.danger)
            async def button_callback(self, button, interaction):
                try:
                    await message.author.ban(reason=f"{message.author} sent a scam, confirmed by {interaction.user}")
                    embed = discord.Embed(title=f"Successfully banned `{message.author}`", colour=0x00FF00)
                    await interaction.response.send_message(embed=embed)
                except Exception as error:
                    embed = discord.Embed(title=f"While trying to ban `{message.author}`, I got the following error:", description=f"\n```{error}\n```", colour=errorc)
                    await interaction.response.send_message(embed=embed)
        def scamChecker(string):
            change = 0
            blacklist = ["porn", "@everyone", "@here"]
            comboBL = ["free", "http", "crypto"]
            for i in blacklist:
                if blacklist[change] in string:
                    return True
                change +=1
            if ((comboBL[0]in string) or (comboBL[2]in string)) and (comboBL[1]in string):
                return True
            else:
                return False
        if message.author.id not in adminids:
            if scamChecker(message.content):
                await message.reply(content="Your message included blacklisted words, and has been deleted.")
                channel = self.bot.get_channel(1001405648828891187)
                embed = discord.Embed(title=f"`{message.author}` might have sent a scam", description=message.content, colour=errorc)
                await message.delete(reason=f"{message.author} might have sent a scam.")
                await channel.send(embed=embed, view=BanView(bot=self.bot))
            else:
                pass
        else:
            pass

def setup(bot):
    bot.add_cog(Listeners(bot=bot))