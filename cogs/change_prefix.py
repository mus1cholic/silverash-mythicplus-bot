import discord
from discord.ext import commands

bot_client = commands.Bot(command_prefix='.')


@bot_client.command()
async def change_prefix(ctx, new_prefix):
    """
    Changes the command prefix of this bot
    """
    if len(new_prefix) == 1:
        bot_client.command_prefix = new_prefix
        await ctx.send(f"The prefix of this bot has been changed to {new_prefix}.")
    else:
        await ctx.send("The entered prefix has a length greater than 1. "
                       "Please enter a valid prefix.")
    return new_prefix

bot_client.run('')
