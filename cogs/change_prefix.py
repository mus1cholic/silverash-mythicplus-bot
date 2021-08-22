import discord
from discord.ext import commands


class Prefix(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client

    @commands.command()
    async def change_prefix(self, ctx, new_prefix):
        """
        Changes the command prefix of this bot
        """
        if len(new_prefix) == 1:
            self.bot_client.command_prefix = new_prefix
            await ctx.send(f"The prefix of this bot has now been changed to {new_prefix}")
        else:
            await ctx.send("The entered prefix has a length greater than 1. "
                           "Please enter a valid prefix")


def setup(bot_client):
    bot_client.add_cog(Prefix(bot_client))


