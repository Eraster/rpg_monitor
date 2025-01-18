from enum import Enum, auto
from typing import Optional
from dataclasses import dataclass


class WeaponType(Enum):
    SIMPLE = auto()
    MARTIAL = auto()
    EXOTIC = auto()

class WeaponProperties(Enum):
    FINESSE = auto()
    LIGHT = auto()
    RANGE = auto()
    RANGE_AND_MELEE = auto()
    THROWN = auto()
    HEAVY = auto()
    TWO_HANDED = auto()

class Abilities(Enum):
    STRENGTH = auto()
    DEXTERITY = auto()
    CONSTITUTION = auto()
    INTELLIGENCE = auto()
    WISDOM = auto()
    CHARISMA = auto()


class Skills(Enum):
    ACROBATICS = auto()
    ANIMAL_HANDLING = auto()
    ARCANA = auto()
    ATHLETICS = auto()
    DECEPTION = auto()
    HISTORY = auto()
    INSIGHT = auto()
    INTIMIDATION = auto()
    INVESTIGATION = auto()
    MEDICINE = auto()
    NATURE = auto()
    PERCEPTION = auto()
    PERFORMANCE = auto()
    PERSUASION = auto()
    RELIGION = auto()
    SLEIGHT_OF_HAND = auto()
    STEALTH = auto()
    SURVIVAL = auto()

    def get_ability(self) -> Abilities:
        skill_to_ability = {
            Skills.ACROBATICS: Abilities.DEXTERITY,
            Skills.ANIMAL_HANDLING: Abilities.DEXTERITY,
            Skills.ARCANA: Abilities.INTELLIGENCE,
            Skills.ATHLETICS: Abilities.STRENGTH,
            Skills.DECEPTION: Abilities.CHARISMA,
            Skills.HISTORY: Abilities.INTELLIGENCE,
            Skills.INSIGHT: Abilities.WISDOM,
            Skills.INTIMIDATION: Abilities.CHARISMA,
            Skills.INVESTIGATION: Abilities.INTELLIGENCE,
            Skills.MEDICINE: Abilities.WISDOM,
            Skills.NATURE: Abilities.INTELLIGENCE,
            Skills.PERCEPTION: Abilities.WISDOM,
            Skills.PERFORMANCE: Abilities.CHARISMA,
            Skills.PERSUASION: Abilities.CHARISMA,
            Skills.RELIGION: Abilities.INTELLIGENCE,
            Skills.SLEIGHT_OF_HAND: Abilities.DEXTERITY,
            Skills.STEALTH: Abilities.DEXTERITY,
            Skills.SURVIVAL: Abilities.WISDOM
        }
        return skill_to_ability[self]

@dataclass
class AbilityScoreTracker:
    base: Optional[int] = None
    modifier: Optional[int] = 0


@dataclass
class SkillScoreTracker:
    base_type: Optional[Abilities] = None
    modifier_excl_proficiency: Optional[int] = None
    modifier: Optional[int] = 0

class DamageType(Enum):
    BLUDGEONING = auto()
    PIERCING = auto()
    SLASHING = auto()
    FIRE = auto()
    COLD = auto()
    LIGHTNING = auto()
    THUNDER = auto()
    ACID = auto()
    POISON = auto()
    NECROTIC = auto()
    RADIANT = auto()
    PSYCHIC = auto()
    FORCE = auto()

class Size(Enum):
    TINY = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    HUGE = auto()
    GARGANTUAN = auto()
