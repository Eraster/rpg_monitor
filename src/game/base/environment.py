from __future__ import annotations

from collections import defaultdict
from typing import Optional, Dict, List
from enum import Enum, auto
from dataclasses import dataclass, field

from game.base.weapons import BaseWeapon


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
                return min(abs(self.x + self.y), abs(self.x - self.y)) + min(abs(self.x), abs(self.y))
            else:
                return abs(self.x) + abs(self.y)
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
            raise ValueError(f"Metric {self.metric!r} not supported for operator '-'.\n"
                             f"Supported: {LocationMetric.HEX_BASE_60}")

    def __repr__(self) -> str:
        return f"x({self.x}, y({self.y}, metric({self.metric.name}))"

    def description(self):
        if self.metric == LocationMetric.HEX_BASE_60:
            explanation = (f"The grid is defined as a hex based setting.\n"
                           f"Imagine the x axis as the horizontal base.\n"
                           f"Imagine the y axis as offset by 60 degrees from the x axis.\n"
                           f"This means that one to the right and one upwards (top right hex) "
                           f"has distance 2 with x = 1, y = 1.\n"
                           f"The top left hex from the current position has coordinates x = -1, y = 1 though.")
            return explanation

@dataclass
class EnvironmentSquare:
    location: Location = None
    weapons: List[BaseWeapon] = field(default_factory=list)

class Environment:
    def __init__(self):
        self._environment: Dict[str, EnvironmentSquare] = dict()
        self._default: EnvironmentSquare = EnvironmentSquare()

    def get_environment_square(self, location: Location = None):
        if location is None:
            return self._default
        elif repr(location) in self._environment:
            return self._environment[repr(location)]
        else:
            new = EnvironmentSquare(location=location)
            self._environment[repr(Location)] = new
            return new

    def add_drop(self, drop, location: Location = None):
        env = self.get_environment_square(location)

        if isinstance(drop, BaseWeapon):
            env.weapons.append(drop)
