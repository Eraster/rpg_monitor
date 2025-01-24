from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Union, List, Set, Any
from copy import deepcopy
from xml.dom.minidom import Entity
from abc import ABC, abstractmethod

from _game.base.stats_abilities_and_settings import DamageType, WeaponProperties
from _game.base.functionality import RollInfo
from _game.base.weapons import Weapons, BaseWeapon
from _game.base.functionality import roll_dice, RollInfo

class ActionType(Enum):
    ENVIRONMENT_ACTION_PICK_UP_WEAPON = auto()
    WEAPON_ATTACK_MELEE = auto()
    WEAPON_ATTACK_RANGED = auto()
    WEAPON_ATTACK_THROW = auto()

class TargetType(Enum):
    ENTITY = auto()
    ENVIRONMENT_WEAPON = auto()

@dataclass
class Action(ABC):
    battle_tracker_turn: int = None
    battle_tracker_round: int = None

    action_type: ActionType = 0
    bonus_action: bool = False

    source: Entity = None
    allowed_target_types: Union[List[TargetType], TargetType] = None
    target: Optional[Any] = None
    target_type: Optional[TargetType] = None

    primed: bool = False
    success: bool = None
    executed: bool = False

    action_info: str = field(default_factory=list)

    @abstractmethod
    def description_prior(self) -> str:
        pass

    @abstractmethod
    def description_primed(self) -> str:
        pass

    @abstractmethod
    def description_executed(self) -> str:
        pass

@dataclass
class EnvironmentAction(Action):
    weapon: BaseWeapon = None

    def description_prior(self) -> str:
        if self.action_type == ActionType.ENVIRONMENT_ACTION_PICK_UP_WEAPON:
            return "Environment: Pick up Weapon"
        raise NotImplementedError()

    def description_primed(self) -> str:
        if self.action_type == ActionType.ENVIRONMENT_ACTION_PICK_UP_WEAPON:
            if self.target is None:
                ret = f"Environment: No weapon selected for pick up."
            else:
                ret = f"Environment: Pick up {self.target[1]} from Location {self.target[0]}"
            return ret
        raise NotImplementedError()

    def description_executed(self) -> str:
        if self.action_type.ENVIRONMENT_ACTION_PICK_UP_WEAPON:
            if self.target is None:
                ret = f"Environment: Picked up nothing from nowhere. Select a weapon first you dingus."
            else:
                ret = f"Environment: Picked up {self.target[1]} from Location {self.target[0]}"
            return ret
        raise NotImplementedError()


@dataclass
class WeaponAttackAction(Action):
    """
    Class for Action transfers and evaluation between entities (players, monsters)
    """
    advantage: bool = False
    disadvantage: bool = False
    applied_ac_advantage_disadvantage: bool = False
    ac_dice_notation: str = None
    ac_roll: Optional[RollInfo] = None
    ac_secondary_roll: Optional[RollInfo] = None
    crit_roll: bool = False

    source_roll_dice_notation: str = None
    source_roll: Optional[RollInfo] = None

    magic: bool = None
    magic_damage: int = 0
    damage_type: DamageType = None
    resistance_applied: bool = None
    immunity_applied: bool = None
    
    ranged_attack: bool = False
    attack_distance: int = None
    range: int = None
    range_disadvantage: int = None

    weapon: BaseWeapon = None
    two_handed_attack: bool = False

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
            self.success = False
        else:
            self.success = True

    def apply_resistance_and_immunity(self, resistances: Set[DamageType] = None, immunities: Set[DamageType] = None):
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

    def apply_environment_effects(self):
        # Apply range disadvantage
        if self.ranged_attack:

            if self.source.battle_data.enemy_in_melee_range:
                self.disadvantage = True

            if self.attack_distance is None:
                self.attack_distance = abs(self.source.battle_data.location - self.target.battle_data.location)

            if self.attack_distance > self.range_disadvantage:
                self.success = False
            elif self.attack_distance > self.range:
                self.disadvantage = True

    def set_attack_distance(self, distance: int):
        self.attack_distance = distance

    def __copy__(self):
        copy = deepcopy(self)

        copy.source = self.source
        copy.target = self.target

        copy.weapon = self.weapon

        return copy

    def description_prior(self) -> str:
        if self.action_type in {ActionType.WEAPON_ATTACK_MELEE,
                                ActionType.WEAPON_ATTACK_RANGED,
                                ActionType.WEAPON_ATTACK_THROW}:
            ret = f"{self.action_type.name}"
            if self.weapon:
                ret += f", {self.weapon.name}"
            ret += f", Attack: {self.ac_dice_notation}"
            ret += f", Damage: {self.source_roll_dice_notation}"
            ret += f", {self.damage_type.name}"
            ret += f", Range ({self.range}/{self.range_disadvantage})" if self.ranged_attack else ""
            ret += ", magical" if self.magic else ""
            return ret
        raise NotImplementedError()

    def description_primed(self) -> str:
        if self.action_type in {ActionType.WEAPON_ATTACK_MELEE,
                                ActionType.WEAPON_ATTACK_RANGED,
                                ActionType.WEAPON_ATTACK_THROW}:
            ret = f"{'CRIT ' if self.crit_roll else ''}SUCCESS" if self.success else "FAILED"
            ret += f", AC: {self.ac_roll.total_roll}"
            ret += f", Damage: {self.source_roll.total_roll} ({self.source_roll.dice_notation})"
            ret += f", {self.damage_type.name}"
            ret += (f", Attacked at range {self.attack_distance} "
                    f"({self.range}/{self.range_disadvantage})") if self.ranged_attack else ""
            ret += ", magical" if self.magic else ""
            ret += ", RESISTANCE" if self.resistance_applied and not self.immunity_applied else ""
            ret += ", IMMUNITY" if self.immunity_applied else ""
            ret += ", ".join(self.action_info) if self.action_info is not None else ""
            return ret
        raise NotImplementedError()


    def description_executed(self) -> str:
        if self.action_type in {ActionType.WEAPON_ATTACK_MELEE,
                                ActionType.WEAPON_ATTACK_RANGED,
                                ActionType.WEAPON_ATTACK_THROW}:
            ret = f"Turn {self.battle_tracker_turn}, Round {self.battle_tracker_round}"
            ret += f", {self.action_type.name}"
            if self.action_type in {ActionType.WEAPON_ATTACK_MELEE,
                                    ActionType.WEAPON_ATTACK_RANGED,
                                    ActionType.WEAPON_ATTACK_THROW}:
                ret += f", Crit {self.crit_roll}"
                if not self.success:
                    ret += f", FAILED Attack roll {self.ac_roll.total_roll} not sufficient"
                else:
                    ret += f", SUCCESS ({self.ac_roll.total_roll}), {self.source_roll.description()})"
                    if self.immunity_applied:
                        ret += f", Immunity applied"
                    elif self.resistance_applied:
                        ret += f", Resistance applied"
                    ret += f", {self.damage_type}"
            return ret
        raise NotImplementedError()


