from typing import Optional, List, Union, Dict
from copy import copy

from _game.base.functionality import roll_dice, empty_set_or_set_of_dataclasses, \
    emtpy_list_or_list_of_dataclasses
from _game.base.stats_abilities_and_settings import Abilities, Skills, AbilityScoreTracker, SkillScoreTracker, \
    DamageType, WeaponType, WeaponProperties, Size
from _game.base.weapons import BaseWeapon
from _game.entities.base.action import Action, ActionType
from _game.entities.base.entity import HitPointTracker, BattleTrackerMetaData, Entity


class Enemy(Entity):

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
