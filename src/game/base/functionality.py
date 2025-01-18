import random
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Dict

from game.base.stats_abilities_and_settings import DamageType


@dataclass
class RollInfo:
    total_roll: int = 0
    dice_notation: str = None
    all_rolls: Dict[int, list] = field(default_factory=lambda: defaultdict(list))

    def description(self) -> str:
        ret = f"Total: {self.total_roll}, Rolled: {self.dice_notation}"
        if self.all_rolls:
            ret += f", Rolls:"
            for dice, rolls in self.all_rolls.items():
                ret += f"  d{dice} [{', '.join([str(r) for r in rolls])}]"

        return ret


def roll_dice(dice_notation: str, double_dice: bool = False) -> RollInfo:
    # Regular expression to match each part of the dice roll (including multiple dice rolls and modifiers)

    roll = RollInfo()
    roll.dice_notation = dice_notation

    to_handle = ""
    to_roll = ""
    while dice_notation:
        dice_notation.strip()

        pre_string = dice_notation[0]
        dice_notation = dice_notation[1:]

        if pre_string.isdigit():
            to_handle += pre_string
        elif pre_string == "d":
            to_roll = to_handle if to_handle else 1
            to_handle = ""

        if pre_string == "+" or not dice_notation:
            if to_roll:

                num_dice = int(to_roll) if not double_dice else 2 * int(to_roll)
                dice = int(to_handle)

                rolls = [random.randint(1, dice) for _ in range(num_dice)]
                roll.total_roll += sum(rolls)
                roll.all_rolls[dice] += rolls

            else:
                modifier = int(to_handle)

                roll.total_roll += modifier

            to_roll = ""
            to_handle = ""

    return roll

def empty_set_or_set_of_dataclasses(variable) -> set:
    if variable is None:
        return set()
    if isinstance(variable, set) or isinstance(variable, list):
        return set(variable)
    else:
        return {variable}

def emtpy_list_or_list_of_dataclasses(variable) -> list:
    if variable is None:
        return []
    if isinstance(variable, set) or isinstance(variable, list):
        return list(variable)
    else:
        return [variable]
