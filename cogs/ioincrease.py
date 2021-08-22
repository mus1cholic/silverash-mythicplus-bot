import discord
import os

from discord.ext import commands

# Contains commands/listeners relevant to ioincrease

class Ioincrease(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client

    @commands.command()
    async def track(self, ctx, *, character):
        """
        Starts tracking the specified character
        """

        character_split = character.split("/")
        assert len(character_split) == 3, "`<character>` field must follow format `us/stormrage/character_name`!"

        if not os.path.isfile("../data/tracking.json"):
            print("Required file tracking.json does not exist, creating one right now:")
            with open('../data/tracking.json', 'w+') as f:
                # TODO: make this into a constants file
                DEFAULT_TRACKING_JSON = [{'example_discord_unique_id': {'realm': 'us', 'server': 'stormrage', 'character_name': 'sample_name'}}]
                json.dump(DEFAULT_TRACKING_JSON, f)

        with open('../data/tracking.json', 'w+') as f:
            tracking = json.load(f)
            if self.bot_client.user.id in tracking.keys():
                await ctx.send(f'@{self.bot_client.user.name}, character {tracking[self.bot_client.user.id][character_name]} is already being tracked. To untrack this character, do `~untrack <character>`')
            else:
                # TODO: make an assert that <character> is trackable
                
                tracking[self.bot_client.user.id] = {'realm': character_split[0], 'server': character_split[1], 'character_name': character_split[2]}
                json.dump(tracking, f)
                await ctx.send(f'@{self.bot_client.user.name}, character {character_split[2]} is now being tracked.')

def setup(bot_client):
    bot_client.add_cog(Ioincrease(bot_client))
