import discord
import os
import json

from discord.ext import commands

# Contains commands/listeners relevant to ioincrease

class Ioincrease(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client

    @commands.command()
    async def ioincrease(self, ctx, *, args):
        args_split = args.split(" ")
        if args_split[0] == 'track':
            await self.track(ctx, args_split[1])

    async def track(self, ctx, character):
        """
        Starts tracking the specified character
        """

        character_split = character.split("/")
        try:
            assert len(character_split) == 3, "`<character>` field must follow format `realm/server/character_name`!"
        except AssertionError:
            await ctx.send("`<character>` field must follow format `realm/server/character_name`!")
            raise
        
        if not os.path.isfile("data/tracking.json"):
            print("Required file tracking.json does not exist, creating one now")

            # TODO: make this into a constants file
            DEFAULT_TRACKING_JSON = {'example_discord_unique_id': {'realm': 'us', 'server': 'stormrage', 'character_name': 'sample_name'}}
            
            with open('data/tracking.json', 'a') as dumpfile:
                json.dump(DEFAULT_TRACKING_JSON, dumpfile, indent=4)
                

        with open('./data/tracking.json', 'r') as f:
            tracking = json.load(f)
            
        if str(ctx.message.author.id) in tracking.keys():
            await ctx.send(f'{ctx.message.author.mention}, character `{tracking[str(ctx.message.author.id)]["character_name"]}` is already being tracked. To untrack this character, do `~untrack <character>`')
        else:
            # TODO: make an assert that <character> is trackable
            
            tracking[str(ctx.message.author.id)] = {'realm': character_split[0], 'server': character_split[1], 'character_name': character_split[2]}
            with open('./data/tracking.json', 'w') as f:
                json.dump(tracking, f)
            await ctx.send(f'{ctx.message.author.mention}, character `{character_split[2]}` is now being tracked.')

def setup(bot_client):
    bot_client.add_cog(Ioincrease(bot_client))
