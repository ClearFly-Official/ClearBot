import discord
import pyfiglet
import random
import textwrap
import os
import flag
from dadjokes import Dadjoke
from discord import option
from discord.ext import commands
from pilmoji import Pilmoji
from wonderwords import RandomSentence
from PIL import Image, ImageDraw, ImageFont
from main import cfc, errorc


class FunCommands(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    fun = discord.SlashCommandGroup(name="fun",description="Fun commands.")

    @commands.Cog.listener()
    async def on_ready(self):
        print("| Fun cog loaded sucessfully")


    @fun.command(name="bigtext", description="📚 Convert text into text emoji characters.")
    @option("text", description="The text you want to convert.")
    async def bigtxtconv(self, ctx, text):
        
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
            embed = discord.Embed(title="Error 400!", description="The output of the converted text is more than 2000 characters, as Discord only allows a maximum of 2000 characters in a message I can't send it. Please try again with a shorter input.", color=errorc)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("".join(convtext))

    @fun.command(name="ascii",description="📑 Convert text into big characters using ASCII.")
    @option("text", description="The text you want to convert.")
    async def asciiconv(self, ctx, text):
        try:
            await ctx.respond(f"```{pyfiglet.figlet_format(text)}```")
        except Exception as error:
            await ctx.respond(f"""Error:
```
{error}
```
            """)

    @fun.command(name="8ball", description="🎱  Roll the eight ball and recieve the wisdom of chance!")
    @option("question", description="The question you want to ask the bot.")
    @option("mode", description="The mode of the answers. This will determine the answer type.", choices=["Normal", "Weird Mode"])
    async def VIIIball(self, ctx, question, mode= None):
        if (mode == None) or (mode == "Normal"):
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
            embed = discord.Embed(title=f'{question}:', description=f'{random.choice(answers)}', color=cfc)
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
            "I politely ask you to shut up."
            ]
            embed = discord.Embed(title=f'{question}:', description=f'{random.choice(answers)}', color=cfc)
            await ctx.respond(embed=embed)

    @fun.command(name="dadjoke", description="🃏 Get an unfunny dadjoke.")
    async def dadjoke(self, ctx):
        dadjoke = Dadjoke()
        embed = discord.Embed(title=f"{dadjoke.joke}", color=cfc)
        await ctx.respond(embed=embed)

    @fun.command(name="roast", description="🔥 Why roast your friends when the bot can do it for you?")
    @option("user", description="The person you'd like to roast.")
    async def roast(self, ctx, user: discord.Member):
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
            "You're so fat, when you wear a yellow rain coat people scream \"taxi\".",
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
    async def bgame(self, ctx):
        embed = discord.Embed(title="Choose a button!", color=cfc)
        class ButtonGame(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=20)

            async def on_timeout(self, interaction):
                interaction.response.edit_message("You ran out of time! Rerun the command to play again.")
                for child in self.children:
                    child.disabled = True
                
            global b, isPressed
            b = 0
            isPressed = 0

            @discord.ui.button(label="1", style=discord.ButtonStyle.green)
            async def first_button_callback(self, button, interaction):
                if interaction.user == ctx.author:
                    global b, isPressed
                    b = 1
                    isPressed = 1
                    opts = [1, 2, 1, 2, 3, 3, 1, 2]
                    output = random.choice(opts)
                    if output == b:
                        embed = discord.Embed(description=":partying_face: You guessed right. Congrats!", colour=cfc)
                        await interaction.response.edit_message(embed=embed)
                    elif isPressed == 1:
                        embed = discord.Embed(description=f":disappointed_relieved: You guessed wrong. The right answer was {output}", colour=cfc)
                        await interaction.response.edit_message(embed=embed)
                else:
                    await interaction.response.send_message("Run the command yourself to use it!", ephemeral=True)

            @discord.ui.button(label="2", style=discord.ButtonStyle.green)
            async def second_button_callback(self, button, interaction):
                if interaction.user == ctx.author:
                    global b, isPressed
                    b = 2
                    isPressed = 1
                    opts = [1, 2, 3, 1, 3, 3, 1, 2]
                    output = random.choice(opts)
                    if output == b:
                        embed = discord.Embed(description=":partying_face: You guessed right. Congrats!", colour=cfc)
                        await interaction.response.edit_message(embed=embed)
                    elif isPressed == 1:
                        embed = discord.Embed(description=f":disappointed_relieved: You guessed wrong. The right answer was {output}", colour=cfc)
                        await interaction.response.edit_message(embed=embed)
                else:
                    await interaction.response.send_message("Run the command yourself to use it!", ephemeral=True)

            @discord.ui.button(label="3", style=discord.ButtonStyle.green)
            async def third_button_callback(self, button, interaction):
                if interaction.user == ctx.author:
                    global b, isPressed
                    b = 3
                    isPressed = 1
                    opts = [1, 2, 3, 1, 2, 3, 1, 2]
                    output = random.choice(opts)
                    if output == b:
                        embed = discord.Embed(description=":partying_face: You guessed right. Congrats!", colour=cfc)
                        await interaction.response.edit_message(embed=embed)
                    elif isPressed == 1:
                        embed = discord.Embed(description=f":disappointed_relieved: You guessed wrong. The right answer was {output}", colour=cfc)
                        await interaction.response.edit_message(embed=embed)
                else:
                    await interaction.response.send_message("Run the command yourself to use it!", ephemeral=True)


        await ctx.respond(embed=embed, view=ButtonGame())

    @discord.message_command(name='📰 Quote Message')
    async def quote(self, ctx, message):
        await ctx.defer()
        await message.author.avatar.save("images/avataroriginq.png")
        avatarorigin = Image.open("images/avataroriginq.png")
        avatar = avatarorigin.resize((1024, 1024))
        avatar.save("images/avatarq.png")
        avatar = Image.open("images/avatarq.png")
        qclear = Image.open("images/quoteClear.png")
        qavmask = Image.open("images/quoteAVMask.png")
        img = Image.new('RGBA', (2048, 1024), 0)
        img.paste(avatar, qavmask)
        img.paste(qclear, mask=qclear)
        font = ImageFont.truetype("fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf", size=100, layout_engine=ImageFont.Layout.BASIC)
        draw = ImageDraw.ImageDraw(img)
        text = f"{textwrap.fill(message.clean_content, 22, max_lines=6)}"
        author = f"- {message.author.name}"
        draw.text((950, 100), text, font=font)
        draw.text((1000, 824), author, font=font, fill=(130, 130, 130))
        img.save("images/qoute.png")
        await ctx.respond(file=discord.File("images/qoute.png"))

    @fun.command(name="flag-game", description="🏳️ Guess a sentence where country codes get replace by flags(e.g. after -> 🇦🇫ter).")
    @option("difficulty", description="Difficulty level of the game(only affects sentences, not flags!)", choices=["Very Easy", "Easy", "Normal", "Hard"])
    async def flagsgame(self, ctx, difficulty):
        await ctx.defer()
        fileName = "flaggame"+str(random.randint(0,100))+".png"

        s = RandomSentence()
        if difficulty == "Very Easy":
            oldText = s.bare_bone_sentence()
        if difficulty == "Easy":
            oldText = s.simple_sentence()
        if difficulty == "Normal":
            oldText = s.bare_bone_with_adjective()
        if difficulty == "Hard":
            oldText = s.sentence()

        with open("countrycodes.txt", "r") as f:
            ccodes = f.readlines()

        newText = oldText

        for ccode in ccodes:
            newText = newText.replace(ccode.lower()[:2], flag.flag(ccode.upper()))

        newText = str(textwrap.fill(newText, 28, max_lines=2))

        with Image.new('RGBA', (2048, 512)) as image:
            font = ImageFont.truetype('fonts/HelveticaNeue/OpenType-TT/HelveticaNeue.ttf', 144)
            with Pilmoji(image) as pilmoji:
                pilmoji.text((10, 10), newText, (255, 255, 255), font, emoji_position_offset=(0, 10))
            image.save(fileName)

        file = discord.File(fileName, filename=fileName)
        embed = discord.Embed(title="Guess the sentence!", description=f"Hurry up, you only have **2 mins**!\n\n*Sentence generated with '{difficulty}' difficulty, reply ping with your answer*", color=cfc)
        embed.set_image(url=f"attachment://{fileName}")
        embed.set_footer(text="Difficulty level only affects sentences, not flags!")
        await ctx.respond(embed=embed,file=file)

        def check(m):
            return m.author == ctx.author and str(m.type) == "MessageType.reply" and self.bot.user in m.mentions
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=120.0)
            if msg.content.lower().replace(".", "") == oldText.lower().replace(".", ""):
                embed = discord.Embed(title="🎉 Congrats, you got it!", color=0x00FF00)
                await msg.reply(embed=embed)
            else:
                embed = discord.Embed(title="🥲 Sadness, you got it wrong...", description=f"The correct answer was: `{oldText}`", color=errorc)
                await msg.reply(embed=embed)
        except Exception:
            embed = discord.Embed(title="Error 408", description=f"You ran out of time! The answer was: `{oldText}`", colour=errorc)
            await ctx.respond(embed=embed)
        os.remove(fileName)

def setup(bot):
    bot.add_cog(FunCommands(bot))
