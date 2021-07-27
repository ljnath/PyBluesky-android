from enum import Enum


class BackgroundType(Enum):
    """
    Background type enumerator
    """
    DAY = 0
    NIGHT = 1
    MOUNTAIN = 2
    DESERT = 3
    MOON = 4
    BIG_CLOUD_1 = 5
    BIG_CLOUD_2 = 6
    BIG_CLOUD_3 = 7
    BIG_CLOUD_4 = 8
    BIG_CLOUD_5 = 9
    SMALL_CLOUD_1 = 10
    SMALL_CLOUD_2 = 11
    MEDIUM_CLOUD_1 = 12
    MEDIUM_CLOUD_2 = 13
    MEDIUM_CLOUD_3 = 14


class Choice(Enum):
    """
    Game menu choice enumerator
    """
    YES = 'YES'
    NO = 'NO'
    UNSELECTED = 'UNSELECTED'
    OK = 'OK'
    CLEAR = 'CLEAR'


class CloudType(Enum):
    """
    Cloud Type enumerator
    """
    BIG = 0
    SMALL = 1
    MEDIUM = 2


class GameState(Enum):
    """
    All Game state enumerator
    """
    READY_TO_RUN = 0
    RUNNING = 1
    PAUSED = 2
    GAMEOVER = 3
    
class JetMovement(Enum):
    """
    All jet movement enumerator
    """
    LEFT_2_RIGHT = 0
    RIGHT_2_LEFT = 1


class PowerUpState(Enum):
    """
    All powerup state enumerator; used to hold the state of power-up star
    """
    ACTIVE = 0
    INACTIVE = 1


class Screen(Enum):
    """
    Game screen enumerator
    """
    GAMEPLAY = 0        # main game play screen
    PAUSE_MENU = 1      # pause menu user player hits [BACK]
    REPLAY_MENU = 2     # replay menu when gameover
    NAME_INPUT = 3      # player name input screen


class SoundType(Enum):
    """
    All game sound enumerator
    """
    MISSILE_COLLISION = 0
    MISSILE_HIT = 1
    LEVEL_UP = 2
    POWER_UP = 3
    SHOOT = 4
    TANK_FIRE = 5
