from _game.base.environment import Location, LocationMetric
from _game.base.weapons import Weapons
from _game.entities.base.action import ActionType
from _game.entities.entities.monsters import ALL_MONSTERS
from _game.mechanics.battle_tracker import Battletracker

if __name__ == '__main__':
    bt = Battletracker()

    bt.add_entity(ALL_MONSTERS['Goblin'])
    bt.add_entity(ALL_MONSTERS['Goblin'])

    bt.enemy[0].add_weapon(weapon=Weapons.get_weapon('Greatsword'))
    bt.enemy[1].add_weapon(weapon=Weapons.get_weapon('Greatsword'))

    bt.roll_initiative_for_all()

    for enemy in bt.enemy.values():
        bt.place_entity(enemy, x=1, y=1, metric=LocationMetric.HEX_BASE_60)

    bt.set_next_player()
    actions = bt.current_entity.get_actions()[ActionType.WEAPON_ATTACK_MELEE]

    action = actions[-1]

    applied_actions = bt.apply_action(action, bt.enemy[1])

    print(bt.enemy[0].hit_points)
    print(bt.enemy[1].hit_points)
