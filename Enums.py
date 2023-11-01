from enum import Enum


class DealerStrategy(Enum) :
    HS17 = 0
    SS17 = 1

class Action(Enum):
    STAND = 0
    HIT = 1
    SPLIT = 2
    NO_SPLIT = 3
    DD = 4


    