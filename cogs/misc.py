import discord
from discord.ext import commands

# Contains miscallaneous commands/listeners

class Misc(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client

    @commands.command()
    async def help(self, ctx):
        """
        Provides a description of all the commands for this bot
        """

        await ctx.send("***Commands for individuals:***\n" +
                       "`*score <character>`: Displays the current Raider.IO Mythic+ score of the provided character.\n" +
                       "")

def setup(bot_client):
    bot_client.add_cog(Misc(bot_client))

