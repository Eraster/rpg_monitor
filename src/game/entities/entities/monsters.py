import random

from game.entities.base.enemy_base_sheet import Enemy, Skills
from game.entities.base.entity import HitPointTracker
from game.base.weapons import Weapons
from game.base.stats_abilities_and_settings import Size

name_set = {
    "Bowelclaw", "Grimeby", "Horbug", "Mudmuncher", "Bloodspike", "Thornfist",
    "Shatteredtooth", "Wretchedfang", "Darkblight", "Cinderlash", "Rotwing",
    "Sludgebelly", "Vilehorn", "Goregrip", "Nightgash", "Foulflame", "Tornwretch",
    "Skullrend", "Grubmonger", "Ashbloom", "Ironhowl", "Ruinmaw", "Doomthorn",
    "Flareclaw", "Banegrip", "Frostbite", "Vilecrash", "Stagblade", "Ragehowler",
    "Blightreaver", "Swampfury", "Dreadwretch", "Murkclaw", "Miasmaflame", "Ironwrath",
    "Pestilentwhip", "Bloodfang", "Stormgore", "Scumgrip", "Gloomfang", "Frostmaul",
    "Doomspike", "Bonegrip", "Ghoulfang", "Ironrend", "Clawbane", "Gravespike",
    "Witchthorn", "Maggotlash", "Stormclaw", "Bloodwrack", "Fiendhowl", "Rotgore",
    "Wailfang", "Stonebite", "Fleshspike", "Bonecrash", "Frostthroat", "Ashvile",
    "Skullmonger", "Doomripper", "Scourgedread", "Blackthorn", "Ragetooth",
    "Sinewgrip", "Ashclaw", "Dreadmonger", "Fleshroot", "Ironbite", "Voidflame",
    "Ravencinder", "Grubclaw", "Rotscorch", "Frostvile", "Darkrend", "Ashthorn",
    "Cinderbite", "Nightshard", "Grimmaw", "Slagthorn", "Bloodflesh", "Frostroot",
    "Venomspike", "Ravengloom", "Mireclaw", "Gloomfang", "Blightclaw", "Raggedthorn",
    "Gashclaw", "Bitterfang", "Doomraven", "Searflame", "Rotgrip", "Nightbloom",
    "Witchbite", "Venomsplinter", "Grimclaw", "Stormgrip", "Slaughterspike",
    "Spinemaw", "Shiverbone", "Blightroot", "Ironfang", "Gravetusk", "Swampflesh",
    "Gorefang", "Cinderblight", "Rageclaw", "Hungermaw", "Frostwretch",
    "Scornedhowl", "Ashbone", "Grimwretch", "Vileclaw", "Bloodcurse",
    "Tearwing", "Gravescorch", "Thorncrusher", "Verminfang", "Blightbane",
    "Mournshade", "Ravageclaw", "Bitterlash", "Mudfang", "Rotmourn",
    "Wretchedhowl", "Seargrip", "Cinderbloom", "Grimshard", "Miasmablade",
    "Hellscrape", "Grimthorn", "Scourgerip", "Vilehowl", "Searclaw",
    "Blightflesh", "Hollowfang", "Murkcrash", "Dreadlash", "Rotspike",
    "Searmonger", "Gloommaw", "Vilemaul", "Doomcrush", "Fleshspore",
    "Thornbite", "Frostgore", "Vampiriclash", "Mudmash", "Ragefang",
    "Frenzyfang", "Shadowscorch", "Dreadroot", "Witchgore", "Bloodrazor",
    "Venomlash", "Gravebite", "Fleshgrip", "Skullfury", "Frostwhip",
    "Vilefang", "Wrathclaw", "Soulrender", "Bloodgrip", "Horrorscorch",
    "Stormmonger", "Blightroot", "Nightgrip", "Cinderscorch", "Fleshflame",
    "Scourgerend", "Vilehowler", "Dreadbite", "Gloomthorn", "Ashclash",
    "Thornsplitter", "Nightwhip", "Bloodlash", "Rageflame", "Fiendbite",
    "Rotstorm", "Doomlash", "Slimeclaw", "Venomhowl", "Frostbone",
    "Nightspike", "Ashfiend", "Gravegrip", "Blightblade", "Cinderfang",
    "Hollowscorch", "Gravenight", "Venomlash", "Grimraven", "Goreclaw",
    "Witchflame", "Doomshade", "Cinderwhip", "Rotclaw", "Frostfang",
    "Nightmaw", "Darkfang", "Gloomclaw", "Ravenspike", "Bloodbloom",
    "Fleshthorn", "Gravescorch", "Grimroot", "Doomflame", "Scourgehowl",
    "Rotbloom", "Mireclaw", "Frostlash", "Searfang", "Ashmaw", "Venomslice",
    "Gorebloom", "Blightroot", "Nightmonger", "Searmash", "Vilecrusher"
}

def random_name_pick():
    return random.choice(list(name_set))

class PredefinedMonsters:
    GOBLIN = Enemy(
        race='Goblin',
        armor_class=13,
        hit_points=HitPointTracker(
            rule_default=7,
            rule_rolls='2d6'
        ),
        size=Size.SMALL,
        speed=30,
        strength=8,
        dexterity=14,
        constitution=10,
        intelligence=10,
        wisdom=8,
        charisma=8,
        proficiencies=[Skills.STEALTH],
        proficiency_bonus=2,
        weapons=Weapons.dagger
    )

    TROLL = Enemy(
        race='Troll',
        armor_class=15,
        hit_points=HitPointTracker(
            rule_default=84,
            rule_rolls='8d10 + 40'
        ),
        size=Size.LARGE,
        speed=30,
        strength=18,
        dexterity=13,
        constitution=20,
        intelligence=7,
        wisdom=9,
        charisma=7,
        proficiencies=[Skills.PERCEPTION],
        proficiency_bonus=3,
        weapons=Weapons.claw
    )

    ORC = Enemy(
        race='Orc',
        armor_class=13,
        hit_points=HitPointTracker(
            rule_default=15,
            rule_rolls='2d8 + 6'
        ),
        size=Size.MEDIUM,
        speed=30,
        strength=16,
        dexterity=12,
        constitution=14,
        intelligence=8,
        wisdom=11,
        charisma=10,
        proficiencies=[Skills.INTIMIDATION],
        proficiency_bonus=2,
        weapons=Weapons.greataxe
    )

    DRAGON = Enemy(
        race='Dragon',
        armor_class=19,
        hit_points=HitPointTracker(
            rule_default=300,
            rule_rolls='20d12 + 120'
        ),
        size=Size.GARGANTUAN,
        speed=60,
        strength=23,
        dexterity=14,
        constitution=21,
        intelligence=16,
        wisdom=15,
        charisma=19,
        proficiencies=[Skills.PERCEPTION, Skills.PERSUASION],
        proficiency_bonus=6,
        weapons=Weapons.breath_weapon  # Can represent a fire/ice breath weapon
    )

    VAMPIRE = Enemy(
        race='Vampire',
        armor_class=16,
        hit_points=HitPointTracker(
            rule_default=112,
            rule_rolls='15d8 + 45'
        ),
        size=Size.MEDIUM,
        speed=30,
        strength=18,
        dexterity=18,
        constitution=16,
        intelligence=17,
        wisdom=14,
        charisma=18,
        proficiencies=[Skills.PERCEPTION, Skills.PERSUASION],
        proficiency_bonus=3,
        weapons=Weapons.bite  # Can represent vampire bite weapon
    )

    GHOUL = Enemy(
        race='Ghoul',
        armor_class=12,
        hit_points=HitPointTracker(
            rule_default=22,
            rule_rolls='4d6 + 4'
        ),
        size=Size.MEDIUM,
        speed=30,
        strength=13,
        dexterity=14,
        constitution=10,
        intelligence=6,
        wisdom=10,
        charisma=7,
        proficiencies=[Skills.PERCEPTION, Skills.STEALTH],
        proficiency_bonus=2,
        weapons=Weapons.claws
    )

    OGRE = Enemy(
        race='Ogre',
        armor_class=11,
        hit_points=HitPointTracker(
            rule_default=59,
            rule_rolls='6d10 + 24'
        ),
        size=Size.LARGE,
        speed=40,
        strength=19,
        dexterity=8,
        constitution=16,
        intelligence=5,
        wisdom=7,
        charisma=7,
        proficiencies=[Skills.ATHLETICS],
        proficiency_bonus=2,
        weapons=Weapons.greatclub
    )

    MIMIC = Enemy(
        race='Mimic',
        armor_class=12,
        hit_points=HitPointTracker(
            rule_default=58,
            rule_rolls='8d8 + 24'
        ),
        size=Size.MEDIUM,
        speed=30,
        strength=17,
        dexterity=13,
        constitution=14,
        intelligence=5,
        wisdom=12,
        charisma=8,
        proficiencies=[Skills.PERCEPTION],
        proficiency_bonus=2,
        weapons=Weapons.bite
    )

    BEHOLDER = Enemy(
        race='Beholder',
        armor_class=18,
        hit_points=HitPointTracker(
            rule_default=180,
            rule_rolls='18d10 + 72'
        ),
        size=Size.LARGE,
        speed=0,  # Beholders can float
        strength=10,
        dexterity=14,
        constitution=16,
        intelligence=17,
        wisdom=15,
        charisma=17,
        proficiencies=[Skills.PERCEPTION],
        proficiency_bonus=4,
        weapons=Weapons.eye_ray  # Can represent the different eye rays
    )

    ALL_MONSTERS = {
        'Beholder': BEHOLDER,
        'Dragon': DRAGON,
        'Ghoul': GHOUL,
        'Goblin': GOBLIN,
        'Mimic': MIMIC,
        'Ogre': OGRE,
        'Orc': ORC,
        'Troll': TROLL,
        'Vampire': VAMPIRE,
    }

    @staticmethod
    def get_monster(race: str = None):
        all_monsters = PredefinedMonsters.ALL_MONSTERS
        for monster in all_monsters.values():
            monster.name = random_name_pick()

        if race is not None:
            return all_monsters[race]
        else:
            return all_monsters

