from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Union, List, Set
from copy import deepcopy

from game.base.stats_abilities_and_settings import DamageType, WeaponProperties
from game.base.functionality import RollInfo
from game.base.weapons import Weapons, BaseWeapon
from game.base.functionality import roll_dice, RollInfo

class ActionType(Enum):
    WEAPON_ATTACK_MELEE = auto()
    WEAPON_ATTACK_RANGED = auto()
    WEAPON_ATTACK_THROW = auto()

@dataclass
class Action:
    """
    Class for Action transfers and evaluation between entities (players, monsters)
    """

    battle_tracker_turn: int = None
    battle_tracker_round: int = None

    bonus_action: bool = False
    action_type: ActionType = 0

    advantage: bool = False
    disadvantage: bool = False
    applied_ac_advantage_disadvantage: bool = False
    ac_dice_notation: str = None
    ac_roll: Optional[RollInfo] = None
    ac_secondary_roll: Optional[RollInfo] = None
    crit_roll: bool = False

    source: Union['Player', 'Enemy'] = None
    target: Optional[Union['Player', 'Enemy', List[Union['Player', 'Enemy']]]] = None
    success: bool = None

    source_roll_dice_notation: str = None
    source_roll: Optional[RollInfo] = None
    target_roll: Optional[RollInfo] = None

    magic: bool = None
    magic_damage: int = 0
    damage_type: DamageType = None
    resistance_applied: bool = None
    immunity_applied: bool = None
    
    ranged_attack: bool = False
    attack_distance: int = None
    range: int = None
    range_disadvantage: int = None

    # SpecialConditions
    # Possibly moved to separate state class which could be imported from entity.
    weapon: BaseWeapon = None
    two_handed_attack: bool = False

    action_info: str = "INFO"

    def roll_ac(self):
        if self.ac_dice_notation is None:
            raise ValueError(f"ac_dice_notation must be defined.\n"
                             f"Delivered: {self.ac_dice_notation}")

        roll_1 = roll_dice(self.ac_dice_notation)
        if (self.disadvantage or self.advantage) and not (self.disadvantage and self.advantage):
            roll_2 = roll_dice(self.ac_dice_notation)
            ac_low, ac_high = sorted([roll_1, roll_2], key=lambda x: x.total_roll)

            self.applied_ac_advantage_disadvantage = True
            if self.disadvantage:
                self.ac_roll, self.ac_secondary_roll = ac_low, ac_high
            else:
                self.ac_roll, self.ac_secondary_roll = ac_high, ac_low
        else:
            self.applied_ac_advantage_disadvantage = False
            self.ac_roll = roll_1

        self.crit_roll = self.ac_roll.all_rolls[20][0] == 20

    def roll_source(self):
        self.source_roll = roll_dice(self.source_roll_dice_notation, double_dice=self.crit_roll)

    def check_attack_success(self, defender_ac: int):
        if self.success is not None:
            return

        if self.ac_roll.total_roll < defender_ac and not self.crit_roll:
            self.success = True
        else:
            self.success = False

    def apply_resistance_and_immunity(self, resistances: Set[DamageType] = None, immunities: Set[DamageType] = None):
        if self.target_roll is not None:
            raise NotImplementedError(f"Target rolls (i.e. spell damage) not yet implemented.")

        if self.resistance_applied is not None:
            raise ValueError(f"Cannot apply resistance twice. Delivered {self.resistance_applied}")
        if self.immunity_applied is not None:
            raise ValueError(f"Cannot apply immunity twice. Delivered {self.immunity_applied}")

        if self.damage_type in resistances:
            self.source_roll.total_roll = self.source_roll.total_roll // 2
            self.resistance_applied = True
        else:
            self.resistance_applied = False

        if self.damage_type in immunities:
            self.source_roll.total_roll = 0
            self.immunity_applied = True
        else:
            self.immunity_applied = False


    def description_prior(self) -> str:
        if self.action_type in {
            ActionType.WEAPON_ATTACK_MELEE,
            ActionType.WEAPON_ATTACK_RANGED,
            ActionType.WEAPON_ATTACK_THROW
        }:
            return f"{self.action_type}" + self.weapon.description_short + (
                f"{', advantage' if self.advantage and not self.disadvantage else ''}"
                f"{', disadvantage' if self.disadvantage and not self.advantage else ''}"
                f", AC: {self.ac_dice_notation}"
                f"{f', Range ({self.range}/{self.range_disadvantage})' if self.ranged_attack else ''}"
            )
        else:
            raise ValueError(f"{self.action_type} has not implemented description.")

    def description_after(self) -> str:
        ret = f"Turn {self.battle_tracker_turn}, Round {self.battle_tracker_round}"
        ret += f", {self.action_type.name}"
        if self.action_type == ActionType.WEAPON_ATTACK_MELEE:
            ret += f", Crit {self.crit_roll}"
            if not self.success:
                ret += f", FAILED Attack roll {self.ac_roll} not sufficient"
            else:
                ret += f", SUCCESS, {self.source_roll.description()})"
                if self.immunity_applied:
                    ret += f", Immunity applied"
                elif self.resistance_applied:
                    ret += f", Resistance applied"
                ret += f", {self.damage_type}"
        return ret

    def apply_environment_effects(self):
        # Apply range disadvantage
        if self.ranged_attack:
            if self.attack_distance is None:
                self.attack_distance = abs(self.source.battle_data.location - self.target.battle_data.location)

            if self.attack_distance > self.range_disadvantage:
                self.success = False
            elif self.attack_distance > self.range:
                self.disadvantage = True

            if self.source.battle_data.enemy_in_melee_range:
                self.disadvantage = True

    def set_attack_distance(self, distance: int):
        self.attack_distance = distance

    def __copy__(self):
        copy = deepcopy(self)

        copy.source = self.source
        copy.target = self.target

        copy.weapon = self.weapon

        return copy
