import discord
import requests
import os
import json

from . import constants
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
    async def score(self, ctx, *args):
        """
        Sends out the score of the player
        """

        region, realm, character_name = "", "", ""
        api_fields = constants.API_FIELDS

        if len(args) == 0:
            if os.path.isfile("./data/setcharacters.json"):
                with open('./data/setcharacters.json', 'r') as f:
                    setcharacters_json = json.load(f)

                    if not str(ctx.message.author.id) in setcharacters_json.keys():
                        await ctx.send(f'You have not yet set a character to your discord account. To do so, type `~setcharacter <character>`')
                        return

                    region = setcharacters_json[str(ctx.message.author.id)]['region']
                    realm = setcharacters_json[str(ctx.message.author.id)]['realm']
                    character_name = setcharacters_json[str(ctx.message.author.id)]['character_name']
            else:
                await ctx.send(f'You have not yet set a character to your discord account. To do so, type `~setcharacter <character>`')
                return
        elif len(args) >= 1:
            try:
                assert len(args) <= 1, "`score` command must follow format `~score <character>`!"
            except AssertionError:
                await ctx.send("`score` command must follow format `~score <character>`!")
                raise
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
            assert r.status_code != 400, f"character `{character_name}` from `{realm}` does not exist, perhaps you misspelled?"
        except AssertionError:
            await ctx.send(f"character `{character_name}` from `{realm}` does not exist, perhaps you misspelled?")
            raise

        request_json = r.json()

        # Processing the data

        # character data
        char_role = self._convert_role(request_json['active_spec_role'])
        char_class = request_json['class']
        char_spec = request_json['active_spec_name']
        char_thumbnail = request_json['thumbnail_url']

        # scores data
        char_total_score = request_json['mythic_plus_scores']['all']
        char_role_score = request_json['mythic_plus_scores'][char_role]
        char_spec_score = request_json['mythic_plus_scores'][f'spec_{constants.spec_ids[char_class][char_spec]["id"]}']

        # rank data
        char_role_rank = request_json['mythic_plus_ranks'][char_role]
        char_class_rank = request_json['mythic_plus_ranks']['class']
        char_spec_rank = request_json['mythic_plus_ranks'][f'spec_{constants.spec_ids[char_class][char_spec]["uid"]}']

        # TODO: de-duplicate dungeon data code

        # individual dungeon data
        best, nw_best, sd_best, halls_best, plaguefall_best, mists_best, spires_best, top_best, dos_best = request_json['mythic_plus_best_runs'], None, None, None, None, None, None, None, None
        for dungeon in best:
            if dungeon["dungeon"] == "The Necrotic Wake":
                nw_best = dungeon
            elif dungeon["dungeon"] == "Sanguine Depths":
                sd_best = dungeon
            elif dungeon["dungeon"] == "Spires of Ascension":
                spires_best = dungeon
            elif dungeon["dungeon"] == "Mists of Tirna Scithe":
                mists_best = dungeon
            elif dungeon["dungeon"] == "Halls of Atonement":
                halls_best = dungeon
            elif dungeon["dungeon"] == "Plaguefall":
                pf_best = dungeon
            elif dungeon["dungeon"] == "Theater of Pain":
                top_best = dungeon
            elif dungeon["dungeon"] == "De Other Side":
                dos_best = dungeon

        # alternate dungeon data
        alt, nw_alt, sd_alt, halls_alt, plaguefall_alt, mists_alt, spires_alt, top_alt, dos_alt = request_json['mythic_plus_alternate_runs'], None, None, None, None, None, None, None, None
        for dungeon in alt:
            if dungeon["dungeon"] == "The Necrotic Wake":
                nw_alt = dungeon
            elif dungeon["dungeon"] == "Sanguine Depths":
                sd_alt = dungeon
            elif dungeon["dungeon"] == "Spires of Ascension":
                spires_alt = dungeon
            elif dungeon["dungeon"] == "Mists of Tirna Scithe":
                mists_alt = dungeon
            elif dungeon["dungeon"] == "Halls of Atonement":
                halls_alt = dungeon
            elif dungeon["dungeon"] == "Plaguefall":
                pf_alt = dungeon
            elif dungeon["dungeon"] == "Theater of Pain":
                top_alt = dungeon
            elif dungeon["dungeon"] == "De Other Side":
                dos_alt = dungeon

        character_embed = discord.Embed(title=f"{character_name}'s Raider.IO Profile", url=f"https://raider.io/characters/{region}/{realm}/{character_name}", 
            description="", color=discord.Color.blue()) # TODO: pair color with spec (shaman is blue, etc...)

        character_embed.set_author(name=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        character_embed.set_thumbnail(url=char_thumbnail)

        character_embed.add_field(name="Overall Statistics", value=f"**Total Score: {char_total_score}**\n", inline=False)
                                                                   # f"Tank Score: 0\n" +
                                                                   # f"Healer Score: 0\n" +
                                                                   # f"DPS Score: 0", inline=False)

        character_embed.add_field(name="Rankings", value=f"**{char_spec} {char_class}** Rank: Realm **#{char_spec_rank['realm']}**, Region **#{char_spec_rank['region']}**, World **#{char_spec_rank['world']}**\n" +
                                                         f"Overall **{char_class}** Rank: Realm **#{char_class_rank['realm']}**, Region **#{char_class_rank['region']}**, World **#{char_class_rank['world']}**\n" +
                                                         f"Overall **{char_role}** Rank: Realm **#{char_role_rank['realm']}**, Region **#{char_role_rank['region']}**, World **#{char_role_rank['world']}**", inline=False)

        # TODO: generalize this code with for loop and add cases for None best dungeons
        character_embed.add_field(name="Best Dungeons", value=f"De Other Side - **{'+' * dos_best['num_keystone_upgrades']}{dos_best['mythic_level']}** {dos_best['affixes'][0]['name']}, Score: **{dos_best['score']:.1f}**\n" +
                                                                  f"Halls of Atonement - **{'+' * halls_best['num_keystone_upgrades']}{halls_best['mythic_level']}** {halls_best['affixes'][0]['name']}, Score: **{halls_best['score']:.1f}**\n" +
                                                                  f"Mists of Tirna Scithe - **{'+' * mists_best['num_keystone_upgrades']}{mists_best['mythic_level']}** {mists_best['affixes'][0]['name']}, Score: **{mists_best['score']:.1f}**\n" +
                                                                  f"Necrotic Wake - **{'+' * nw_best['num_keystone_upgrades']}{nw_best['mythic_level']}** {nw_best['affixes'][0]['name']}, Score: **{nw_best['score']:.1f}**\n" +
                                                                  f"Plaguefall - **{'+' * pf_best['num_keystone_upgrades']}{pf_best['mythic_level']}** {pf_best['affixes'][0]['name']}, Score: **{pf_best['score']:.1f}**\n" +
                                                                  f"Sanguine Depths - **{'+' * sd_best['num_keystone_upgrades']}{sd_best['mythic_level']}** {sd_best['affixes'][0]['name']}, Score: **{sd_best['score']:.1f}**\n" +
                                                                  f"Spires of Ascension - **{'+' * spires_best['num_keystone_upgrades']}{spires_best['mythic_level']}** {spires_best['affixes'][0]['name']}, Score: **{spires_best['score']:.1f}**\n" +
                                                                  f"Theater of Pain - **{'+' * top_best['num_keystone_upgrades']}{top_best['mythic_level']}** {top_best['affixes'][0]['name']}, Score: **{top_best['score']:.1f}**\n", inline=False)

        await ctx.send(embed=character_embed)

    @commands.command()
    async def setcharacter(self, ctx, *, args):
        """
        Sets a default character for the discord user
        """

        api_fields = constants.API_FIELDS

        if args == "":
            try:
                assert args != "", "`<character>` field must not be empty`!"
            except AssertionError:
                await ctx.send("`<character>` field must not be empty`!")
                raise
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

        if not os.path.isfile("./data/setcharacters.json"):
            print("Required file setcharacters.json does not exist, creating one now")
            
            with open('./data/setcharacters.json', 'a') as dumpfile:
                json.dump(constants.DEFAULT_SETCHARACTERS_JSON, dumpfile, indent=4)

        with open('./data/setcharacters.json', 'r') as f:
            setcharacters_json = json.load(f)

        if str(ctx.message.author.id) in setcharacters_json.keys():
            await ctx.send(f'Character `{setcharacters_json[str(ctx.message.author.id)]["character_name"]}` was previously set to this account. Overriding it...')
        
        with open('./apiurl.txt', 'r') as f:
            api_url = constants.API_URL
            api_url = api_url.replace("{}", region, 1)
            api_url = api_url.replace("{}", realm, 1)
            api_url = api_url.replace("{}", character_name, 1)
            api_url = api_url.replace("{}", '%2C'.join(api_fields))

        r = requests.get(api_url)

        try:
            assert r.status_code != 400, f"character `{character_name}` from `{realm}` does not exist, perhaps you misspelled?"
        except AssertionError:
            await ctx.send(f"character `{character_name}` from `{realm}` does not exist, perhaps you misspelled?")
            raise
        
        setcharacters_json[str(ctx.message.author.id)] = {'region': character_split[0], 'realm': character_split[1], 'character_name': character_split[2]}
        with open('./data/setcharacters.json', 'w') as f:
            json.dump(setcharacters_json, f)
        await ctx.send(f'{ctx.message.author.mention}, character `{character_split[2]}` is now being tracked.')


def setup(bot_client):
    bot_client.add_cog(Individuals(bot_client))
