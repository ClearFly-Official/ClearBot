import discord
import pymongo
import os
from main import cogs
from discord import option
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

client = pymongo.MongoClient(os.environ['MONGODB_URI'])
db = client["ClearBotDB"]
tagcol = db['tags']

#cfc = 0x2681b4 #<- default color
#cfc = 0xcc8d0e # <- halloween color
cfc = 0x00771d # <- christmas color
errorc = 0xFF0000

class TagCommands(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    tags = discord.SlashCommandGroup(name="tag", description="Tag related commands")
    
    async def get_tags(ctx: discord.AutocompleteContext):
        tags = []
        for tag in tagcol.find():
            tags.append(tag.get("name"))
        return [tag for tag in tags if ctx.value in tag]

    @tags.command(description="View a tag.")
    @option("tag", description="The tag you want to view.",autocomplete=get_tags)
    async def view(self, ctx, tag):
        tags = []
        for tag_ in tagcol.find():
            tags.append(tag_.get("name"))
        if tag in tags:
            output = tagcol.find_one({"name":tag})
            await ctx.respond(f"{output.get('value')}")
        else:
            embed = discord.Embed(title="Error 404", description=f"""
Didn't found {tag}. 
            """, colour=errorc)
            await ctx.respond(embed=embed)

    @tags.command(description="List all the tags.")
    async def list(self, ctx):
        tags = []
        for tag_ in tagcol.find():
            tags.append(tag_.get("name"))
        print(tags)
        var = 0
        var2 = 1
        for i in tags:
            tags[var] = f"{var2}: " + tags[var]
            var += 1
            var2 += 1
        tagsList = '\n'.join(tags)

        embed = discord.Embed(title="Tag list:", description=f"""
{tagsList}
        """, colour=cfc)
        await ctx.respond(embed=embed)

    @tags.command(description="Add a new tag")
    @commands.has_permissions(manage_channels=True)
    @option("name", description="The name of the new tag.")
    @option("value", description="The value of the new tag.")
    async def add(self, ctx):
        class AddTagModal(discord.ui.View):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)

                self.add_item(discord.ui.InputText(label="Name of tag", placeholder="foo"))
                self.add_item(discord.ui.InputText(label="Value of tag", style=discord.InputTextStyle.long), placeholder="A very interesting value.")

            async def callback(self, interaction: discord.Interaction):
                try:
                    tagcol.insert_one({
                        "_id":self.children[0].value,
                        "name":self.children[0].value,
                        "value":self.children[1].value
                    })
                    embed = discord.Embed(title=f"Tag created with following data:",description=f"\n\n**Name:** {self.children[0].value}\n\n**Value:** {self.children[1].value}", colour=cfc)
                    await ctx.respond(embed=embed)
                except Exception as error:
                    await ctx.respond(f"```{error}```")
        modal = AddTagModal(title="Create a new tag.")
        await ctx.send_modal(modal)

    @tags.command(description="Edit a tag.")
    @commands.has_permissions(manage_channels=True)
    @option("edit", description="The tag you want to edit.", autocomplete=get_tags)
    @option("name", description="The name of the edited tag.")
    @option("value", description="The value of the edited tag.")
    async def edit(self, ctx, edit):
        class EditTagModal(discord.ui.View):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)

                self.add_item(discord.ui.InputText(label="Name of tag", placeholder="foo"))
                self.add_item(discord.ui.InputText(label="Value of tag", style=discord.InputTextStyle.long), placeholder="A very interesting value.")

            async def callback(self, interaction: discord.Interaction):
                try:
                    tags = []
                    for tag_ in tagcol.find():
                        tags.append(tag_.get("name"))
                    if edit in tags:
                        tagcol.update_one({"name":edit}, {
                            "$set":{
                                "_id":self.children[0].value,
                                "name":self.children[0].value,
                                "value":self.children[1].value
                            }
                        })
                        embed = discord.Embed(title=f"Tag edited with following data:", description=f"\n\n**Name:** {self.children[0].value}\n\n**Value:** {self.children[1].value}", colour=cfc)
                        await ctx.respond(embed=embed)
                    else:
                        embed = discord.Embed(title="Error 404", description=f"""
Didn't found {edit}. 
                        """, colour=errorc)
                        await ctx.respond(embed=embed)
                except Exception as error:
                    await ctx.respond(f"```{error}```")
        modal = EditTagModal(title="Create a new tag.")
        await ctx.send_modal(modal)

    @tags.command(description="Delete a tag.")
    @commands.has_permissions(manage_channels=True)
    @option("tag", description="The tag you want to delete.", autocomplete=get_tags)
    async def delete(self, ctx, tag):
        tagcol.delete_one({"name":tag})
        embed = discord.Embed(title="Tag deleted successfully", colour=cfc)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(TagCommands(bot))