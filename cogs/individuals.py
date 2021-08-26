import discord
import requests

from discord.ext import commands

# Contains commands/listeners relevant to individuals

class Individuals(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client

    @commands.command()
    async def score(self, ctx, *, args):
        """
        Sends out the score of the player
        """

        realm, server, character_name = "", "", ""

        if args == "":
        	# TODO: write code to see whether setcharacter has been done for this character 
        	pass
        else:
        	character_split = args.split("/")

        	# TODO: refactor
	        try:
	            assert len(character_split) == 3, "`<character>` field must follow format `realm/server/character_name`!"
	        except AssertionError:
	            await ctx.send("`<character>` field must follow format `realm/server/character_name`!")
	            raise

        	realm = character_split[0]
	        server = character_split[1]
	        character_name = character_split[2]


	    # TODO: refactor out this part too?
        with open('./apiurl.txt', 'r') as f:
            api_url = f.readlines()[0]
            api_url = api_url.replace("{}", server, 1)
            api_url = api_url.replace("{}", character_name, 1)
            api_url = api_url.replace("{}", realm, 1)

        r = requests.get(api_url)

        try:
            assert r.status_code != 404, f"character `{character_name}` from `{server}` does not exist, perhaps you misspelled?"
        except AssertionError:
            await ctx.send(f"character `{character_name}` from `{server}` does not exist, perhaps you misspelled?")
            raise

        request_json = r.json()

        await ctx.send(f"`{character_name}`'s current Mythic+ score: {request_json['current_mythic_rating']['rating']}")

def setup(bot_client):
    bot_client.add_cog(Individuals(bot_client))
