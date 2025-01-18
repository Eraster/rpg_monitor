from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional, List, Union, Dict
from copy import copy

from _game.base.environment import Location
from _game.base.functionality import roll_dice, RollInfo
from _game.entities.base.action import Action
from _game.base.functionality import roll_dice, empty_set_or_set_of_dataclasses, \
    emtpy_list_or_list_of_dataclasses
from _game.base.stats_abilities_and_settings import Abilities, Skills, AbilityScoreTracker, SkillScoreTracker, \
    DamageType, WeaponType, WeaponProperties, Size
from _game.base.weapons import BaseWeapon
from _game.entities.base.action import Action, ActionType


@dataclass
class HitPointTracker:
    rule_default: Optional[int] = None
    rule_rolls: Optional[str] = None
    play_max: Optional[int] = None
    play_max_modifier: Optional[int] = None
    current: Optional[int] = None
    dead: bool = False
    has_death_save: bool = False
    death_save: int = 0

    def set_default_hit_points(self):
        self.play_max = self.rule_default
        self.play_max_modifier = 0
        self.current = self.play_max

    def roll_hit_points(self):
        if self.rule_rolls is not None:
            self.play_max = roll_dice(self.rule_rolls).total_roll
        self.play_max_modifier = 0
        self.current = self.play_max

    def apply_damage(self, damage: RollInfo):
        self.current -= damage.total_roll if damage.total_roll > 0 else 0
        if self.current < 0 and not self.has_death_save:
            self.dead = True


@dataclass
class BattleTrackerMetaData:
    # This data is never Written directly by the Enemy Class
    entity_id: int = None
    initiative: int = None

    actions_affected_by: List[Action] = field(default_factory=list)
    actions_taken: List[Action] = field(default_factory=list)

    enemy_in_melee_range: bool = False

    left_hand: str = None
    right_hand: str = None
    both_hands: str = None
    inventory: str = field(default_factory=list)

    location: Location = None

class Entity:
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

        self.battle_data = BattleTrackerMetaData()

        self.race = race
        self.name = name

        self.armor_class = armor_class

        if not isinstance(hit_points, HitPointTracker):
            self.hit_points = HitPointTracker(rule_default=hit_points)
            self.hit_points.roll_hit_points()
        else:
            self.hit_points = hit_points
        self.hit_points.set_default_hit_points()

        self.size = size

        self.speed = speed
        self.proficiencies = empty_set_or_set_of_dataclasses(proficiencies)
        self.proficiency_bonus = proficiency_bonus

        self.ability_scores = {
            Abilities.STRENGTH: AbilityScoreTracker(base=strength),
            Abilities.DEXTERITY: AbilityScoreTracker(base=dexterity),
            Abilities.CONSTITUTION: AbilityScoreTracker(base=constitution),
            Abilities.INTELLIGENCE: AbilityScoreTracker(base=intelligence),
            Abilities.WISDOM: AbilityScoreTracker(base=wisdom),
            Abilities.CHARISMA: AbilityScoreTracker(base=charisma)
        }

        self.damage_resistances = empty_set_or_set_of_dataclasses(damage_resistances)
        self.damage_immunity = empty_set_or_set_of_dataclasses(damage_immunities)

        self.weapons = emtpy_list_or_list_of_dataclasses(weapons)

        if roll_for_stats:
            self.reroll_health_stats()
        self.initial_data_update()

    def _set_ability_skill_modifiers(self):
        for ability, score in self.ability_scores.items():
            if score.base is None:
                continue
            score.modifier = (score.base - 10)//2

        skill_scores = {}
        for skill in Skills:
            score = SkillScoreTracker()
            score.base_type = skill.get_ability()
            score.modifier_excl_proficiency = self.ability_scores[score.base_type].modifier
            if skill in self.proficiencies:
                score.modifier = score.modifier_excl_proficiency + self.proficiency_bonus
            else:
                score.modifier = score.modifier_excl_proficiency
            skill_scores[skill] = score
        self.skill_scores = skill_scores

    def initial_data_update(self):
        self._set_ability_skill_modifiers()

    def reroll_health_stats(self):
        self.hit_points.roll_hit_points()

    def add_weapon(self, weapon: BaseWeapon):
        self.weapons.append(weapon)

    def drop_weapon(self, weapon: BaseWeapon) -> BaseWeapon:
        weapon_num = None
        for num, carried_weapon in enumerate(self.weapons):
            if carried_weapon.name == weapon.name:
                weapon_num = num

        if weapon_num is None:
            raise ValueError(f"Could not drop weapon with name {weapon.name!r}.\n"
                             f"Available: {[w.name for w in self.weapons]!r}")
        else:
            drop = self.weapons.pop(weapon_num)

        return drop

    def _get_weapon_attacks(self, base_action: Action, bonus_action = False) -> List[Action]:

        weapon_attacks = []
        for weapon in self.weapons:
            if bonus_action and WeaponProperties.FINESSE not in weapon.properties:
                continue

            action = copy(base_action)
            action.action_type = ActionType.WEAPON_ATTACK_MELEE
            action.weapon = weapon

            # AC dice
            if WeaponProperties.HEAVY in weapon.properties and self.size == Size.SMALL:
                action.disadvantage = True

            action.ac_dice_notation = "d20"

            attack_modifiers = [stats for typ, stats in self.ability_scores.items() if typ in weapon.modifier]
            if attack_modifiers:
                used_modifier = max([at.modifier for at in attack_modifiers])
                action.ac_dice_notation += f" +{used_modifier}"

            if weapon.weapon_type in self.proficiencies:
                action.ac_dice_notation += f" +{self.proficiency_bonus}"

            attack_dice = weapon.damage_dice if not action.two_handed_attack and not weapon.two_handed_damage_dice else weapon.two_handed_damage_dice

            modifier_abilities = [stats for typ, stats in self.ability_scores.items() if typ in weapon.modifier]
            max_modifier = max(stat.modifier for stat in modifier_abilities) if modifier_abilities else 0
            attack_dice += f" +{max_modifier}"

            action.magic = True if weapon.magic_bonus else False
            action.magic_damage = weapon.magic_bonus if weapon.magic_bonus else 0
            attack_dice += f" +{action.magic_damage}"

            # Damage dice (source)
            if WeaponProperties.TWO_HANDED in weapon.properties and not action.two_handed_attack:
                action.action_info += ", attack_dice set to zero due to two handed weapon being used with one hand"
                #raise ValueError(f"Implement handling of two handed weapons.")
                attack_dice = ""

            action.source_roll_dice_notation = attack_dice

            # Append Actions and set values for ranged attacks
            if not WeaponProperties.RANGE in weapon.properties:
                weapon_attacks.append(copy(action))

            action.ranged_attack = True
            action.range = weapon.range
            action.range_disadvantage = weapon.range_disadvantage

            if {WeaponProperties.RANGE_AND_MELEE, WeaponProperties.RANGE} & weapon.properties:
                action.action_type = ActionType.WEAPON_ATTACK_RANGED
                weapon_attacks.append(copy(action))

            if WeaponProperties.THROWN in weapon.properties:
                action.action_type = ActionType.WEAPON_ATTACK_THROW
                weapon_attacks.append(copy(action))

        return weapon_attacks


    def get_actions(self,
                    current_turn: int,
                    current_round_number: int,
                    action_types: Optional[Union[ActionType, List[ActionType]]] = None
                    ) -> Dict[ActionType, List[Action]]:
        if action_types is None:
            action_types = list(ActionType)
        elif not isinstance(action_types, list):
            action_types = [action_types]

        possible_actions: Dict[ActionType, List[Action]] = dict()
        base_action = Action(
            battle_tracker_turn=current_turn,
            battle_tracker_round=current_round_number,
            source=self
        )

        if ActionType.WEAPON_ATTACK_MELEE in action_types:
            weapon_attacks = self._get_weapon_attacks(base_action=base_action)
            possible_actions[ActionType.WEAPON_ATTACK_MELEE] = weapon_attacks

        return possible_actions

    def get_bonus_actions(self,
                          current_turn: int = None,
                          current_round_number: int = None,
                          action_types: Optional[Union[ActionType, List[ActionType]]] = None
                          ) -> Dict[ActionType, List[Action]]:
        if action_types is None:
            action_types = list(ActionType)
        elif not isinstance(action_types, list):
            action_types = [action_types]

        possible_actions: Dict[ActionType, List[Action]] = dict()
        base_action = Action(
            battle_tracker_turn=current_turn,
            battle_tracker_round=current_round_number,
            source=self,
            bonus_action=True
        )

        if ActionType.WEAPON_ATTACK_MELEE in action_types:
            weapon_attacks = self._get_weapon_attacks(base_action=base_action, bonus_action=True)
            possible_actions[ActionType.WEAPON_ATTACK_MELEE] = weapon_attacks

        return possible_actions

    def roll_initiative(self):

        base_roll = roll_dice('d20').total_roll
        dex_stats = self.ability_scores[Abilities.DEXTERITY]

        return base_roll + dex_stats.modifier

    def description_short(self):
        return (f"{f'ID{self.battle_data.entity_id}, ' if self.battle_data.entity_id is not None else''}"
                f"{self.race}, "
                f"{f'\"{self.name}\", ' if self.name is not None else ''}"
                f"AC {self.armor_class}, "
                f"HP {self.hit_points.current}"
                f"{', DEAD' if self.hit_points.dead else ''}")

    def description(self):
        text = (f"""
        {self.race}{f', ID{self.battle_data.entity_id}' if self.battle_data.entity_id is not None else ''} 
        Base Stats:
            AC {self.armor_class}
            HP {self.hit_points.rule_default} ({self.hit_points.rule_rolls})
            Size {self.size.name}
            Speed {self.speed}
        Abilities:
            {Abilities.STRENGTH.name} {self.ability_scores[Abilities.STRENGTH].modifier}
            {Abilities.DEXTERITY.name} {self.ability_scores[Abilities.DEXTERITY].modifier}
            {Abilities.CONSTITUTION.name} {self.ability_scores[Abilities.CONSTITUTION].modifier}
            {Abilities.INTELLIGENCE.name} {self.ability_scores[Abilities.INTELLIGENCE].modifier}
            {Abilities.WISDOM.name} {self.ability_scores[Abilities.WISDOM].modifier}
            {Abilities.CHARISMA.name} {self.ability_scores[Abilities.CHARISMA].modifier}            
            """)
        return text

    def get_html(self) -> str:
        html = f"<h2>{self.race} {self.name!r} Stats</h2>"

        # Display Important Features
        html += "<table border='1' cellpadding='5'>"
        html += "<tr><th>Ability</th><th>Base</th><th>Max (+Modifier)</th><th>Current</th></tr>"
        html += f"<tr><td>Armor Class</td><td>{self.armor_class}</td><td>{'@TODO'}</td><td>{'@TODO'}</td></tr>"
        html += f"<tr><td>Hit Points</td>" \
                f"<td>{self.hit_points.rule_default} ({self.hit_points.rule_rolls})</td>" \
                f"<td>{self.hit_points.play_max} ({self.hit_points.play_max_modifier})</td>" \
                f"<td>{self.hit_points.current}</td></tr>"
        html += f"<tr><td>Speed</td><td>{self.speed}</td><td>{'@TODO'}</td><td>{'@TODO'}</td></tr>"
        html += "</table>"

        # Display Ability Scores
        html += "<h3>Ability Scores</h3>"
        html += "<table border='1' cellpadding='5'>"
        html += "<tr><th>Ability</th><th>Score</th><th>Modifier</th></tr>"
        for ability, tracker in self.ability_scores.items():
            score = tracker.base
            modifier = tracker.modifier
            html += f"<tr><td>{ability.name}</td><td>{score}</td><td>{modifier}</td></tr>"
        html += "</table>"

        # Display Skill Scores and Proficiencies
        if self.skill_scores or self.proficiencies:
            html += "<h3>Skill Scores</h3>"

            html += "<h4>Proficiencies</h4>"
            html += f"Bonus: {self.proficiency_bonus}"
            html += "<ul>"
            for proficiency in self.proficiencies:
                html += f"<li>{proficiency.name}</li>"
            html += "</ul>"

            html += "<h4>Skills</h4>"
            html += "<table border='1' cellpadding='5'>"
            html += "<tr><th>Skill</th><th>Base Score</th><th>Modifier</th></tr>"
            for skill, tracker in self.skill_scores.items():
                base_score = tracker.base_type
                modifier = tracker.modifier
                html += f"<tr><td>{skill.name}</td><td>{base_score.name}</td><td>{modifier}</td></tr>"
            html += "</table>"

        return html
