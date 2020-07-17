from enum import Enum

class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    SHOW_INVENTORY = 4
    DROP_INVENTORY = 5
    TARGETING = 6
    WEAPON_TARGETING = 7
    SPELL_TARGETING = 8
    LEVEL_UP = 9
    CHARACTER_SCREEN = 10