import discord
import pymongo
import os
import time
from main import cogs
from discord import option
from discord.ext import commands
from dotenv import load_dotenv
from main import cfc, errorc
from discord.ext.pages import Page, Paginator

load_dotenv()

client = pymongo.MongoClient(os.environ["MONGODB_URI"])
db = client["ClearBotDB"]
tagcol = db["tags"]


class TagCommands(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    tags = discord.SlashCommandGroup(name="tag", description="Tag related commands")

    @commands.Cog.listener()
    async def on_ready(self):
        print("| Tags cog loaded sucessfully")

    async def get_tags(ctx: discord.AutocompleteContext):
        tags = []
        for tag in tagcol.find():
            tags.append(tag.get("name"))
        return [tag for tag in tags if ctx.value in tag]

    @tags.command(description="🔎 View a tag.")
    @option("tag", description="The tag you want to view.", autocomplete=get_tags)
    @option(
        "raw",
        description="Toggles if you want to view the tag raw, for copying/editing.",
        required=False,
    )
    @option(
        "info",
        description="Toggles if you want to view information about the tag.",
        required=False
    )
    async def view(self, ctx: discord.ApplicationContext, tag: str, raw: bool, info: bool):
        tags = []
        for tag_ in tagcol.find():
            tags.append(tag_.get("name"))
        if tag in tags:
            output = tagcol.find_one({"name": tag})
            if raw:
                await ctx.respond(
                    f"```\n{output.get('value')}\n```",
                    allowed_mentions=discord.AllowedMentions.none(),
                )
            elif info:
                embed = discord.Embed(
                    title="Tag information",
                    colour=cfc
                )
                tagAuthor = await self.bot.fetch_user(int(output.get("author")))
                embed.add_field(name="Name", value=output.get("name"), inline=False)
                embed.add_field(name="Value", value=output.get("value"), inline=False)
                embed.add_field(name="Author", value=tagAuthor.mention, inline=False)
                embed.add_field(name="Created At", value=f"<t:{round(int(output.get('created_at')))}:f>(<t:{round(int(output.get('created_at')))}:R>)")
                embed.add_field(name="Edited At", value=f"<t:{round(int(output.get('edited_at')))}:f>(<t:{round(int(output.get('edited_at')))}:R>)")
                embed.set_thumbnail(url=tagAuthor.avatar.url)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond(
                    f"{output.get('value')}",
                    allowed_mentions=discord.AllowedMentions.none(),
                )
        else:
            embed = discord.Embed(
                title="Error 404",
                description=f"""
Didn't found {tag}. 
            """,
                colour=errorc,
            )
            await ctx.respond(embed=embed)

    @tags.command(description="📂 List all the tags.")
    async def list(self, ctx: discord.ApplicationContext):
        tags = []
        for tag_ in tagcol.find():
            tags.append(tag_.get("name"))
        var = 0
        var2 = 1
        for i in tags:
            tags[var] = f"{var2}: " + f"`{tags[var]}`"
            var += 1
            var2 += 1

        chunks = [tags[i : i + 25] for i in range(0, len(tags), 25)]

        pages = [
            Page(
                embeds=[
                    discord.Embed(
                        title=f"Tags {i+1}-{i+len(chunk)}",
                        description="\n".join(chunk),
                        colour=cfc
                    ).set_footer(text=f"Showing 25/page, total of {len(tags)} tags")
                ]
            )
            for i, chunk in enumerate(chunks)
        ]
        paginator = Paginator(pages)
        await paginator.respond(ctx.interaction)

    @tags.command(description="➕ Add a new tag.")
    @option("name", description="The name of the new tag.")
    @option("value", description="The value of the new tag.")
    async def add(self, ctx: discord.ApplicationContext):
        class AddTagModal(discord.ui.Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)

                self.add_item(
                    discord.ui.InputText(label="Name of tag", placeholder="foo")
                )
                self.add_item(
                    discord.ui.InputText(
                        label="Value of tag",
                        style=discord.InputTextStyle.long,
                        placeholder="A very interesting value.",
                    )
                )

            async def callback(self, interaction: discord.Interaction):
                try:
                    tagcol.insert_one(
                        {
                            "name": self.children[0].value,
                            "value": self.children[1].value,
                            "author": ctx.author.id,
                            "created_at": time.time(),
                            "edited_at": time.time(),
                        }
                    )
                    embed = discord.Embed(
                        title=f"Tag created with following data:",
                        description=f"\n\n**Name:** {self.children[0].value}\n\n**Value:** {self.children[1].value}",
                        colour=cfc,
                    )
                    await interaction.response.send_message(embed=embed)
                except Exception as error:
                    await interaction.response.send_message(f"```{error}```")

        modal = AddTagModal(title="Create a new tag.")
        await ctx.send_modal(modal)

    @tags.command(description="✍️ Edit a tag.")
    @option("edit", description="The tag you want to edit.", autocomplete=get_tags)
    @option("name", description="The name of the edited tag.")
    @option("value", description="The value of the edited tag.")
    async def edit(self, ctx: discord.ApplicationContext, edit: str):
        class EditTagModal(discord.ui.Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)

                self.add_item(
                    discord.ui.InputText(label="Name of tag", placeholder="foo")
                )
                self.add_item(
                    discord.ui.InputText(
                        label="Value of tag",
                        style=discord.InputTextStyle.long,
                        placeholder=f"A value that's very, very interesting and useful.",
                    )
                )

            async def callback(self, interaction: discord.Interaction):
                tags = []
                for tag_ in tagcol.find():
                    tags.append(tag_.get("name"))
                if edit in tags:
                    tagcol.update_one(
                        {"name": edit},
                        {
                            "$set": {
                                "name": self.children[0].value,
                                "value": self.children[1].value,
                                "edited_at": time.time()
                            }
                        },
                    )
                    embed = discord.Embed(
                        title=f"Tag edited with following data:",
                        description=f"\n\n**Name:** {self.children[0].value}\n\n**Value:** {self.children[1].value}",
                        colour=cfc,
                    )
                    await interaction.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error 404",
                        description=f"""
Didn't found {edit}. 
                        """,
                        colour=errorc,
                    )
                    await interaction.response.send_message(embed=embed)
        editTag = tagcol.find_one({"name": edit})
        if int(editTag['author']) == ctx.author.id:
            modal = EditTagModal(title="Create a new tag.")
            await ctx.send_modal(modal)
        elif 965422406036488282 in ctx.author.roles:
            modal = EditTagModal(title="Create a new tag.")
            await ctx.send_modal(modal)
        else:
            embed = discord.Embed(title="Error 403!", description="You are not authorised to edit this tag!", colour=errorc)
            await ctx.respond(embed=embed)


    @tags.command(description="⛔️ Delete a tag.")
    @option("tag", description="The tag you want to delete.", autocomplete=get_tags)
    async def delete(self, ctx: discord.ApplicationContext, tag: str):
        deltag = tagcol.find_one({"name": tag})
        if int(deltag['author']) == ctx.author.id:
            tagcol.delete_one({"name": tag})
            embed = discord.Embed(title=f"Tag `{tag}` deleted successfully", colour=cfc)
        elif 965422406036488282 in ctx.author.roles:
            tagcol.delete_one({"name": tag})
            embed = discord.Embed(title=f"Tag `{tag}` deleted successfully", colour=cfc)
        else:
            embed = discord.Embed(title="Error 403!", description="You are not authorised to delete this tag!", colour=errorc)
            
        await ctx.resopnd(embed=embed)


def setup(bot):
    bot.add_cog(TagCommands(bot))
