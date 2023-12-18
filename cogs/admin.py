import discord
from discord import option
from discord.ext import commands
import datetime

from main import ClearBot


class AdminCommands(discord.Cog):
    def __init__(self, bot: ClearBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            "\033[34m|\033[0m \033[96;1mAdmin\033[0;36m cog loaded sucessfully\033[0m"
        )

    admin = discord.SlashCommandGroup(
        name="admin", description="🔒 Commands for admins only."
    )

    @admin.command(name="echo", description="💬 Send a message as ClearBot.")
    @option("text", description="The text you want to send as the bot.")
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def echo(self, ctx: discord.ApplicationContext, text: str):
        sendable = self.bot.sendable_channel(ctx.channel)
        if sendable:
            await sendable.send(text)
        else:
            raise ValueError("Invalid channel")

        emb = discord.Embed(
            title=f"{ctx.author} used echo", description=text, color=self.bot.color()
        )
        emb.set_thumbnail(url=ctx.author.display_avatar.url)
        await self.bot.send_log(embed=emb)
        await ctx.respond("Posted your message!", ephemeral=True)

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
    @commands.cooldown(1, 10, commands.BucketType.user)
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
        ademb = discord.Embed(
            title=f"{ctx.author} posted an embed", colour=self.bot.color()
        )
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

        emb = discord.Embed(
            title=title,
            description=description,
            colour=int(colour, 16),
            url=url,
        )

        if timestamp:
            emb.timestamp = datetime.datetime.now()

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

        sendable = self.bot.sendable_channel(ctx.channel)
        if sendable:
            await sendable.send(embed=emb)
        else:
            raise ValueError("Invalid channel")

        await ctx.respond("Posted your embed!", ephemeral=True)
        ademb.set_thumbnail(url=ctx.author.display_avatar.url)
        await self.bot.send_log(embed=ademb)

    @admin.command(name="spam", description="⌨️ Spam the channel to oblivion.")
    @option("amount", description="Amount of messages to spam.")
    @option("text", description="What you want to spam.")
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def spam(self, ctx: discord.ApplicationContext, amount: int, text: str):
        user = ctx.author
        if amount >= 100:

            class Spam(discord.ui.View):
                def __init__(self, bot: ClearBot):
                    self.bot = bot
                    self.confirm = 0
                    super().__init__(timeout=15.0, disable_on_timeout=True)

                @discord.ui.button(style=discord.ButtonStyle.green, label="Yes")
                async def button_callback(
                    self, button: discord.Button, interaction: discord.Interaction
                ):
                    self.confirm = 1
                    await interaction.response.send_message(
                        f"Ok, here we go! `{ctx.channel}` {amount} times",
                        ephemeral=True,
                    )
                    embed = discord.Embed(
                        title=f"**{ctx.author}** spammed `{ctx.channel}` **{amount} times** (after confirmation) with the following text:",
                        description=text,
                        color=self.bot.color(),
                    )
                    embed.set_thumbnail(url=ctx.author.display_avatar.url)
                    await self.bot.send_log(embed=embed)
                    for i in range(amount):
                        await ctx.send(text)

                @discord.ui.button(style=discord.ButtonStyle.danger, label="No")
                async def second_button_callback(self, button, interaction):
                    self.confirm = 1
                    await interaction.response.send_message(
                        f"Ok, cancelling.", ephemeral=True
                    )
                    await ctx.edit(view=None)

                async def on_timeout(self):
                    if self.confirm == 0:
                        await ctx.respond(
                            "You waited too long. Rerun the command to start over!",
                            ephemeral=True,
                        )
                    else:
                        return

            embed = discord.Embed(
                title="**Do you want to continue?**",
                description=f"You are spamming **{amount} times**. That's a lot!",
                color=self.bot.color(),
            )
            await ctx.respond(embed=embed, view=Spam(bot=self.bot), ephemeral=True)
        else:
            embed = discord.Embed(
                title=f"**{ctx.author}** spammed `{ctx.channel}` **{amount} times** with the following text:",
                description=text,
                color=self.bot.color(),
            )
            embed.set_thumbnail(url=user.display_avatar.url)
            await ctx.respond(
                "Get ready for the show <:aye:965627580743024671>", ephemeral=True
            )
            await self.bot.send_log(embed=embed)
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
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sm(
        self,
        ctx: discord.ApplicationContext,
        slowmode: int,
        channel: discord.TextChannel,
    ):
        if slowmode > 21600:
            await ctx.respond("Maximum slowmode is 21600(6 hours) seconds!")

        if not channel:
            if isinstance(ctx.channel, discord.TextChannel):
                channel = ctx.channel
            else:
                await ctx.respond("You can't use that command here!", ephemeral=True)
                return

        await channel.edit(slowmode_delay=slowmode)
        embed = discord.Embed(
            title=f"`{channel}`'s slow mode has been set to {slowmode} second(s)!",
            color=self.bot.color(),
        )
        await ctx.respond(embed=embed)

    @admin.command(description="🗑️ Delete large amounts of messages from a channel.")
    @option("amount", description="The number of messages you want to delete.")
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def purge(self, ctx: discord.ApplicationContext, amount: int):
        if amount > 100:

            class PurgeView(discord.ui.View):
                def __init__(self, bot: ClearBot):
                    self.bot = bot
                    self.confirm = 0
                    super().__init__(timeout=15.0, disable_on_timeout=True)

                @discord.ui.button(style=discord.ButtonStyle.green, label="Yes")
                async def yes_callback(
                    self, button: discord.Button, interaction: discord.Interaction
                ):
                    self.confirm = 1
                    await interaction.response.send_message(
                        f"Ok, purging {amount} messages.", ephemeral=True
                    )
                    sendable = self.bot.sendable_channel(ctx.channel)
                    if sendable:
                        await sendable.purge(
                            limit=amount, check=lambda message: not message.pinned
                        )

                    embed = discord.Embed(
                        title=f"{ctx.author} purged **{amount}** messages in `{ctx.channel}` after confirmation!",
                        color=self.bot.color(),
                    )
                    embed.set_thumbnail(url=ctx.author.display_avatar.url)
                    await self.bot.send_log(embed=embed)
                    await ctx.edit(view=None)

                @discord.ui.button(style=discord.ButtonStyle.danger, label="No")
                async def no_callback(
                    self, button: discord.Button, interaction: discord.Interaction
                ):
                    self.confirm = 1
                    await interaction.response.send_message(
                        f"Ok, cancelling purge.", ephemeral=True
                    )
                    await ctx.edit(view=None)

                async def on_timeout(self):
                    if not self.confirm:
                        await ctx.respond(
                            "You waited too long. Re-run the command to purge!",
                            ephemeral=True,
                        )
                    else:
                        return

            embed = discord.Embed(
                title="**Do you want to continue?**",
                description=f"You are purging **{amount} messages**. that's a lot!",
                color=self.bot.color(2),
            )
            await ctx.respond(embed=embed, view=PurgeView(bot=self.bot), ephemeral=True)
        else:
            sendable = self.bot.sendable_channel(ctx.channel)
            if sendable:
                await sendable.purge(
                    limit=amount, check=lambda message: not message.pinned
                )

            await ctx.respond(f"Purging {amount} messages.", ephemeral=True)
            embed = discord.Embed(
                title=f"{ctx.author} purged **{amount}** messages in `{ctx.channel}`!",
                color=self.bot.color(),
            )
            embed.set_thumbnail(url=ctx.author.display_avatar.url)
            await self.bot.send_log(embed=embed)

    @admin.command(name="setup", description="⚙️ Setup the server.")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setup(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral=True)

        res = await self.bot.setup_server()

        await ctx.respond("Posted!" if res else "Something went wrong...")


def setup(bot):
    bot.add_cog(AdminCommands(bot))
