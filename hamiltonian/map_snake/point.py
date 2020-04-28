import time
import sys
from enum import Enum, unique


@unique
class PointType(Enum):
    """Type of the points on the game map."""
    EMPTY = 0
    WALL = 1
    FOOD = 2
    HEAD_L = 10
    HEAD_U = 11
    HEAD_R = 12
    HEAD_D = 13
    BODY_LU = 14
    BODY_UR = 15
    BODY_RD = 16
    BODY_DL = 17
    BODY_HOR = 18
    BODY_VER = 19


class Point:
    """Point on the game map."""
    def __init__(self):
        self._type = PointType.EMPTY

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        self._type = val
