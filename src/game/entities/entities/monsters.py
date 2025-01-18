from game.entities.base.enemy_base_sheet import Enemy, Skills
from game.entities.base.entity import HitPointTracker
from game.base.weapons import Weapons
from game.base.stats_abilities_and_settings import Size

GOBLIN = Enemy(
    race='Goblin',
    name='NoName',
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

ALL_MONSTERS = {
    'Goblin': GOBLIN
}
