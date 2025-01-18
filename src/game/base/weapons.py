from typing import Union, List

from game.base.functionality import empty_set_or_set_of_dataclasses
from game.base.stats_abilities_and_settings import Abilities, DamageType, AbilityScoreTracker, WeaponType, \
    WeaponProperties


class BaseWeapon:
    def __init__(self,
                 name: str,
                 weapon_type: WeaponType,
                 damage_dice: str,
                 damage_type: Union[DamageType, str],
                 properties: Union[List[WeaponProperties], WeaponProperties] = None,
                 magic_bonus: int = 0,
                 modifier: Union[List[Abilities], Abilities] = None,
                 range: int = None,
                 range_disadvantage: int = None,
                 two_handed_damage_dice: str = None,
                 cost: int = None,
                 weight: int = None):
        """
        Initialize a weapon.

        :param name: Name of the weapon
        :param damage_dice: Dice rolls in Format "1d8 + 3" or "10" or "d10" or "6d8"
        :param damage_type: DamageType enum value
        :param magic_bonus: Magic bonus to attack and damage rolls
        :param modifier: Ability modifier for weapon.
        """
        self.name = name
        self.weapon_type = weapon_type
        self.damage_dice = damage_dice
        self.damage_type = damage_type if isinstance(damage_type, DamageType) else DamageType(damage_type)
        self.properties = empty_set_or_set_of_dataclasses(properties)
        self.magic_bonus = magic_bonus
        self.modifier = empty_set_or_set_of_dataclasses(modifier)
        self.two_handed_damage_dice = two_handed_damage_dice if two_handed_damage_dice is not None else damage_dice

        self.range = range
        self.range_disadvantage = range_disadvantage

        self.cost = cost
        self.weight = weight

        self.description_short = self._describe('short')

        if WeaponProperties.FINESSE in self.properties:
            self.modifier.add(Abilities.STRENGTH)
            self.modifier.add(Abilities.DEXTERITY)

    def get_damage_type(self):
        """
        Get the weapon's damage type.

        :return: The weapon's damage type
        """
        return self.damage_type

    def _describe(self, length: str) -> str:
        if length == 'short':
            description = (
                f"{self.name}, "
                f"{self.weapon_type.name}, "
                f"{self.damage_type.name}, "
                f"{self.damage_dice}, "
                f"{[mod.name for mod in self.modifier]!r}, "
                f"Magic: {self.magic_bonus}, "
                f"{[prop.name for prop in self.properties]!r}"
            )
        else:
            raise ValueError(f"Description length '{length}' not implemented.")
        return description

class Weapons:
    all_weapons = {
        'Greatsword': 'greatsword',
        'Dagger': 'dagger'
    }

    greatsword = BaseWeapon(
        name ='Greatsword',
        weapon_type=WeaponType.MARTIAL,
        damage_dice='2d6',
        damage_type=DamageType.SLASHING,
        properties=[
            WeaponProperties.HEAVY,
            WeaponProperties.TWO_HANDED
        ],
        magic_bonus=0,
        modifier=Abilities.STRENGTH,
        two_handed_damage_dice=None,
        cost=50,
        weight=6
    )

    dagger = BaseWeapon(
        name='Dagger',
        weapon_type=WeaponType.SIMPLE,
        damage_dice='1d4',
        damage_type=DamageType.PIERCING,
        properties=[
            WeaponProperties.FINESSE,
            WeaponProperties.LIGHT,
            WeaponProperties.RANGE,
            WeaponProperties.THROWN
        ],
        range=20,
        range_disadvantage=60,
        weight=1
    )

    @staticmethod
    def get_weapon(weapon_name):
        if weapon_name in Weapons.all_weapons.values():
            return getattr(Weapons, weapon_name)
        elif weapon_name in Weapons.all_weapons:
            return getattr(Weapons, Weapons.all_weapons[weapon_name])
        raise ValueError(f"Unknown weapon '{Weapons.all_weapons}'")

