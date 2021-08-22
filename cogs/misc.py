import discord
from discord.ext import commands

# Contains miscallaneous commands/listeners

class Misc(commands.Cog):
    def __init__(self, bot_client):
        bot_client.remove_command('help')

        self.bot_client = bot_client

    @commands.command()
    async def help(self, ctx):
        """
        Provides a description of all the commands for this bot
        """

        await ctx.send("**Commands for individuals:**\n" +
                       "`~score <character>`: Displays the current Raider.IO Mythic+ score of the provided character.\n" +
                       "")

    @commands.command()
    async def change_prefix(self, ctx, new_prefix):
        """
        Changes the command prefix of this bot
        """
        if new_prefix == self.bot_client.command_prefix:
            await ctx.send(f"The current prefix is already {new_prefix}")
        elif len(new_prefix) == 1:
            self.bot_client.command_prefix = new_prefix
            await ctx.send(f"The prefix of this bot has now been changed to {new_prefix}")
        else:
            await ctx.send("The entered prefix is not of length 1. "
                           "Please enter a valid prefix")


def setup(bot_client):
    bot_client.add_cog(Misc(bot_client))

