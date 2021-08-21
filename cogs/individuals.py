import discord
from discord.ext import commands

# Contains commands/listeners relevant to individuals

class Individuals(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client

    @commands.command()
    async def score(self, ctx):
        """
        Sends out the score of the player
        """
        await ctx.send("1000")

def setup(bot_client):
    bot_client.add_cog(Individuals(bot_client))
