import streamlit as st
from itertools import chain
from copy import deepcopy, copy

from _game.base.environment import LocationMetric, Location
from _game.base.weapons import Weapons
from _game.entities.base.action import Action, ActionType
from _game.entities.base.entity import Entity
from _game.entities.entities.monsters import PredefinedMonsters
from _game.base.functionality import roll_dice
from _game.mechanics.battle_tracker import Battletracker


def page_set_up_add_player(bt) -> Battletracker:

    st.subheader(f"Add Players: Build")
    st.warning("In Development")

    return bt

def page_set_up_add_enemy(bt) -> Battletracker:

    st.subheader(f"Add Enemies:")
    added_enemy_name = st.selectbox("Select Enemy:", list(PredefinedMonsters.get_monster()))
    add_enemy: Entity = deepcopy(PredefinedMonsters.get_monster(race=added_enemy_name))

    cols = st.columns(2)
    if cols[0].button("Add Enemy Base Stats"):
        bt.add_entity(add_enemy)
    if cols[1].button("Add Enemy Rolled Stats"):
        bt.add_entity(add_enemy, roll_health=True)

    # Remove
    st.subheader(f"Remove Enemies:")
    selected_enemy = st.radio(f"Select enemies:", [(enemy_id, enemy.description_short())
                                                   for enemy_id, enemy in bt.enemy.items()])
    if st.button(f"Remove {selected_enemy}", disabled=True if selected_enemy is None else False):
        st.write("Removed selected enemy. (Press any on screen button to view changes.)")
        if selected_enemy is not None:
            st.write(selected_enemy[0])
            bt.remove_entity(selected_enemy[0])

    # Enemy information page
    st.markdown(add_enemy.get_html(), unsafe_allow_html=True)

    return bt

def page_set_up_alter(bt) -> Battletracker:
    if not bt.enemy:
        st.warning(f"Add enemies prior to mutation.")
        return bt

    # Alter
    st.subheader(f"Select Enemy:")


    selected_enemy = st.radio(f"Select enemies:", [(enemy_id, enemy.description_short())
                                                   for enemy_id, enemy in bt.enemy.items()])

    weapon = st.selectbox(f"Select weapon:", list(Weapons.all_weapons.keys()))
    if st.button("Add Weapon to Enemy"):
        enemy = bt.enemy[selected_enemy[0]]
        enemy.add_weapon(weapon=Weapons.get_weapon(weapon))

    weapons = bt.enemy[selected_enemy[0]].weapons
    weapon_name = st.radio(f"Select weapon:", [(i, w.description_short) for i, w in enumerate(weapons)])
    if st.button("Remove Weapon", disabled=True if weapon_name is None else False):
        enemy = bt.enemy[selected_enemy[0]]
        if weapon_name is not None:
            del enemy.weapons[weapon_name[0]]

    return bt

def page_play_order_placement(bt) -> Battletracker:
    if not bt.enemy:
        st.warning(f"Add enemies prior to mutation.")
        return bt

    # Roll Initiative
    st.subheader("Initiative:")

    cols = st.columns(2)
    if cols[0].button(f"Roll Initiative (ALL)"):
        bt.roll_initiative_for_all()
    if cols[1].button(f"Roll Initiative (Newly added)"):
        bt.roll_initiative_for_added_entities()

    col_description, col_initiative = st.columns(2)

    col_description.subheader("Entity")
    col_initiative.subheader("Initiative")

    initiatives = {}
    for id, enemy in bt.enemy.items():
        with st.container():
            col_description, col_initiative = st.columns(2)

            col_description.write(bt.enemy[id].description_short())
            initiative = col_initiative.number_input(
                label=f"Init {id}",
                value=enemy.battle_data.initiative if enemy.battle_data.initiative is not None else 0
            )

            initiatives[id] = initiative

    if st.button("Process initiative"):
        if initiatives:
            bt.mutate_initiative_rolls(initiatives=initiatives)
            st.write("Data Processed succesfully.")
        else:
            st.warning("No data entered.")

    # Entity Placement
    st.subheader("Placement:")

    ids = list(bt.enemy)
    placements = {}

    metric = st.radio("Metric", list(LocationMetric))
    st.write(Location(metric=metric).description())

    # Create columns for X and Y values
    col_description, colx, coly = st.columns(3)  # Two columns for X and Y

    # Add headers for X and Y
    col_description.subheader("Enemy")
    colx.subheader("Coordinates")
    coly.subheader("")

    # Collect input data for each ID in rows
    for id in ids:
        # Create a row for each ID with X and Y inputs
        with st.container():
            col_description, colx, coly = st.columns(3)  # Columns for X and Y inputs

            col_description.write(bt.enemy[id].description_short())
            x_value = colx.number_input(label=f"X {id}:", step=1)
            y_value = coly.number_input(label=f"Y {id}:", step=1)

            # Store the inputs in the dictionary
            placements[id] = {"x": x_value, "y": y_value}

    if st.button("Process Data"):
        if placements:
            for key, values in placements.items():
                bt.place_entity(key, x=values['x'], y=values['y'], metric=metric)
            st.write("Data Processed succesfully.")
            st.write("Click again to enable 'Battle' Sidebar functionality.")
        else:
            st.warning("No data entered.")

    return bt

def page_battle(bt) -> Battletracker:
    if not bt.enemy:
        st.warning(f"Add enemies prior to mutation.")
        return bt
    if not bt.turn_order:
        st.warning(f"Define Turn Order prior to Action taking.")
        return bt
    if any([True if e.battle_data.location is None else False for e in bt.enemy.values()]):
        st.warning(f"Ensure that every Entity has loaded Locations.")
        return bt

    col_a, col_b = st.columns([1, 1], gap="small")
    with col_a:
        button_prev_player = st.button("<- Prev. Turn")
    with col_b:
        button_next_player = st.button("Next Turn ->")

    if button_next_player:
        bt.set_next_player()
        st.session_state.executed_actions = None
        st.session_state.primed_actions = None
    if button_prev_player:
        bt.set_previous_player()
        st.session_state.executed_actions = None
        st.session_state.primed_actions = None

    current_entity = bt.get_current_entity()
    if bt.current_entity is None:
        st.write(f"Round: {bt.get_current_round_number()}, Turn: {bt.get_current_turn_number()}")
    else:
        st.write(f"Round: {bt.get_current_round_number()}, "
                 f"Turn: {bt.get_current_turn_number()}, "
                 f"{current_entity.description_short()}")

    if bt.current_entity is None:
        st.write(f"Continue with first round for usage.")
        return bt

    st.sidebar.write("Next turns:")
    for turn, entity in bt.get_turn_order():
        st.sidebar.write(f"{turn}, {entity.description_short()}")


    # Main Selection
    st.markdown("### Action")
    col_actions, col_targets, col_execute = st.columns(3)

    # First column content (Action and Bonus Action)

    with col_actions:
        actions = bt.get_actions(source=bt.current_entity)
        actions_flat = list(chain(*actions.values()))
        action_selection = {str(num) + " " + action.description_prior(): action for num, action in
                            enumerate(actions_flat)}
        selected_action_key = st.radio("Choose Action:", list(action_selection))
        st.session_state.selected_action = action_selection[selected_action_key]

    with col_targets:
        if st.session_state.selected_action is None:
            target_selection = {}
        else:
            target_selection = bt.get_targets(st.session_state.selected_action.allowed_target_types)
        target_description = st.radio(f"Select Target", target_selection.keys())
        target_id = target_selection[target_description] if target_description is not None else None

        if st.button(f"Prime Action", disabled=True if st.session_state.selected_action is None else False):
            if st.session_state.selected_action is not None:
                action: Action = st.session_state.selected_action
                st.session_state.primed_actions = bt.prime_action(action, target_id)
                st.session_state.executed_actions = None

    with col_execute:

        if st.session_state.primed_actions is not None:

            st.write("Primed Actions")
            for action in st.session_state.primed_actions:
                st.write(action.description_primed())

            st.markdown("Attack Reactions")
            st.markdown("- Attack of opportunity\n- Shield\n- Held Attack")

            if st.button(f"Execute Action"):

                executed_actions = bt.execute_actions(st.session_state.primed_actions)
                st.session_state.executed_actions = executed_actions
                st.session_state.primed_actions = None

        elif st.session_state.executed_actions is not None:
            st.write("Executed Action")
            for action in st.session_state.executed_actions:
                st.write(action.description_executed())

        else:
            st.warning("Prime Actions")

    st.markdown("### Bonus Action")
    st.markdown("- NotImplemented\n- ...\n- ...\n- ...")


    # Second column content (Movement and Reactions)
    col_actions, col_targets = st.columns(2)
    with col_actions:
        st.markdown("### Movement")

        new_loc = copy(current_entity.battle_data.location)
        with st.container():
            st.markdown("""
                <style>
                .stNumberInput label {
                    display: none;
                }
                </style>
            """, unsafe_allow_html=True)

            colx, coly = st.columns(2)  # Columns for X and Y inputs
            x_value = colx.number_input(label="X", step=1, label_visibility='hidden')
            y_value = coly.number_input(label="Y", step=1, label_visibility='hidden')

            new_loc.x = x_value
            new_loc.y = y_value

            st.write(f"Total: {current_entity.speed}, Minimal target location distance: "
                     f"{abs(new_loc - current_entity.battle_data.location)}")

        if st.button("Set New Location"):
            if new_loc:
                bt.place_entity(current_entity.battle_data.entity_id,
                                x=new_loc.x,
                                y=new_loc.y,
                                metric=new_loc.metric)
                st.write("Data Processed succesfully.")
            else:
                st.warning("No data entered.")

    return bt

def page_environment(bt) -> Battletracker:
    for key in bt.environment._environment.keys():
        st.write(key)
        for weapon in bt.environment._environment[key]:
            st.write(f"Weapon: {weapon.name}")
    return bt

def page_battle_summary(bt) -> Battletracker:

    st.subheader("Enemies")
    for num, enemy in bt.enemy.items():
        st.write(f"ID {num},  Enemy {enemy.description_short()}")

    st.subheader("Past Actions")
    for action in bt.battle_log_actions:
        st.write(action.description_executed())

    st.write(bt.turn_order)

    return bt

def main_battle_tracker():

    if 'battle_tracker' not in st.session_state:
        st.session_state.battle_tracker = Battletracker()
    bt = st.session_state.battle_tracker

    if 'selected_action' not in st.session_state:
        st.session_state.selected_action = None

    if 'primed_actions' not in st.session_state:
        st.session_state.primed_actions = None

    if 'executed_actions' not in st.session_state:
        st.session_state.executed_actions = None

    # Page Selection

    pages = [
        "Set Up: Add Players",
        "Set Up: Add Enemy",
        "Set Up: Modify Enemy",
        "Set Up: Play Order / Placement",
        "Battle",
        "Battlesummary",
        "Environment",
        "Store and Load",
        "Dice Roll"
    ]

    st.session_state.battle_tracker_page = st.sidebar.radio('Battle pages:', pages)

    st.title(f"{st.session_state.battle_tracker_page}")

    if st.session_state.battle_tracker_page == "Set Up: Add Players":
        bt = page_set_up_add_player(bt)

    if st.session_state.battle_tracker_page == "Set Up: Add Enemy":
        bt = page_set_up_add_enemy(bt)

    if st.session_state.battle_tracker_page == "Set Up: Modify Enemy":
        bt = page_set_up_alter(bt)

    elif st.session_state.battle_tracker_page == "Set Up: Play Order / Placement":
        bt = page_play_order_placement(bt)

    elif st.session_state.battle_tracker_page == "Battlesummary":
        bt = page_battle_summary(bt)

    elif st.session_state.battle_tracker_page == "Environment":
        bt = page_environment(bt)

    elif st.session_state.battle_tracker_page == "Battle":
        bt = page_battle(bt)

    elif st.session_state.battle_tracker_page == "Store and Load":
        st.write("Following allows to store and load battle data in between sessions or for battle tracking purposes")
        st.write("")
        # Button to select directory
        if st.button('Load Battle Data'):
            raise NotImplementedError()
            # File uploader allowing multiple files (and directories in compatible browsers)
            uploaded_files = st.file_uploader("Choose a folder", accept_multiple_files=True)

            # Display selected files
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    st.write(f"File: {uploaded_file.race}, Size: {uploaded_file.size} bytes")
                    print(f"File: {uploaded_file.race}, Size: {uploaded_file.size} bytes")
                bt.load_battle_data(uploaded_files)

        if st.button('Store Battle Data'):
            raise NotImplementedError()
            # bt.save_battle_data()

    elif st.session_state.battle_tracker_page == "Dice Roll":
        st.write("Independent Dice Rolls")
        input_take_damage = st.text_input("Roll:")
        if input_take_damage:
            roll = roll_dice(input_take_damage)
            st.write(roll.description())
            st.write("")

            st.write(roll)


    st.session_state.battle_tracker = bt