import discord
import pymongo
import os
from main import cogs
from discord import option
from discord.ext import commands
from dotenv import load_dotenv
from main import cfc, errorc

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
    async def view(self, ctx: discord.ApplicationContext, tag, raw: bool):
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
        tagsList = "\n".join(tags)

        embed = discord.Embed(
            title="Tag list:",
            description=f"""
{tagsList}
        """,
            colour=cfc,
        )
        embed.set_footer(text=f"There are a total of {len(tags)} tags.")
        await ctx.respond(embed=embed)

    @tags.command(description="➕ Add a new tag.")
    @commands.has_role(965422406036488282)
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
    @commands.has_role(965422406036488282)
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

        modal = EditTagModal(title="Create a new tag.")
        await ctx.send_modal(modal)

    @tags.command(description="⛔️ Delete a tag.")
    @commands.has_role(965422406036488282)
    @option("tag", description="The tag you want to delete.", autocomplete=get_tags)
    async def delete(self, ctx: discord.ApplicationContext, tag: str):
        tagcol.delete_one({"name": tag})
        embed = discord.Embed(title="Tag deleted successfully", colour=cfc)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(TagCommands(bot))
