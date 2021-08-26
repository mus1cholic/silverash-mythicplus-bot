import discord
import requests
import constants

from discord.ext import commands

# Contains commands/listeners relevant to individuals

class Individuals(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client

    def _convert_role(self, char_role):
        char_role = char_role.lower()

        if char_role == "healing":
            return "healer"

        return char_role

    @commands.command()
    async def score(self, ctx, *, args):
        """
        Sends out the score of the player
        """

        realm, server, character_name = "", "", ""
        api_fields = ['mythic_plus_scores', 'mythic_plus_ranks', 'mythic_plus_best_runs', 'mythic_plus_alternate_runs']

        if args == "":
        	# TODO: write code to see whether setcharacter has been done for this character 
        	pass
        else:
        	character_split = args.split("/")

        	# TODO: refactor
	        try:
	            assert len(character_split) == 3, "`<character>` field must follow format `region/realm/character_name`!"
	        except AssertionError:
	            await ctx.send("`<character>` field must follow format `region/realm/character_name`!")
	            raise

        	region = character_split[0]
	        realm = character_split[1]
	        character_name = character_split[2]


	    # TODO: refactor out this part too?
        api_url = constants.API_URL
        api_url = api_url.replace("{}", region, 1)
        api_url = api_url.replace("{}", realm, 1)
        api_url = api_url.replace("{}", character_name, 1)
        api_url = api_url.replace("{}", '%2C'.join(api_fields))

        r = requests.get(api_url)

        # TODO: use message directly from API response instead of being hardcoded
        try:
            assert r.status_code != 400, f"character `{character_name}` from `{server}` does not exist, perhaps you misspelled?"
        except AssertionError:
            await ctx.send(f"character `{character_name}` from `{server}` does not exist, perhaps you misspelled?")
            raise

        request_json = r.json()

        # Processing the data

        # character data
        char_role = self._convert_role(request_json['active_spec_role'])
        char_class = request_json['class']
        char_spec = request_json['active_spec_name']

        # scores data
        char_total_score = request_json['mythic_plus_scores']['all']
        char_role_score = request_json['mythic_plus_scores'][char_role]
        char_spec_score = request_json['mythic_plus_scores']['spec_0']

        # rank data
        char_role_rank = request_json['mythic_plus_ranks']['dps']
        char_class_rank = request_json['mythic_plus_ranks']['class']
        char_spec_rank = request_json['mythic_plus_ranks'][f'spec_{constants.spec_ids[char_class][char_spec]}']

        # individual dungeon data
        best, nw_best, sd_best, halls_best, plaguefall_best, mists_best, spires_best, top_best, dos_best = request_json['mythic_plus_best_runs'], None, None, None, None, None, None, None, None
        for dungeon in best:
            if best["dungeon"] == "The Necrotic Wake":
                nw_best = best["dungeon"]
            elif best["dungeon"] == "Sanguine Depths":
                sd_best = best["dungeon"]
            elif best["dungeon"] == "Spires of Ascension":
                spires_best = best["dungeon"]
            elif best["dungeon"] == "Mists of Tirna Scithe":
                mists_best = best["dungeon"]
            elif best["dungeon"] == "Halls of Atonement":
                halls_best = best["dungeon"]
            elif best["dungeon"] == "Plaguefall":
                pf_best = best["dungeon"]
            elif best["dungeon"] == "Theatre of Pain":
                top_best = best["dungeon"]
            elif best["dungeon"] == "De Other Side":
                dos_best = best["dungeon"]

        # alternate dungeon data
        alt, nw_alt, sd_alt, halls_alt, plaguefall_alt, mists_alt, spires_alt, top_alt, dos_alt = request_json['mythic_plus_alternate_runs'], None, None, None, None, None, None, None, None
        for dungeon in alt:
            if alt["dungeon"] == "The Necrotic Wake":
                nw_alt = alt["dungeon"]
            elif alt["dungeon"] == "Sanguine Depths":
                sd_alt = alt["dungeon"]
            elif alt["dungeon"] == "Spires of Ascension":
                spires_alt = alt["dungeon"]
            elif alt["dungeon"] == "Mists of Tirna Scithe":
                mists_alt = alt["dungeon"]
            elif alt["dungeon"] == "Halls of Atonement":
                halls_alt = alt["dungeon"]
            elif alt["dungeon"] == "Plaguefall":
                pf_alt = alt["dungeon"]
            elif alt["dungeon"] == "Theatre of Pain":
                top_alt = alt["dungeon"]
            elif alt["dungeon"] == "De Other Side":
                dos_alt = alt["dungeon"]

        character_embed = discord.Embed(title=f"{character_name}'s Raider.IO Profile", url=f"https://raider.io/characters/{realm}/{server}/{character_name}", 
            description="", color=discord.Color.blue()) # TODO: pair color with spec (shaman is blue, etc...)

        character_embed.set_author(name=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        character_embed.add_field(name="Overall Statistics", value=f"**Total Score: {char_total_score}**\n", inline=False)
                                                                   # f"Tank Score: 0\n" +
                                                                   # f"Healer Score: 0\n" +
                                                                   # f"DPS Score: 0", inline=False)

        character_embed.add_field(name="Rankings", value=f"{char_spec} {char_class} Rank: Realm #{char_spec_rank['realm']}, Region #{char_spec_rank['region']}, World #{char_spec_rank['world']}\n" +
                                                         f"Overall {char_class} Rank: Realm #{char_class_rank['realm']}, Region #{char_class_rank['region']}, World #{char_class_rank['world']}\n" +
                                                         f"Overall {char_role} Rank: Realm #{char_role_rank['realm']}, Region #{char_role_rank['region']}, World #{char_role_rank['world']}", inline=False)

        character_embed.add_field(name="**Best Dungeons**", value="\u200b", inline=False)

        character_embed.add_field(name="Dungeon Name", value="Mists of Tirna Scithe\nNW", inline=True)
        character_embed.add_field(name="Fortified", value="13\n15", inline=True)
        character_embed.add_field(name="Tyrannical", value="19\n11", inline=True)
        character_embed.add_field(name="Total Score", value="232.4\n101.3", inline=True)

        await ctx.send(embed=character_embed)

def setup(bot_client):
    bot_client.add_cog(Individuals(bot_client))
