from typing import Union, List

from _game.base.functionality import empty_set_or_set_of_dataclasses
from _game.base.stats_abilities_and_settings import Abilities, DamageType, AbilityScoreTracker, WeaponType, \
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
        'Bite': 'bite',
        'Breath Weapon': 'breath_weapon',
        'Claw': 'claw',
        'Claws': 'claws',
        'Eye Ray': 'eye_ray',
        'Greataxe': 'greataxe',
        'Greatclub': 'greatclub',
        'Greatsword': 'greatsword',
        'Dagger': 'dagger'
    }

    eye_ray = BaseWeapon(
        name='Eye Ray',
        weapon_type=WeaponType.EXOTIC,  # This would be considered an exotic or special weapon
        damage_dice='4d10',  # Eye rays can deal high damage (example: 4d10)
        damage_type=DamageType.FORCE,  # Eye rays are often force damage, but could be other types
        properties=[WeaponProperties.RANGE],  # Eye rays are ranged but not typical weapons
        magic_bonus=0,  # Eye rays might not have a magic bonus but you could adjust
        modifier=Abilities.INTELLIGENCE,  # Some creatures use Intelligence for their eye ray attacks
        two_handed_damage_dice=None,  # Not applicable
        cost=0,  # No cost, as this is an ability or natural weapon
        weight=0,
        range=30,
        range_disadvantage=30# Eye rays don't have weight
    )

    greatclub = BaseWeapon(
        name='Greatclub',
        weapon_type=WeaponType.MARTIAL,  # Martial weapon, suitable for strong characters
        damage_dice='1d8',  # Greatclubs deal 1d8 damage
        damage_type=DamageType.BLUDGEONING,  # Greatclubs deal bludgeoning damage
        properties=[WeaponProperties.HEAVY, WeaponProperties.TWO_HANDED],  # It is both heavy and requires two hands
        magic_bonus=0,
        modifier=Abilities.STRENGTH,  # Uses Strength for attack and damage rolls
        two_handed_damage_dice='1d10',  # Greatclub deals 1d10 damage when used two-handed
        cost=2,  # Greatclubs are relatively cheap
        weight=10  # A greatclub is quite heavy
    )

    claws = BaseWeapon(
        name='Claws',
        weapon_type=WeaponType.SIMPLE,  # This could be SIMPLE as it's a natural weapon
        damage_dice='1d4',  # Claws typically deal 1d4 damage
        damage_type=DamageType.SLASHING,  # Claws usually deal slashing damage
        properties=[WeaponProperties.FINESSE, WeaponProperties.LIGHT],  # Claws are light and finesse weapons
        magic_bonus=0,
        modifier=Abilities.STRENGTH,  # Could also use Dexterity if you treat it as a finesse weapon
        two_handed_damage_dice=None,  # Claws are usually one-handed
        cost=0,  # No cost for natural weapons
        weight=0.5  # Very light, as claws are natural weapons
    )

    bite = BaseWeapon(
        name='Bite',
        weapon_type=WeaponType.SIMPLE,  # This could be SIMPLE as it's often a natural weapon
        damage_dice='1d6',  # Bite typically deals 1d6 damage
        damage_type=DamageType.PIERCING,  # Bite damage is typically piercing
        properties=[WeaponProperties.FINESSE],  # Can use Dexterity (finesse)
        magic_bonus=0,
        modifier=Abilities.STRENGTH,  # You could modify it to Dexterity if you want it to be finesse
        two_handed_damage_dice=None,  # Not applicable for a bite
        cost=0,  # Natural weapon, so no cost
        weight=0  # Natural weapon with no weight
    )

    breath_weapon = BaseWeapon(
        name='Breath Weapon',
        weapon_type=WeaponType.EXOTIC,  # You can define this as EXOTIC or SPECIAL if it's a unique ability
        damage_dice='6d6',  # Example: Dragons often deal 6d6 damage with their breath weapon
        damage_type=DamageType.FIRE,  # This could be FIRE, ACID, COLD, etc. depending on the creature
        properties=[WeaponProperties.RANGE],  # Breath weapons typically have range but are not a typical weapon
        magic_bonus=0,
        modifier=Abilities.DEXTERITY,  # Some creatures use Constitution or another modifier for breath weapons
        two_handed_damage_dice=None,
        cost=0,  # No cost, as this is typically a natural ability
        weight=0,
        range=15,
        range_disadvantage=30# Breath weapon has no weight
    )

    greataxe = BaseWeapon(
        name='Greataxe',
        weapon_type=WeaponType.MARTIAL,
        damage_dice='1d12',
        damage_type=DamageType.SLASHING,
        properties=[
            WeaponProperties.HEAVY,
            WeaponProperties.TWO_HANDED
        ],
        magic_bonus=0,
        modifier=Abilities.STRENGTH,
        two_handed_damage_dice='2d12',  # Greataxe does more damage when used two-handed
        cost=30,
        weight=7
    )

    claw = BaseWeapon(
        name='Claw',
        weapon_type=WeaponType.MARTIAL,  # You can adjust this to SIMPLE if needed
        damage_dice='1d6',  # Assuming claws deal 1d6 damage
        damage_type=DamageType.SLASHING,  # Claws typically deal slashing damage
        properties=[
            WeaponProperties.FINESSE,  # Finesse because claws can be used with Dexterity
            WeaponProperties.LIGHT  # Claws are often light in nature
        ],
        magic_bonus=0,
        modifier=Abilities.STRENGTH,  # You can change it to Dexterity for finesse if needed
        two_handed_damage_dice=None,  # Not applicable as claws are typically single-handed
        cost=0,  # Claws are usually natural weapons, so they might be free or have no cost
        weight=0.5  # Assuming a light natural weapon like claws weighs very little
    )

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

