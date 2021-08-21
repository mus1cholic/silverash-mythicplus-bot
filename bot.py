import discord
from discord.ext import commands

bot_client = commands.Bot(command_prefix='*')

# When the bot is ready (occurs in startup)
@bot_client.event
async def on_ready():
    print("Bot is ready")

bot_client.run('ODc4NzIyMjQ5NDQ2ODE3ODUy.YSFT3g.AH_pdefkJHeQ1Gcn7V0H8rYju8E')
