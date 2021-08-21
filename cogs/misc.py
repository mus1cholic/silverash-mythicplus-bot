import discord
from discord.ext import commands

# Contains miscallaneous commands/listeners

class Misc(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client

def setup(bot_client):
    bot_client.add_cog(Misc(bot_client))

