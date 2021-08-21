import discord
from discord.ext import commands

bot_client = commands.Bot(command_prefix='*')

# When the bot is ready (occurs in startup)
@bot_client.event
async def on_ready():
    print("Bot is ready")

with open('token.txt', 'r') as f:
    lines = f.readlines()

    # Running the actual bot
    bot_client.run(f'{lines[0]}')
