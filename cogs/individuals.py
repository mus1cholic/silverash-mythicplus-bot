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

        total_score = request_json['current_mythic_rating']['rating']

        character_embed = discord.Embed(title=f"{character_name}'s Raider.IO Profile", url=f"https://raider.io/characters/{realm}/{server}/{character_name}", 
            description="", color=dicord.Color.blue()) # TODO: pair color with spec (shaman is blue, etc...)

        character_embed.set_author(name=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        character_embed.add_field(name="Overall Statistics", value=f"**Total Score: {total_score}**\n" +
                                                                   f"Tank Score: 0\n" +
                                                                   f"Healer Score: 0\n" +
                                                                   f"DPS Score: 0", inline=False)

        character_embed.add_field(name="Rankings", value=f"Spec Rank: #100 Frost Mage")

        character_embed.add_field(name="Best Dungeons")

        character_embed.add_field(name="Dungeon Name", value="DOS\nNW", inline=True)
        character_embed.add_field(name="Fortified", value="13\n15", inline=True)
        character_embed.add_field(name="Tyrannical", value="19\n11", inline=True)
        character_embed.add_field(name="Total Score", value="232.4\n101.3", inline=True)

        await ctx.send(embed=character_embed)

def setup(bot_client):
    bot_client.add_cog(Individuals(bot_client))
