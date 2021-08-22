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
                       "`~score <character>`: Displays the current Raider.IO Mythic+ score of the provided character\n" +
                       "`~setcharacter <character>`: Sets the specified character to be the user's default character\n" +
                       "**Leaderboard Commands:**\n" +
                       "`~leaderboards show <filter>`: Shows the leaderboard with the provided filter. Filters by Raider.IO Mythic+ score by default. Must be tracking at least one character through `~ioincrease track`\n" +
                       "`~leaderboards page <number>`: Displays the leaderboard's <number>th page\n" +
                       "`~leaderboards rank <character> <filter>`: Displays the ranking of the given character for the given leaderboard filter type\n" +
                       "**Ioincrease Commands:**\n" +
                       "`~ioincrease track <character>`: Starts tracking the given character\n" +
                       "`~ioincrease untrack <character>`: Stops tracking the given character. Admin only unless used on own character\n" +
                       "`~ioincrease update`: Performs a manual ioincrease update of everyone that is being tracked\n" +
                       "`~ioincrease purge`: Untracks all characters. Admin only\n"
                       "**Miscallaenous Commands:**\n" +
                       "`~help`: Displays the current menu\n" +
                       "`~info`: Shows some information about the bot\n" +
                       "`~reload`: Reloads the bot and fetches the newest version\n" +
                       "`~reportbug` <message>: Reports the <message> as a bug\n"
                       "`changeprefix <prefix>`: Changes the prefix of the bot to another key")

    # TODO: reload all modules: https://github.com/Rapptz/RoboDanny/blob/27417da0da48c06df7a54e44527ec10dbf78b339/cogs/admin.py#L165

def setup(bot_client):
    bot_client.add_cog(Misc(bot_client))

