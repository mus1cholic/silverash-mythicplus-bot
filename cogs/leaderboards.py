import discord
from discord.ext import commands

# Contains commands/listeners relevant to leaderboards

class Leaderboards(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client
        
def setup(bot_client):
    bot_client.add_cog(Leaderboards(bot_client))

