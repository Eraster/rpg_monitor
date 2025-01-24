from __future__ import annotations

from typing import Dict, List, Any
from enum import Enum
from dataclasses import dataclass, field

from _game.base.weapons import BaseWeapon


class LocationMetric(Enum):
    HEX_BASE_60 = "HexBase60"


class Location:
    def __init__(self, x: int = 0, y: int = 0, metric: LocationMetric = LocationMetric.HEX_BASE_60):
        self.x = x
        self.y = y
        self.metric = metric

    def __abs__(self) -> int:
        if self.metric == LocationMetric.HEX_BASE_60:
            if self.x < 0 < self.y or self.y < 0 < self.x:
                return 5 * (min(abs(self.x + self.y), abs(self.x - self.y)) + min(abs(self.x), abs(self.y)))
            else:
                return 5 * (abs(self.x) + abs(self.y))
        else:
            raise ValueError(f"Metric {self.metric!r} not supported for operator 'abs'.")

    def __add__(self, other: Location) -> Location:
        if not self.metric == other.metric:
            raise ValueError(f"Cannot add {self.__class__.__name__} of different metrics.\n"
                             f"Delivered metrics: {self.metric!r} and {other.metric!r}")

        if self.metric == LocationMetric.HEX_BASE_60:
            new_loc = Location(
                x=self.x + other.x,
                y=self.y + other.y,
                metric=self.metric
            )
            return new_loc
        else:
            raise ValueError(f"Metric {self.metric!r} not supported for operator '+'.")

    def __sub__(self, other: Location) -> Location:
        if not self.metric == other.metric:
            raise ValueError(f"Cannot add {self.__class__.__name__} of different metrics.\n"
                             f"Delivered metrics: {self.metric!r} and {other.metric!r}")

        if self.metric == LocationMetric.HEX_BASE_60:
            new_loc = Location(
                x=self.x - other.x,
                y=self.y - other.y,
                metric=self.metric
            )
            return new_loc
        else:
            raise ValueError(f"Metric {self.metric} (type {type(LocationMetric.HEX_BASE_60)}) "
                             f"not supported for operator '-'.\n"
                             f"Supported: {LocationMetric.HEX_BASE_60} (type {type(LocationMetric.HEX_BASE_60)})")

    def key(self) -> str:
        return f"x({self.x}), y({self.y}), metric({self.metric.name})"

    def description(self):
        if self.metric == LocationMetric.HEX_BASE_60:
            explanation = (f"The grid is defined as a hex based setting.\n"
                           f"Imagine the x axis as the horizontal base.\n"
                           f"Imagine the y axis as offset by 60 degrees from the x axis.\n"
                           f"This means that one to the right and one upwards (top right hex) "
                           f"has distance 2 with x = 1, y = 1.\n"
                           f"The top left hex from the current position has coordinates x = -1, y = 1 though.")
            return explanation

    def get_html(self) -> str:
        html = f"""
        <div class='location'>
            <h2>Location</h2>
            <ul>
                <li><strong>X Coordinate:</strong> {self.x}</li>
                <li><strong>Y Coordinate:</strong> {self.y}</li>
                <li><strong>Metric:</strong> {self.metric.name}</li>
            </ul>
        </div>
        """
        return html


@dataclass
class EnvironmentSquare:
    location: Location = None
    weapons: List[BaseWeapon] = field(default_factory=list)
    undefined: List[Any] = field(default_factory=list)

class Environment:
    def __init__(self):
        self._environment: Dict[str, EnvironmentSquare] = {}
        self._default: EnvironmentSquare = EnvironmentSquare()

    def get_environment_square(self, location: Location = None):
        if location is None:
            return self._default
        elif location.key() in self._environment:
            return self._environment[location.key()]
        else:
            self._environment[location.key()] = EnvironmentSquare(location=location)
            return self._environment[location.key()]

    def add_drop(self, drop, location: Location = None):
        env = self.get_environment_square(location)
        if drop is None:
            return

        if isinstance(drop, BaseWeapon):
            env.weapons.append(drop)
        else:
            env.undefined.append(drop)

    def spot_weapons(self) -> Dict[str, str]:
        weapons_def = {w.description_short: [None, w.name]
                   for w in self._default.weapons}
        weapons_sqr = {w.description_short: [loc, w.name]
                   for loc, square in self._environment.items()
                   for w in square.weapons}
        weapons_def.update(weapons_sqr)
        return weapons_def

    def pick_up_weapon(self, weapons_def) -> BaseWeapon:
        loc, weapon = weapons_def

        if loc is None:
            location = self._default
        elif loc in self._environment:
            location = self._environment[loc]

        weapons = location.weapons

        remaining_weapons = []
        pick_up = None
        pick_up_done = False
        for w in weapons:
            if weapon == w.name and not pick_up_done:
                pick_up = w
                pick_up_done = True
            else:
                remaining_weapons.append(w)

        location.weapons = remaining_weapons

        return pick_up


