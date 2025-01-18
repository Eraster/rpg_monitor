from typing import Union, Optional, List

from game.entities.base.entity import Entity, HitPointTracker
from game.base.stats_abilities_and_settings import Skills, Abilities, WeaponType, DamageType, Size

class Player(Entity):

    def __init__(self,
                 race: str,
                 armor_class: int,
                 hit_points: Union[int, HitPointTracker],
                 size: Size,
                 speed: int,
                 strength: int,
                 dexterity: int,
                 constitution: int,
                 intelligence: int,
                 wisdom: int,
                 charisma: int,
                 proficiencies: Optional[List[Union[Skills, Abilities, WeaponType]]],
                 proficiency_bonus: int,
                 name: str = None,
                 damage_resistances: Optional[Union[List[DamageType], DamageType]] = None,
                 damage_immunities: Optional[Union[List[DamageType], DamageType]] = None,
                 roll_for_stats=False,
                 weapons: List[WeaponType] = None):
        super().__init__(
            race=race,
            armor_class=armor_class,
            hit_points=hit_points,
            size=size,
            speed=speed,
            strength=strength,
            dexterity=dexterity,
            constitution=constitution,
            intelligence=intelligence,
            wisdom=wisdom,
            charisma=charisma,
            proficiencies=proficiencies,
            proficiency_bonus=proficiency_bonus,
            name=name,
            damage_resistances=damage_resistances,
            damage_immunities=damage_immunities,
            roll_for_stats=roll_for_stats,
            weapons=weapons
        )
