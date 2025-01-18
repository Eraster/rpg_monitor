from typing import Optional, Union, List, Dict
from copy import copy, deepcopy

from _game.base.environment import Environment, LocationMetric
from _game.base.stats_abilities_and_settings import WeaponProperties
from _game.entities.base.player_base_sheet import Player
from _game.entities.base.enemy_base_sheet import Enemy
from _game.entities.base.action import Action, ActionType
from _game.base.environment import Location


class Battletracker:
    def __init__(self):
        self.enemy: Dict[int, Enemy] = {}  # Enemy_id: Enemy
        self.turn_order = {}  # Turn: Enemy
        self.current_turn = -1
        self.current_round_number = -1
        self.current_entity: Optional[Union[Enemy, Player]] = None
        self.battle_log_actions = []
        self.environment: Environment = Environment()

    def add_enemy(self, enemy: Enemy, roll_health = False):
        enemy = deepcopy(enemy)
        if roll_health:
            enemy.reroll_health_stats()

        i = 0
        while i in self.enemy:
            i += 1
        enemy.battle_data.entity_id = i
        self.enemy[i] = enemy

    def place_enemy(self,
                    enemy: Union[Enemy, int],
                    x: int,
                    y: int,
                    metric: LocationMetric = LocationMetric.HEX_BASE_60) -> None:

        if not isinstance(enemy, int):
            enemy = enemy.battle_data.entity_id
        enemy: Enemy = self.enemy[enemy]

        location = Location(x=x, y=y, metric=metric)
        enemy.battle_data.location=location

    def remove_enemy(self, enemy: Union[Enemy, str]):
        if isinstance(enemy, int):
            enemy_id = enemy
        else:
            enemy_id = enemy.battle_data.entity_id

        turn = 0
        new_order = {}
        for key, value in self.turn_order.items():
            if enemy_id == value.battle_data.entity_id:
                if enemy_id == self.current_entity.battle_data.entity_id:
                    self.current_entity = None
                continue

            if key == self.current_turn:
                self.current_turn = turn

            new_order[turn] = value
            turn += 1

        self.turn_order = new_order
        self.enemy.pop(enemy_id)

    def _reorder_initiative(self):
        init = [[e.battle_data.initiative ,e] for e in self.enemy.values()]
        init = sorted(init, key=lambda x: x[0], reverse=True)

        i = 0
        for initiative, enemy in init:
            self.turn_order[i] = enemy
            i += 1

    def roll_initiative_for_all(self):
        for enemy in self.enemy.values():
            enemy.battle_data.initiative = enemy.roll_initiative()
        self._reorder_initiative()

    def roll_initiative_for_added_entities(self):
        for enemy in self.enemy.values():
            if enemy.battle_data.initiative is None:
                enemy.battle_data.initiative = enemy.roll_initiative()
        self._reorder_initiative()

    def mutate_initiative_rolls(self, initiatives: Dict[int, int]):
        for id, initiative in initiatives.items():
            self.enemy[id].battle_data.initiative = initiative
        self._reorder_initiative()

    def get_current_round_number(self) -> int:
        return self.current_round_number

    def get_current_turn_number(self) -> int:
        return self.current_turn

    def get_current_entity(self) -> Union[Player, Enemy]:
        return self.current_entity

    def get_enemies(self):
        return list(self.enemy.values())

    def set_next_player(self):
        self.current_turn = self.current_turn + 1 if self.current_turn + 1 < len(self.turn_order) else 0
        self.current_round_number = self.current_round_number + 1 if self.current_turn == 0 else self.current_round_number
        self.current_entity = self.turn_order[self.current_turn]

    def get_actions(self,
                    source: Optional[Union[Enemy, Player]] = None,
                    action_types: Optional[Union[ActionType, List[ActionType]]] = None,
                    allow_all_actions: bool = False
                    ) -> Dict[ActionType, List[Action]]:
        if source is not None:
            actions = source.get_actions(
                current_turn=self.current_turn,
                current_round_number=self.current_round_number,
                action_types=action_types
            )
        else:
            actions = self.current_entity.get_actions(
                current_turn=self.current_turn,
                current_round_number=self.current_round_number,
                action_types=action_types
            )

        for action in actions:
            if action.action_type == ActionType.WEAPON_ATTACK_MELEE:
                if WeaponProperties.TWO_HANDED in action.weapon.properties:
                    action.two_handed_attaack = True

        return actions

    def get_bonus_actions(self,
                    source: Optional[Union[Enemy, Player]] = None,
                    action_types: Optional[Union[ActionType, List[ActionType]]] = None
                    ) -> Dict[ActionType, List[Action]]:
        if source is not None:
            actions = source.get_bonus_actions(
                current_turn=self.current_turn,
                current_round_number=self.current_round_number,
                action_types=action_types
            )
        else:
            actions = self.current_entity.get_bonus_actions(
                current_turn=self.current_turn,
                current_round_number=self.current_round_number,
                action_types=action_types
            )
        return actions

    def _apply_action(self, action: Action, target: Union[Enemy, Player] = None) -> Action:
        # Target and source handled at the end of function
        action.target = target

        action.apply_environment_effects()

        if action.action_type in {
            ActionType.WEAPON_ATTACK_MELEE,
            ActionType.WEAPON_ATTACK_RANGED,
            ActionType.WEAPON_ATTACK_THROW
        }:
            action.roll_ac()
            action.check_attack_success(defender_ac=target.armor_class)

            if action.success:
                action.roll_source()

                action.apply_resistance_and_immunity(
                    resistances=target.damage_resistances,
                    immunities=target.damage_immunity
                )

                target.hit_points.apply_damage(action.source_roll)

            if action.action_type == ActionType.WEAPON_ATTACK_THROW:
                drop = action.source.drop_weapon(action.weapon)
                self.environment.add_drop(drop, location=action.source.battle_data.location)

        else:
            raise ValueError(f"ActionType '{action.action_type}' not recognized. "
                             f"Implement actionType in {self.__class__.__name__} '_apply_action.'")

        action.target = target
        if action.source is not None:
            action.source.battle_data.actions_taken.append(action)
        if target is not None:
            target.battle_data.actions_affected_by.append(action)
        self.battle_log_actions.append(action)
        return action

    def apply_action(self,
                     action: Action,
                     targets: Optional[Union[Enemy, Player, int, List[Union[Enemy, Player, int]]]] = None) -> List[Action]:

        applied_actions = []

        if targets is not None:
            if not isinstance(targets, list):
                targets = [targets]

            targets = [t if isinstance(t, Enemy) or isinstance(t, Player) else self.enemy[t] for t in targets]

            for target in targets:
                applied_actions.append(self._apply_action(copy(action), target=target))

        else:
            applied_actions.append(self._apply_action(copy(action)))

        return applied_actions

    def add_player(self):
        raise NotImplementedError()

    def remove_player(self):
        raise NotImplementedError()

    def save_battle_data(self):
        raise NotImplementedError()

    def load_battle_data(self, file):
        raise NotImplementedError()


