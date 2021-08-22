import discord
import os
import sys, traceback

from discord.ext import commands

bot_client = commands.Bot(command_prefix='~')

# When the bot is ready (occurs in startup)
@bot_client.event
async def on_ready():
    print(f'\n\nLogged in as: {bot_client.user.name} - {bot_client.user.id}\nVersion: {discord.__version__}\n')

    # Changes the bot's status (the Playing XXXX thing)
    await bot_client.change_presence(activity=discord.Game(name='Under development!', type=0))

    # Loading all the cogs
    for f in os.listdir('./cogs'):
        if f.endswith('.py'):
            extension_name = f'cogs.{f[:-3]}'
            try:
                bot_client.load_extension(extension_name)
                print(f'Cog {extension_name} loaded successfully')
            # TODO: more specific exception
            except Exception as e:
                print(f'Failed to load extension {extension_name}.', file=sys.stderr)
                traceback.print_exc()

    print(f'Successfully logged in and booted...!')



# Running the actual bot using token
with open('token.txt', 'r') as f:
    lines = f.readlines()
    bot_client.run(f'{lines[0]}')
