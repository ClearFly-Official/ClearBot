import discord
from discord import option
from discord.ext import commands
from main import cfc, errorc
from datetime import datetime


class RulesView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(
        label="I have read and accept the rules",
        custom_id="rulebutton",
        style=discord.ButtonStyle.secondary,
        emoji="<:ClearFly:1054526148576559184>",
    )
    async def button_callback(self, button, interaction):
        guilds = self.bot.get_guild(965419296937365514)
        roles = guilds.get_role(1002200398905483285)
        if roles in interaction.user.roles:
            await interaction.response.send_message(
                "You already accepted the rules!", ephemeral=True
            )
        else:
            author = interaction.user
            guild = self.bot.get_guild(965419296937365514)
            role = guild.get_role(1002200398905483285)
            await author.add_roles(role)
            await interaction.response.send_message(
                "Rules accepted, have fun in the server!", ephemeral=True
            )


class FAQView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(
        label="I have read the FAQ",
        custom_id="faqbutton",
        style=discord.ButtonStyle.secondary,
        emoji="<:ClearFly:1054526148576559184>",
    )
    async def button_callback(self, button, interaction):
        author = interaction.user
        guild = self.bot.get_guild(965419296937365514)
        role = guild.get_role(1002932992534134814)
        await author.add_roles(role)
        await interaction.response.send_message(
            "Thanks for reading the FAQ!", ephemeral=True
        )


class AnnounceRoleView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(
        custom_id="announcebutton", style=discord.ButtonStyle.secondary, emoji="📣"
    )
    async def button_callback(self, button, interaction):
        author = interaction.user
        guild = self.bot.get_guild(965419296937365514)
        role = guild.get_role(965689409364197467)
        if role in author.roles:
            author = interaction.user
            guild = self.bot.get_guild(965419296937365514)
            role = guild.get_role(965689409364197467)
            await author.remove_roles(role)
            await interaction.response.send_message(
                "You won't get mentioned anymore for announcements.", ephemeral=True
            )
        else:
            author = interaction.user
            guild = self.bot.get_guild(965419296937365514)
            role = guild.get_role(965689409364197467)
            await author.add_roles(role)
            await interaction.response.send_message(
                "You will now get mentioned for announcments!", ephemeral=True
            )


class UpdateRoleView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(
        custom_id="updatebutton", style=discord.ButtonStyle.secondary, emoji="🛠"
    )
    async def button_callback(self, button, interaction):
        author = interaction.user
        guild = self.bot.get_guild(965419296937365514)
        role = guild.get_role(965688527109107712)
        if role in author.roles:
            author = interaction.user
            guild = self.bot.get_guild(965419296937365514)
            role = guild.get_role(965688527109107712)
            await author.remove_roles(role)
            await interaction.response.send_message(
                "You won't get mentioned for updates anymore.", ephemeral=True
            )
        else:
            author = interaction.user
            guild = self.bot.get_guild(965419296937365514)
            role = guild.get_role(965688527109107712)
            await author.add_roles(role)
            await interaction.response.send_message(
                "You will now get mentioned for updates!", ephemeral=True
            )


class AdminCommands(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(RulesView(bot=self.bot))
        self.bot.add_view(FAQView(bot=self.bot))
        self.bot.add_view(AnnounceRoleView(bot=self.bot))
        self.bot.add_view(UpdateRoleView(bot=self.bot))
        print("| Admin cog loaded sucessfully")

    admin = discord.SlashCommandGroup(name="admin", description="🔒 Commands for admins only.")

    @admin.command(name="echo", description="💬 Send a message as ClearBot.")
    @option("text", description="The text you want to send as the bot.")
    @commands.has_permissions(manage_messages=True)
    async def echo(self, ctx: discord.ApplicationContext, text: str):
        await ctx.respond("posted your message!", ephemeral=True)
        await ctx.channel.send(text)
        channel = self.bot.get_channel(1001405648828891187)
        emb = discord.Embed(
            title=f"{ctx.author} used echo:", description=text, color=cfc
        )
        emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await channel.send(embed=emb)

    @admin.command(name="embed", description="📦 Send an embed as ClearBot.")
    @option("title", description="The title of the embed.")
    @option(
        "url",
        description="The url of the embed, will show up as hyperlink in the title.",
        required=False,
    )
    @option("description", description="The description of the embed.", required=False)
    @option(
        "footer_text", description="The footer's text of the embed.", required=False
    )
    @option(
        "footer_icon_url",
        description="The footer's icon url of the embed.",
        required=False,
    )
    @option(
        "author_text", description="The author's text of the embed.", required=False
    )
    @option(
        "author_icon_url",
        description="The author's icon url of the embed.",
        required=False,
    )
    @option(
        "author_url",
        description="The url of the author, will show up as hyperlink in the author's text.",
        required=False,
    )
    @option("image_url", description="The image's url of the embed.", required=False)
    @option(
        "thumbnail_url", description="The thumbnail's url of the embed.", required=False
    )
    @option(
        "timestamp",
        description="Determines if the timestamp will show up.",
        required=False,
    )
    @option(
        "colour",
        description=f"The colour of the embed, in hex.(#6db2d9 by default)",
        required=False,
    )
    @commands.has_permissions(manage_messages=True)
    async def embed(
        self,
        ctx: discord.ApplicationContext,
        title: str,
        url: str,
        description: str,
        footer_text: str,
        footer_icon_url: str,
        author_text: str,
        author_icon_url: str,
        author_url: str,
        image_url: str,
        thumbnail_url: str,
        timestamp: bool,
        colour: str,
    ):
        ademb = discord.Embed(title=f"{ctx.author} posted an embed", colour=cfc)
        if colour == None:
            colour = f"6db2d9"
        else:
            colour = colour
        ademb.add_field(
            name="General",
            value=f"""
Title: {title}
Description: {description}
Colour: `#{colour}`
Timestamp: {timestamp}
URL: `{url}`
                            """,
            inline=False,
        )
        if timestamp == True:
            timestamp = datetime.now()
        else:
            timestamp = None
        emb = discord.Embed(
            title=title,
            description=description,
            colour=int(colour, 16),
            url=url,
            timestamp=timestamp,
        )
        if footer_text != None:
            if footer_icon_url != None:
                emb.set_footer(text=footer_text, icon_url=footer_icon_url)
            else:
                emb.set_footer(text=footer_text)
            ademb.add_field(
                name="Footer:",
                value=f"**Text:** {footer_text}\n**Icon URL:** `{footer_icon_url}`",
                inline=False,
            )
        if author_text != None:
            if author_icon_url != None:
                emb.set_author(name=author_text, icon_url=author_icon_url)
            else:
                emb.set_author(name=author_text)
            ademb.add_field(
                name="Author:",
                value=f"**Text:** {author_text}\n**URL:** `{author_url}`\n**Icon URL:** `{author_icon_url}`",
                inline=False,
            )
        if image_url != None:
            emb.set_image(url=image_url)
            ademb.add_field(name="Image URL:", value=f"`{image_url}`")
        if thumbnail_url != None:
            emb.set_thumbnail(url=thumbnail_url)
            ademb.add_field(name="Thumbnail URL:", value=f"`{thumbnail_url}`")
        await ctx.channel.send(embed=emb)
        await ctx.respond("Posted your embed!", ephemeral=True)
        logchannel = self.bot.get_channel(1001405648828891187)
        ademb.set_thumbnail(url=ctx.author.display_avatar.url)
        await logchannel.send(embed=ademb)

    @admin.command(name="spam", description="⌨️ Spam the channel to oblivion.")
    @option("amount", description="Amount of messages to spam.")
    @option("text", description="What you want to spam.")
    @commands.has_permissions(manage_channels=True)
    async def spam(self, ctx: discord.ApplicationContext, amount: int, text: str):
        channel = self.bot.get_channel(1001405648828891187)
        user = ctx.author
        global confirm
        confirm = 0
        if amount >= 100:

            class Spam(discord.ui.View):
                def __init__(self, bot):
                    self.bot = bot
                    super().__init__(timeout=15.0)

                @discord.ui.button(
                    custom_id="okbutton", style=discord.ButtonStyle.green, label="Yes"
                )
                async def button_callback(self, button, interaction):
                    global confirm
                    confirm = 1
                    channel = self.bot.get_channel(1001405648828891187)
                    await interaction.response.send_message(
                        f"Ok, here we go! `{ctx.channel}` {amount} times",
                        ephemeral=True,
                    )
                    embed = discord.Embed(
                        title=f"**{ctx.author}** spammed `{ctx.channel}` **{amount} times**(after confirmation) with the following text:",
                        description=text,
                        color=cfc,
                    )
                    embed.set_thumbnail(url=ctx.author.display_avatar.url)
                    await channel.send(embed=embed)
                    for i in range(amount):
                        await ctx.send(text)

                @discord.ui.button(
                    custom_id="nobutton", style=discord.ButtonStyle.danger, label="No"
                )
                async def second_button_callback(self, button, interaction):
                    global confirm
                    confirm = 1
                    await interaction.response.send_message(
                        f"Ok, cancelling.", ephemeral=True
                    )
                    await ctx.edit(view=None)

                async def on_timeout(self):
                    global confirm
                    if confirm == 0:
                        await ctx.edit(view=None)
                        await ctx.respond(
                            "You waited too long. Rerun the command to start over!",
                            ephemeral=True,
                        )
                    else:
                        return

            embed = discord.Embed(
                title="**Do you want to continue?**",
                description=f"You are spamming **{amount} times**. That's a lot!",
                color=cfc,
            )
            await ctx.respond(embed=embed, view=Spam(bot=self.bot), ephemeral=True)
        else:
            chnlmention = self.bot.get_channel(ctx.channel.id)
            embed = discord.Embed(
                title=f"**{ctx.author}** spammed `{ctx.channel}` **{amount} times** with the following text:",
                description=text,
                color=cfc,
            )
            embed.set_thumbnail(url=user.display_avatar.url)
            await ctx.respond(
                "Get ready for the show <:aye:965627580743024671>", ephemeral=True
            )
            await channel.send(embed=embed)
            for i in range(amount):
                await ctx.send(text)

    @admin.command(name="slowmode", description="⏰ Set the slowmode time of a channel.")
    @option(
        "slowmode", description="The amount of time the slowmode should be, in seconds."
    )
    @option(
        "channel", description="The channel to apply the slowmode to.", required=False
    )
    @commands.has_permissions(manage_channels=True)
    async def sm(
        self,
        ctx: discord.ApplicationContext,
        slowmode: int,
        channel: discord.TextChannel,
    ):
        logchannel = self.bot.get_channel(1001405648828891187)
        if slowmode > 21600:
            await ctx.respond("Maximum slowmode is 21600(6 hours) seconds!")
        if channel == None:
            channel = ctx.channel
        await channel.edit(slowmode_delay=slowmode)
        embed = discord.Embed(
            title=f"`{channel}`'s slow mode has been set to {slowmode} second(s)!",
            color=cfc,
        )
        await ctx.respond(embed=embed)
        embed = discord.Embed(
            title=f"{ctx.author} changed `{channel.mention}` slowmode to {slowmode} second(s).",
            colour=cfc,
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        await logchannel.send(embed=embed)

    @admin.command(description="🗑️ Delete large amounts of messages from a channel.")
    @option("amount", description="The number of messages you want to delete.")
    @commands.has_permissions(manage_channels=True)
    async def purge(self, ctx: discord.ApplicationContext, amount: int):
        global confirm
        confirm = 0
        channel = self.bot.get_channel(1001405648828891187)
        if amount > 100:

            class PurgeView(discord.ui.View):
                def __init__(self, bot):
                    self.bot = bot
                    super().__init__(timeout=15.0)

                @discord.ui.button(
                    custom_id="okbutton", style=discord.ButtonStyle.green, label="Yes"
                )
                async def button_callback(self, button, interaction):
                    global confirm
                    confirm = 1
                    channel = self.bot.get_channel(1001405648828891187)
                    await interaction.response.send_message(
                        f"Ok, purging {amount} messages.", ephemeral=True
                    )
                    await ctx.channel.purge(
                        limit=amount, check=lambda message: not message.pinned
                    )
                    embed = discord.Embed(
                        title=f"{ctx.author} purged **{amount}** messages in `{ctx.channel}` after confirmation!",
                        color=cfc,
                    )
                    embed.set_thumbnail(url=ctx.author.display_avatar.url)
                    await channel.send(embed=embed)
                    await ctx.edit(view=None)

                @discord.ui.button(
                    custom_id="nobutton", style=discord.ButtonStyle.danger, label="No"
                )
                async def second_button_callback(self, button, interaction):
                    global confirm
                    confirm = 1
                    await interaction.response.send_message(
                        f"Ok, cancelling purge.", ephemeral=True
                    )
                    await ctx.edit(view=None)

                async def on_timeout(self):
                    global confirm
                    if confirm == 0:
                        await ctx.edit(view=None)
                        await ctx.respond(
                            "You waited too long. Rerun the command to purge!",
                            ephemeral=True,
                        )
                    else:
                        return

            embed = discord.Embed(
                title="**Do you want to continue?**",
                description=f"You are purging **{amount} messages**. that's a lot!",
                color=cfc,
            )
            await ctx.respond(embed=embed, view=PurgeView(bot=self.bot), ephemeral=True)
        else:
            await ctx.channel.purge(
                limit=amount, check=lambda message: not message.pinned
            )
            await ctx.respond(f"Purging {amount} messages.", ephemeral=True)
            chnlmention = self.bot.get_channel(ctx.channel.id)
            embed = discord.Embed(
                title=f"{ctx.author} purged **{amount}** messages in `{ctx.channel}`!",
                color=cfc,
            )
            embed.set_thumbnail(url=ctx.author.display_avatar.url)
            await channel.send(embed=embed)

    @admin.command(name="rules", description="Sends the rules.")
    @commands.has_permissions(administrator=True)
    async def rules(self, ctx: discord.ApplicationContext):
        embed1 = discord.Embed(color=cfc).set_image(url="https://github.com/ClearFly-Official/ClearFly-Branding/blob/main/Banners/RulesNFAQ/rules.png?raw=true")
        embed2 = discord.Embed(
            color=cfc,
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
        await ctx.respond("Rules posted!", ephemeral=True)
        await ctx.send(embeds=[embed1, embed2], view=RulesView(bot=self.bot))

    @admin.command(name="faq", description="Sends the faq.")
    @commands.has_permissions(administrator=True)
    async def faq(self, ctx: discord.ApplicationContext):
        embed1 = discord.Embed(colour=cfc).set_image(url="https://github.com/ClearFly-Official/ClearFly-Branding/blob/main/Banners/RulesNFAQ/faq.png?raw=true")
        embed2 = discord.Embed(
            title="Lunar FAQ",
            description="""
**Q: When will the Boeing 737-100 be released?**
A: We don’t currently have a set release date. Follow our progress in <#965597725519405106>

**Q: Will there be a 3D cabin?**
A: Yes!

**Q: Will there be a custom FMC?**
A: This is unlikely, but not impossible in the future.
        """,
            color=cfc,
        )
        await ctx.respond("FAQ posted!", ephemeral=True)
        await ctx.send(embeds=[embed1, embed2], view=FAQView(bot=self.bot))

    @admin.command(name="buttonroles", description="Sends the button roles.")
    @commands.has_permissions(administrator=True)
    async def buttonroles(self, ctx: discord.ApplicationContext):
        emb1 = discord.Embed(
            title="Announcement Pings",
            description="Click on the 📣 to receive pings when we post any announcements.\n*click again to remove.*",
            color=cfc,
        )
        emb2 = discord.Embed(
            title="Update Pings",
            description="Click on 🛠️ to receive pings when we post an update on the 737-100.\n*click again to remove.*",
            color=cfc,
        )
        emb3 = discord.Embed(
            title="Livery Painter",
            description="DM <@871893179450925148> or <@668874138160594985> with some examples of your work.",
            colour=cfc,
        )
        emb4 = discord.Embed(
            title="Lunar Livery Painter",
            description="Create a custom livery for the Lunar virtual airline and share it in <#1087399445966110881>(effort must be shown to qualify for the role).",
            colour=cfc,
        )
        embimg = discord.Embed(
            colour=cfc
        ).set_image(url="https://cdn.discordapp.com/attachments/1054156349568729139/1090335535291179068/roleBanner.png")
        await ctx.respond("Button roles posted!", ephemeral=True)
        await ctx.send(embed=embimg)
        await ctx.send(embed=emb1, view=AnnounceRoleView(bot=self.bot))
        await ctx.send(embed=emb2, view=UpdateRoleView(bot=self.bot))
        await ctx.send(embeds=[emb3, emb4])


def setup(bot):
    bot.add_cog(AdminCommands(bot))
