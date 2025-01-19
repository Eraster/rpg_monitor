from typing import Optional, Union, List, Dict, Tuple
from copy import copy, deepcopy

from _game.base.environment import Environment, LocationMetric
from _game.base.stats_abilities_and_settings import WeaponProperties
from _game.entities.base.entity import Entity
from _game.entities.base.action import Action, ActionType
from _game.base.environment import Location


class Battletracker:
    def __init__(self):
        self.enemy: Dict[int, Entity] = {}  # Enemy_id: Entity
        self.turn_order = {}  # Turn: Entity
        self.current_turn = -1
        self.current_round_number = -1
        self.current_entity: Optional[Entity] = None
        self.battle_log_actions = []
        self.environment: Environment = Environment()

    def add_entity(self, entity: Entity, roll_health = False):
        entity = deepcopy(entity)
        if roll_health:
            entity.reroll_health_stats()

        i = 0
        while i in self.enemy:
            i += 1
        entity.battle_data.entity_id = i
        self.enemy[i] = entity

    def place_entity(self,
                     entity: Union[Entity, int],
                     x: int,
                     y: int,
                     metric: LocationMetric = LocationMetric.HEX_BASE_60) -> None:

        if not isinstance(entity, int):
            entity = entity.battle_data.entity_id
        entity: Entity = self.enemy[entity]

        location = Location(x=x, y=y, metric=metric)
        entity.battle_data.location=location

    def remove_entity(self, entity: Union[Entity, str]):
        if isinstance(entity, int):
            enemy_id = entity
        else:
            enemy_id = entity.battle_data.entity_id

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

    def get_turn_order(self) -> List[List[Tuple[int, Entity]]]:
        ret = [[turn, entity] for turn, entity in self.turn_order.items() if turn >= self.current_turn]
        turn = 0
        while turn < self.current_turn:
            ret.append([turn, self.turn_order[turn]])
            turn += 1
        return ret


    def mutate_initiative_rolls(self, initiatives: Dict[int, int]):
        for id, initiative in initiatives.items():
            self.enemy[id].battle_data.initiative = initiative
        self._reorder_initiative()

    def get_current_round_number(self) -> int:
        return self.current_round_number

    def get_current_turn_number(self) -> int:
        return self.current_turn

    def get_current_entity(self) -> Entity:
        return self.current_entity

    def get_enemies(self):
        return list(self.enemy.values())

    def set_next_player(self):
        self.current_turn = self.current_turn + 1 if self.current_turn + 1 < len(self.turn_order) else 0
        self.current_round_number = self.current_round_number + 1 if self.current_turn == 0 else self.current_round_number
        self.current_entity = self.turn_order[self.current_turn]

    def set_previous_player(self):
        self.current_round_number = self.current_round_number if not self.current_turn == 0 else self.current_round_number - 1
        self.current_turn = self.current_turn - 1 if not self.current_turn == 0 else len(self.turn_order) - 1
        self.current_entity = self.turn_order[self.current_turn]

    def get_actions(self,
                    source: Optional[Entity] = None,
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

        return actions

    def get_bonus_actions(self,
                          source: Optional[Entity] = None,
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

    def _prime_action(self, action: Action) -> Action:
        action.primed = True

        action.apply_environment_effects()

        if action.action_type in {
            ActionType.WEAPON_ATTACK_MELEE,
            ActionType.WEAPON_ATTACK_RANGED,
            ActionType.WEAPON_ATTACK_THROW
        }:

            action.roll_ac()
            action.check_attack_success(defender_ac=action.target.armor_class)

            action.roll_source()
            action.apply_resistance_and_immunity(
                resistances=action.target.damage_resistances,
                immunities=action.target.damage_immunity
            )
        else:
            raise ValueError(f"ActionType '{action.action_type}' not recognized. "
                             f"Implement actionType in {self.__class__.__name__} '_apply_action.'")
        return action

    def prime_action(self,
                     action: Action,
                     targets: Optional[Union[Entity, int, List[Union[Entity, int]]]] = None) -> List[Action]:
        if targets is None:
            targets = [None]
        else:
            if not isinstance(targets, list):
                targets = [targets]
            targets = [t if isinstance(t, Entity) else self.enemy[t] for t in targets]

        primed_actions = []
        for target in targets:
            action = copy(action)
            action.target = target
            primed_actions.append(self._prime_action(action))

        return primed_actions

    def _execute_action(self, action: Action) -> Action:
        action.executed = True

        if action.action_type in {
            ActionType.WEAPON_ATTACK_MELEE,
            ActionType.WEAPON_ATTACK_RANGED,
            ActionType.WEAPON_ATTACK_THROW
        }:
            if action.success:
                action.target.hit_points.apply_damage(action.source_roll)

            if action.action_type == ActionType.WEAPON_ATTACK_THROW:
                drop = action.source.drop_weapon(action.weapon)
                self.environment.add_drop(drop, location=action.target.battle_data.location)
        else:
            raise ValueError(f"ActionType '{action.action_type}' not recognized. "
                             f"Implement actionType in {self.__class__.__name__} '_apply_action.'")

        if action.source is not None:
            action.source.battle_data.actions_taken.append(action)
        if action.target is not None:
            action.target.battle_data.actions_affected_by.append(action)
        self.battle_log_actions.append(action)
        return action

    def execute_actions(self, actions: List[Action]) -> List[Action]:
        return [self._execute_action(action) for action in actions]

    def full_action(self,
                    action: Action,
                    targets: Optional[Union[Entity, int, List[Union[Entity, int]]]] = None) -> List[Action]:
        primed_actions = self.prime_action(action, targets)
        executed_actions = self.execute_actions(primed_actions)
        return executed_actions

    def add_player(self):
        raise NotImplementedError()

    def remove_player(self):
        raise NotImplementedError()

    def save_battle_data(self):
        raise NotImplementedError()

    def load_battle_data(self, file):
        raise NotImplementedError()


