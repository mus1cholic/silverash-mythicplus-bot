API_URL = "https://raider.io/api/v1/characters/profile?region={}&realm={}&name={}&fields={}"
API_FIELDS = ['mythic_plus_scores', 'mythic_plus_ranks', 'mythic_plus_best_runs', 'mythic_plus_alternate_runs']

DEFAULT_SETCHARACTERS_JSON = {'example_discord_unique_id': {'region': 'us', 'realm': 'stormrage', 'character_name': 'sample_name'}}

spec_ids = {
	'Death Knight': {
		'Blood': {
			'id': 0,
			'uid': 250
		},
		'Frost': {
			'id': 1,
			'uid': 251
		},
		'Unholy': {
			'id': 2,
			'uid': 252
		}
	},
	'Demon Hunter': {
		'Havoc': {
			'id': 0,
			'uid': 577
		},
		'Vengeance': {
			'id': 1,
			'uid': 581
		}
	},
	'Druid': {
		'Balance': {
			'id': 0,
			'uid': 102
		},
		'Feral': {
			'id': 1,
			'uid': 103
		},
		'Guardian': {
			'id': 2,
			'uid': 104
		},
		'Restoration': {
			'id': 3,
			'uid': 105
		}
	},
	'Hunter': {
		'Beast Mastery': {
			'id': 0,
			'uid': 253
		},
		'Marksmanship': {
			'id': 1,
			'uid': 254
		},
		'Survival': {
			'id': 2,
			'uid': 255
		}
	},
	'Mage': {
		'Arcane': {
			'id': 0,
			'uid': 62
		},
		'Fire': {
			'id': 1,
			'uid': 63
		},
		'Frost': {
			'id': 2,
			'uid': 64
		}
	},
	'Monk': {
		'Brewmaster': {
			'id': 0,
			'uid': 268
		},
		'Windwalker': {
			'id': 1,
			'uid': 269
		},
		'Mistweaver': {
			'id': 2,
			'uid': 270
		}
	},
	'Paladin': {
		'Holy': {
			'id': 0,
			'uid': 65
		},
		'Protection': {
			'id': 1,
			'uid': 66
		},
		'Retribution': {
			'id': 2,
			'uid': 70
		}
	},
	'Priest': {
		'Discipline': {
			'id': 0,
			'uid': 256
		},
		'Holy': {
			'id': 1,
			'uid': 257
		},
		'Shadow': {
			'id': 2,
			'uid': 258
		}
	},
	'Rogue': {
		'Assassination': {
			'id': 0,
			'uid': 259
		},
		'Outlaw': {
			'id': 1,
			'uid': 260
		},
		'Subtlety': {
			'id': 2,
			'uid': 261
		}
	},
	'Shaman': {
		'Elemental': {
			'id': 0,
			'uid': 262
		},
		'Enhancement': {
			'id': 1,
			'uid': 263
		},
		'Restoration': {
			'id': 2,
			'uid': 264
		}
	},
	'Warlock': {
		'Affliction': {
			'id': 0,
			'uid': 265
		},
		'Demonology': {
			'id': 1,
			'uid': 266
		},
		'Destruction': {
			'id': 2,
			'uid': 267
		}
	},
	'Warrior': {
		'Arms': {
			'id': 0,
			'uid': 71
		},
		'Fury': {
			'id': 1,
			'uid': 72
		},
		'Protection': {
			'id': 2,
			'uid': 73
		}
	}
}