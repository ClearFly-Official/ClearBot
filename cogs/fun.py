import asyncio
import io
from typing import Literal
import discord
from discord.ui.item import Item
import pyfiglet
import random
import textwrap
import flag
import time
from dadjokes import Dadjoke
from discord import option
from discord.ext import commands
from pilmoji import Pilmoji
from wonderwords import RandomSentence
from PIL import Image, ImageDraw, ImageFont
from main import ClearBot


class ButtonGameView(discord.ui.View):
    def __init__(
        self,
        ctx: discord.ApplicationContext,
        bot: ClearBot,
        embed: discord.Embed,
    ):
        self.ctx = ctx
        self.bot = bot
        self.embed = embed

        self.button = random.randint(1, 3)

        super().__init__(timeout=60, disable_on_timeout=True)

    @discord.ui.button(label="1")
    async def b1_callback(
        self, button: discord.Button, interaction: discord.Interaction
    ):
        if not self.bot.is_interaction_owner(interaction, self.ctx.author.id):
            await interaction.response.send_message(
                "Run the command yourself to play the game!", ephemeral=True
            )

        embed = self.embed

        if str(self.button) == button.label:
            embed.title = "🥳 Correct button!"
            await interaction.response.edit_message(embed=embed, view=None)
            await asyncio.sleep(3)
            self.button = random.randint(1, 3)
            embed.title = "Guess the correct button!"
            await self.ctx.edit(embed=embed, view=self)
        else:
            embed.title = f"😢 Incorrect button..."
            await interaction.response.edit_message(embed=embed, view=None)
            await asyncio.sleep(3)
            self.button = random.randint(1, 3)
            embed.title = "Guess the correct button!"
            await self.ctx.edit(embed=embed, view=self)

    @discord.ui.button(label="2")
    async def b2_callback(
        self, button: discord.Button, interaction: discord.Interaction
    ):
        if not self.bot.is_interaction_owner(interaction, self.ctx.author.id):
            await interaction.response.send_message(
                "Run the command yourself to play the game!", ephemeral=True
            )

        embed = self.embed

        if str(self.button) == button.label:
            embed.title = "🥳 Correct button!"
            await interaction.response.edit_message(embed=embed, view=None)
            await asyncio.sleep(3)
            self.button = random.randint(1, 3)
            embed.title = "Guess the correct button!"
            await self.ctx.edit(embed=embed, view=self)
        else:
            embed.title = f"😢 Incorrect button..."
            await interaction.response.edit_message(embed=embed, view=None)
            await asyncio.sleep(3)
            self.button = random.randint(1, 3)
            embed.title = "Guess the correct button!"
            await self.ctx.edit(embed=embed, view=self)

    @discord.ui.button(label="3")
    async def b3_callback(
        self, button: discord.Button, interaction: discord.Interaction
    ):
        if not self.bot.is_interaction_owner(interaction, self.ctx.author.id):
            await interaction.response.send_message(
                "Run the command yourself to play the game!", ephemeral=True
            )

        embed = self.embed

        if str(self.button) == button.label:
            embed.title = "🥳 Correct button!"
            await interaction.response.edit_message(embed=embed, view=None)
            await asyncio.sleep(3)
            self.button = random.randint(1, 3)
            embed.title = "Guess the correct button!"
            await self.ctx.edit(embed=embed, view=self)
        else:
            embed.title = f"😢 Incorrect button..."
            await interaction.response.edit_message(embed=embed, view=None)
            await asyncio.sleep(3)
            self.button = random.randint(1, 3)
            embed.title = "Guess the correct button!"
            await self.ctx.edit(embed=embed, view=self)


class FunCommands(discord.Cog):
    def __init__(self, bot: ClearBot):
        self.bot = bot

    fun = discord.SlashCommandGroup(
        name="fun",
        description="🧩 Commands that are supposed to be fun (highly subjective).",
    )

    @commands.Cog.listener()
    async def on_ready(self):
        print("\033[34m|\033[0m \033[96;1mFun\033[0;36m cog loaded sucessfully\033[0m")

    @fun.command(
        name="bigtext",
        description="📚 Convert text into text emoji characters (might not work on mobile).",
    )
    @option("text", description="The text you want to convert.")
    async def bigtxtconv(self, ctx: discord.ApplicationContext, text: str):
        chars = "abcdefghijklmnopqrstuvwxyz"
        convtext = []

        for c in list(text.lower()):
            if c in list(chars):
                c = c.replace(c, f":regional_indicator_{c}:")
            if c == "0":
                c = c.replace(c, ":zero:")
            if c == "1":
                c = c.replace(c, ":one:")
            if c == "2":
                c = c.replace(c, ":two:")
            if c == "3":
                c = c.replace(c, ":three:")
            if c == "4":
                c = c.replace(c, ":four:")
            if c == "5":
                c = c.replace(c, ":five:")
            if c == "6":
                c = c.replace(c, ":six:")
            if c == "7":
                c = c.replace(c, ":seven:")
            if c == "8":
                c = c.replace(c, ":eight:")
            if c == "9":
                c = c.replace(c, ":nine:")
            convtext.append(c)
        if len("".join(convtext)) >= 2000:
            embed = discord.Embed(
                title="Too long output",
                description="The output of the converted text is more than 2000 characters, as Discord only allows a maximum of 2000 characters in a message I can't send it. Please try again with a shorter input.",
                color=self.bot.color(1),
            )
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("".join(convtext))

    @fun.command(
        name="ascii", description="📑 Convert text into big characters using ASCII."
    )
    @option("text", description="The text you want to convert.")
    async def asciiconv(self, ctx: discord.ApplicationContext, text: str):
        await ctx.respond(f"```{pyfiglet.figlet_format(text)}```")

    @fun.command(
        name="8ball",
        description="🎱  Roll the eight ball and recieve the wisdom of chance!",
    )
    @option("question", description="The question you want to ask the bot.")
    @option(
        "mode",
        description="The mode of the answers. This will determine the answer type.",
        choices=["Normal", "Weird"],
    )
    async def VIIIball(
        self, ctx: discord.ApplicationContext, question: str, mode: str = "Normal"
    ):
        if mode == "Normal":
            answers = [
                "It is certain",
                "Reply hazy, try again",
                "Don't count on it",
                "It is decidedly so",
                "Ask again later",
                "My reply is no",
                "Without a doubt",
                "Better not tell you now",
                "My sources say no",
                "Yes definitely",
                "Cannot predict now",
                "Outlook not so good",
                "You may rely on it",
                "Concentrate and ask again",
                "Very doubtful",
                "As I see it, yes",
                "Most likely",
                "Outlook good",
                "Yes",
                "Signs point to yes",
            ]
            embed = discord.Embed(
                title=f"{question}",
                description=f"{random.choice(answers)}",
                color=self.bot.color(),
            )
            await ctx.respond(embed=embed)
        else:
            answers = [
                "No.",
                "Yes.",
                "Maybe.",
                "Never.",
                "Ok",
                "Uhm ok...",
                "For legal purposes, I can't respond to that question",
                "No thank you.",
                "You're joking right?",
                "I don't think so...",
                "Ask Google, don't bother me.|| Not Bing, I dare you.||",
                "Go to sleep, you're tired.",
                "I'm not qualified to give medical advice, sorry.",
                "Ask again later.",
                "What?",
                "Haha, no.",
                "I'd go with yes",
                "Sure",
                "Yeah",
                "I'm concerned.",
                "Really good question to be honest, I still have no clue.",
                "WolfAir probably knows.",
                "A bit suspicious<:susge:965624336956407838>.",
                "Eh, probably not.",
                "Respectfully, shut up.",
                "I politely ask you to shut up.",
            ]
            embed = discord.Embed(
                title=f"{question}",
                description=f"{random.choice(answers)}",
                color=self.bot.color(),
            )
            await ctx.respond(embed=embed)

    @fun.command(name="dadjoke", description="🃏 Get an unfunny dadjoke.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dadjoke(self, ctx: discord.ApplicationContext):
        dadjoke = Dadjoke()
        embed = discord.Embed(title=f"{dadjoke.joke}", color=self.bot.color())
        await ctx.respond(embed=embed)

    @fun.command(
        name="roast",
        description="🔥 Why roast your friends when the bot can do it for you?",
    )
    @option("user", description="The person you'd like to roast.")
    async def roast(self, ctx: discord.ApplicationContext, user: discord.Member):
        roasts = [
            "Your face made the onion cry.",
            "I'm jealous of people who don't know you.",
            "If I had a face like yours, I'd sue my parents.",
            "You sound reasonable… time to up my medication.",
            "I might be crazy, but crazy is better than stupid.",
            "My middle finger gets a boner every time I see you.",
            "If your brain was made of chocolate, it wouldn't fill an M&M.",
            "You're not funny, but your life; now that's a joke.",
            "If laughter is the best medicine, your face must be curing the world.",
            "If you are going to be two faced, at least make one of them pretty.",
            "You're as bright as a black hole, and twice as dense.",
            "I may love to shop but I'm not buying your bullshit.",
            "I'm not saying I hate you, but I would unplug your life support to charge my phone.",
            "You shouldn't play hide and seek, no one would look for you.",
            'You\'re so fat, when you wear a yellow rain coat people scream "taxi".',
            "If I gave you a penny for your thoughts, I'd get change.",
            "If you really want to know about mistakes, you should ask your parents.",
            "Don't feel sad, don't feel blue, Frankenstein was ugly too.",
            "There's only one problem with your face, I can see it.",
            "There are more calories in your stomach than in the local supermarket!",
            "You're so ugly, the only dates you get are on a calendar",
            "I heard your parents took you to a dog show and you won.",
            "Why don't you check eBay and see if they have a life for sale.",
            "Why don't you slip into something more comfortable -- like a coma.",
            "Is there an app I can download to make you disappear?",
            "Keep rolling your eyes. Maybe you'll find your brain back there.",
            "I suggest you do a little soul searching. You might just find one.",
            "Maybe you should eat make-up so you'll be pretty on the inside too.",
            "I keep thinking you can't get any dumber and you keep proving me wrong.",
            "Why is it acceptable for you to be an idiot but not for me to point it out?",
            "Everyone brings happiness to a room. I do when I enter, you do when you leave.",
            "I thought I had the flu, but then I realized your face makes me sick to my stomach.",
            "When karma comes back to punch you in the face, I want to be there in case it needs help.",
            "I'm not an astronomer but I am pretty sure the earth revolves around the sun and not you.",
            "If you're going to be a smart ass, first you have to be smart, otherwise you're just an ass.",
            "Do yourself a favor and ignore anyone who tells you to be yourself. Bad idea in your case.",
            "Your crazy is showing. You might want to tuck it back in.",
        ]
        output = random.choice(roasts)
        if user.id == 1001249135774666823:
            await ctx.respond("Why do you want to roast me :sob:")
        else:
            await ctx.respond(f"{user.mention} {output}")

    @fun.command(name="button-game", description="🔘 Play a game with buttons!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bgame(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title="Choose a button!", color=self.bot.color())

        await ctx.respond(embed=embed, view=ButtonGameView(ctx, self.bot, embed))

    @discord.message_command(name="Quote Message")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def quote(self, ctx: discord.ApplicationContext, message: discord.Message):
        await ctx.defer()
        data = await message.author.display_avatar.read()
        avatarorigin = Image.open(io.BytesIO(data))
        avatar = avatarorigin.resize((1024, 1024))
        qclear = Image.open("images/quote/quote.png")
        qavmask = Image.open("images/quote/AVMask.png")
        img = Image.new("RGBA", (2048, 1024), 0)
        img.paste(avatar, qavmask)  # type: ignore
        img.paste(qclear, mask=qclear)
        font = ImageFont.truetype(
            "fonts/Inter-Regular.ttf",
            size=100,
            layout_engine=ImageFont.Layout.BASIC,
        )
        text = f"{textwrap.fill(message.clean_content, 22, max_lines=6)}"
        author = f"- {message.author.name}"
        with Pilmoji(img) as pilmoji:
            pilmoji.text((950, 100), text, font=font, emoji_position_offset=(0, 20))
            pilmoji.text(
                (1000, 824),
                author,
                font=font,
                fill=(130, 130, 130),
                emoji_position_offset=(0, 20),
            )

        with io.BytesIO() as output:
            img.save(output, format="PNG")
            output.seek(0)
            await ctx.respond(
                file=discord.File(output, filename=f"qoute{message.id}.png")
            )

    @fun.command(
        name="flag-game",
        description="🏳️ Guess a sentence where country codes get replace by flags(e.g. after -> 🇦🇫ter).",
    )
    @option(
        "difficulty",
        description="Difficulty level of the game",
        choices=["Very Easy", "Easy", "Normal", "Hard", "Very Hard"],
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def flagsgame(self, ctx: discord.ApplicationContext, difficulty: str):
        await ctx.defer()
        fileName = "flaggame" + str(random.randint(0, 100)) + ".png"

        s = RandomSentence()

        match difficulty:
            case "Very Easy":
                oldText = s.simple_sentence()
            case "Easy":
                oldText = s.simple_sentence()
            case "Normal":
                oldText = s.bare_bone_with_adjective()
            case "Hard":
                oldText = s.sentence()
            case "Very Hard":
                oldText = s.sentence()
            case _:
                oldText = s.simple_sentence()

        def flag_gen(
            text: str,
            difficulty: str,
        ) -> str:
            match difficulty:
                case "Very Easy":
                    diff = "countrycodes_veasy.txt"
                case "Easy":
                    diff = "countrycodes_easy.txt"
                case "Normal":
                    diff = "countrycodes_normal.txt"
                case "Hard":
                    diff = "countrycodes_hard.txt"
                case "Very Hard":
                    diff = "countrycodes_vhard.txt"
                case _:
                    diff = "countrycodes_veasy.txt"

            with open(f"ccodes/{diff}", "r") as f:
                ccodes = f.readlines()

            conv_text = text

            for ccode in ccodes:
                conv_text = conv_text.replace(
                    ccode.lower()[:2], flag.flag(ccode.upper())
                )

            if conv_text == text:
                try:
                    return flag_gen(text, difficulty)
                except:
                    return "S🇴🇲🇪🇹h🇮🇳g went w🇷🇴🇳🇬..."
            else:
                return conv_text

        newText = flag_gen(oldText, difficulty)
        newText = textwrap.fill(newText, 28, max_lines=2)

        with Image.new("RGBA", (2048, 512)) as image:
            font = ImageFont.truetype("fonts/Inter-Regular.ttf", 144)
            with Pilmoji(image) as pilmoji:
                pilmoji.text(
                    (10, 10),
                    newText,
                    (255, 255, 255),
                    font,
                    emoji_position_offset=(0, 20),
                )
            with io.BytesIO() as output:
                image.save(output, format="PNG")
                output.seek(0)
                file = discord.File(output, filename=fileName)

        embed = discord.Embed(
            title="Guess the sentence!",
            description=f"Hurry up, game ends <t:{round(time.time())+120}:R>!\n\nDifficulty: **{difficulty}**\n*Reply ping with your answer!*",
            color=self.bot.color(),
        )
        embed.set_image(url=f"attachment://{fileName}")
        await ctx.respond(embed=embed, file=file)

        def check(m):
            return (
                m.author == ctx.author
                and str(m.type) == "MessageType.reply"
                and self.bot.user in m.mentions
            )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=120.0)
            if msg.content.lower().replace(".", "") == oldText.lower().replace(".", ""):
                embed = discord.Embed(title="🎉 Congrats, you got it!", color=0x00FF00)
                await msg.reply(embed=embed)
                embed = discord.Embed(
                    title="Guess the sentence!",
                    description=f"**Game finished, {ctx.author.mention} won!**\n\nDifficulty: **{difficulty}**",
                    color=self.bot.color(),
                )
                embed.set_image(url=f"attachment://{fileName}")
                await ctx.edit(embed=embed)
            else:
                embed = discord.Embed(
                    title="🥲 Sad, you got it wrong...",
                    description=f"The correct answer was: `{oldText}`",
                    color=self.bot.color(1),
                )
                await msg.reply(embed=embed)
                embed = discord.Embed(
                    title="Guess the sentence!",
                    description=f"**Game finished, {ctx.author.mention} lost...**\n\nDifficulty: **{difficulty}**",
                    color=self.bot.color(),
                )
                embed.set_image(url=f"attachment://{fileName}")
                await ctx.edit(embed=embed)
        except Exception:
            embed = discord.Embed(
                title="Guess the sentence!",
                description=f"**Game finished, {ctx.author.mention} ran out of time...**\n\nDifficulty: **{difficulty}**",
                color=self.bot.color(),
            )
            embed.set_image(url=f"attachment://{fileName}")
            await ctx.edit(embed=embed)
            embed = discord.Embed(
                title="Timeout",
                description=f"You ran out of time! The answer was: `{oldText}`",
                colour=self.bot.color(1),
            )
            await ctx.respond(embed=embed)

    ####################################################################################
    #              **Disabled due to Reddit API changes. (fuck u/spez!)**             #
    ####################################################################################
    #
    # @fun.command(name="meme", description="🤣 Get a fresh meme from r/aviationmemes.")
    # @option(
    #     "limit",
    #     description="How back far in time the bot should look for memes(in posts).",
    #     required=False,
    # )
    # @commands.cooldown(1, 15)
    # async def avmeme(self, ctx: discord.ApplicationContext, limit: int):
    #     await ctx.defer()
    #     if limit == None:
    #         limit = 24
    #     if limit > 128:
    #         embed = discord.Embed(
    #             title="`limit` too large",
    #             description="You gave too big of a number for the `limit` option!",
    #             colour=self.bot.color(1),
    #         )
    #         await ctx.respond(embed=embed)
    #     else:
    #         subms = []
    #         subreddit = await reddit.subreddit("aviationmemes")
    #         async for subm in subreddit.new(limit=limit):
    #             if subm.id in self.bot.rshownsubms:
    #                 continue
    #             if subm.url.endswith((".jpg", ".png", ".gif")):
    #                 subms.append(subm)
    #         if subms == []:
    #             embed = discord.Embed(
    #                 title="Error 404!",
    #                 description="I did not find any valid posts, try again later.",
    #                 colour=self.bot.color(1),
    #             )
    #             await ctx.respond(embed=embed)
    #         else:
    #             random.seed(time.time())
    #             subm = random.choice(subms)
    #             self.bot.rshownsubms.append(subm.id)
    #             embed = discord.Embed(
    #                 title=subm.title[:256],
    #                 url="https://reddit.com" + subm.permalink,
    #                 description=f"<t:{round(int(subm.created_utc))}:R>",
    #                 colour=self.bot.color(),
    #             )
    #             embed.set_author(
    #                 name=f"r/aviatonmemes | by {subm.author}",
    #                 url="https://reddit.com" + subm.permalink,
    #                 icon_url="https://styles.redditmedia.com/t5_2wzek/styles/communityIcon_jj75v4o3fok81.jpg?width=256&format=pjpg&v=enabled&s=0eb5711d62d7818f07b590a84dce0e3a36b44fac",
    #             )
    #             embed.set_footer(
    #                 text=f"Votes: {subm.score} | Ratio: {subm.upvote_ratio} | Comments: {subm.num_comments} | OC: {subm.is_original_content}"
    #             )
    #             embed.set_image(url=subm.url)
    #             await ctx.respond(embed=embed)

    @fun.command(name="create_meme", description="🌄 Create your own meme!")
    @option("image", description="The image you want to 'memify'.")
    @option("top_text", description="The text at the top of your meme.", required=False)
    @option(
        "bottom_text",
        description="The text at the bottom of your meme.",
        required=False,
    )
    @option("text_size", description="The size of text.", required=False)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def meme(
        self,
        ctx: discord.ApplicationContext,
        image: discord.Attachment,
        top_text: str,
        bottom_text: str,
        text_size: int,
        bars: bool = False,
    ):
        await ctx.defer()
        if not top_text and not bottom_text:
            embed = discord.Embed(
                title="You didn't provide any text!",
                description="Try again, and this time give me some text.",
                colour=self.bot.color(1),
            )
            await ctx.respond(embed=embed)
            return

        if not str(image.content_type).startswith("image/"):
            embed = discord.Embed(
                title="You didn't provide a valid image!",
                description="Try again, and this time give me a valid image.",
                colour=self.bot.color(1),
            )
            await ctx.respond(embed=embed)
            return

        meme_id_n = random.randint(10, 99)
        meme_id = f"meme{meme_id_n}.png"
        img_data = await image.read()
        img = Image.open(io.BytesIO(img_data))
        resolution = img.size
        if len(img_data) >= 6000000:
            embed = discord.Embed(
                title="You provided too big of an image!",
                description="Try again, and this time give me a smaller image (<8MB).",
                colour=self.bot.color(1),
            )
            await ctx.respond(embed=embed)
            return
        if text_size is None:
            text_size = round(resolution[0] * 0.06)
        font = ImageFont.truetype("fonts/Impact.ttf", size=text_size)
        font_bars = ImageFont.truetype("fonts/Arial Bold.ttf", size=text_size)
        border_offset = round(text_size / 25)
        if top_text != None:
            with Pilmoji(img) as pilmoji:
                if bars:
                    draw = ImageDraw.ImageDraw(img)
                    draw.rectangle(
                        ((0, 0), (resolution[0], round(resolution[1] / 6))),
                        fill=(255, 255, 255),
                    )
                    pilmoji.text(
                        (
                            round(resolution[0] / 2)
                            - (round(font_bars.getlength(top_text) / 2)),
                            round(resolution[1] / 47),
                        ),
                        textwrap.fill(top_text, 25, max_lines=2),
                        font=font_bars,
                        fill=(0, 0, 0),
                        emoji_position_offset=(0, 20),
                        align="center",
                    )
                else:
                    pilmoji.text(
                        (
                            round(resolution[0] / 2)
                            + border_offset
                            - round(font.getlength(top_text.upper()) / 2),
                            round(resolution[1] / 40) + border_offset,
                        ),
                        textwrap.fill(top_text.upper(), 25, max_lines=2),
                        font=font,
                        emoji_position_offset=(0 - border_offset, 20 - border_offset),
                        fill=(0, 0, 0),
                        align="center",
                    )
                    pilmoji.text(
                        (
                            round(resolution[0] / 2)
                            - border_offset
                            - round(font.getlength(top_text.upper()) / 2),
                            round(resolution[1] / 40) - border_offset,
                        ),
                        textwrap.fill(top_text.upper(), 25, max_lines=2),
                        font=font,
                        emoji_position_offset=(border_offset, 20 + border_offset),
                        fill=(0, 0, 0),
                        align="center",
                    )
                    pilmoji.text(
                        (
                            round(resolution[0] / 2)
                            + border_offset
                            - round(font.getlength(top_text.upper()) / 2),
                            round(resolution[1] / 40) - border_offset,
                        ),
                        textwrap.fill(top_text.upper(), 25, max_lines=2),
                        font=font,
                        emoji_position_offset=(0 - border_offset, 20 + border_offset),
                        fill=(0, 0, 0),
                        align="center",
                    )
                    pilmoji.text(
                        (
                            round(resolution[0] / 2)
                            - border_offset
                            - round(font.getlength(top_text.upper()) / 2),
                            round(resolution[1] / 40) + border_offset,
                        ),
                        textwrap.fill(top_text.upper(), 25, max_lines=2),
                        font=font,
                        emoji_position_offset=(border_offset, 20 - border_offset),
                        fill=(0, 0, 0),
                        align="center",
                    )
                    pilmoji.text(
                        (
                            round(resolution[0] / 2)
                            - round(font.getlength(top_text.upper()) / 2),
                            round(resolution[1] / 40),
                        ),
                        textwrap.fill(top_text.upper(), 25, max_lines=2),
                        font=font,
                        emoji_position_offset=(0, 20),
                        align="center",
                    )
        if bottom_text != None:
            with Pilmoji(img) as pilmoji:
                if bars:
                    draw = ImageDraw.ImageDraw(img)
                    draw.rectangle(
                        (
                            (0, round(resolution[1] - resolution[1] / 6)),
                            (resolution[0], resolution[1]),
                        ),
                        fill=(255, 255, 255),
                    )
                    pilmoji.text(
                        (
                            round(resolution[0] / 2)
                            - round(font_bars.getlength(bottom_text) / 2),
                            round(resolution[1] - resolution[1] / 7),
                        ),
                        textwrap.fill(bottom_text, 25, max_lines=2),
                        font=font_bars,
                        fill=(0, 0, 0),
                        emoji_position_offset=(0, 20),
                        align="center",
                    )
                else:
                    pilmoji.text(
                        (
                            round(resolution[0] / 2)
                            + border_offset
                            - round(font.getlength(bottom_text.upper()) / 2),
                            round(resolution[1] - resolution[1] / 5) + border_offset,
                        ),
                        textwrap.fill(bottom_text.upper(), 25, max_lines=2),
                        font=font,
                        emoji_position_offset=(0 - border_offset, 20 - border_offset),
                        fill=(0, 0, 0),
                        align="center",
                    )
                    pilmoji.text(
                        (
                            round(resolution[0] / 2)
                            - border_offset
                            - round(font.getlength(bottom_text.upper()) / 2),
                            round(resolution[1] - resolution[1] / 5) - border_offset,
                        ),
                        textwrap.fill(bottom_text.upper(), 30, max_lines=3),
                        font=font,
                        emoji_position_offset=(border_offset, 20 + border_offset),
                        fill=(0, 0, 0),
                        align="center",
                    )
                    pilmoji.text(
                        (
                            round(resolution[0] / 2)
                            + border_offset
                            - round(font.getlength(bottom_text.upper()) / 2),
                            round(resolution[1] - resolution[1] / 5) - border_offset,
                        ),
                        textwrap.fill(bottom_text.upper(), 25, max_lines=2),
                        font=font,
                        emoji_position_offset=(0 - border_offset, 20 + border_offset),
                        fill=(0, 0, 0),
                        align="center",
                    )
                    pilmoji.text(
                        (
                            round(resolution[0] / 2)
                            - border_offset
                            - round(font.getlength(bottom_text.upper()) / 2),
                            round(resolution[1] - resolution[1] / 5) + border_offset,
                        ),
                        textwrap.fill(bottom_text.upper(), 25, max_lines=2),
                        font=font,
                        emoji_position_offset=(border_offset, 20 - border_offset),
                        fill=(0, 0, 0),
                        align="center",
                    )
                    pilmoji.text(
                        (
                            round(resolution[0] / 2)
                            - round(font.getlength(bottom_text.upper()) / 2),
                            round(resolution[1] - resolution[1] / 5),
                        ),
                        textwrap.fill(bottom_text.upper(), 25, max_lines=2),
                        font=font,
                        emoji_position_offset=(0, 20),
                        align="center",
                    )
        with io.BytesIO() as output:
            img.save(output, format="PNG")
            output.seek(0)
            file = discord.File(output, filename=meme_id)

        embed = (
            discord.Embed(
                title="Here's your meme!",
                colour=self.bot.color(),
                description=f"**Text Size**: {text_size}",
            )
            .set_image(url=f"attachment://{meme_id}")
            .set_author(
                name=f"Made by {ctx.author.name}", icon_url=ctx.author.display_avatar
            )
        )
        await ctx.respond(file=file, embed=embed)


def setup(bot):
    bot.add_cog(FunCommands(bot))
