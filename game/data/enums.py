from enum import Enum


class Choice(Enum):
    """
    Game menu choice enumerator
    """
    YES = 'YES'
    NO = 'NO'
    UNSELECTED = 'UNSELECTED'
    OK = 'OK'
    CLEAR = 'CLEAR'


class Screen(Enum):
    """
    Game screen enumerator
    """
    GAMEPLAY = 0        # main game play screen
    PAUSE_MENU = 1      # pause menu user player hits [BACK]
    REPLAY_MENU = 2     # replay menu when gameover
    NAME_INPUT = 3      # player name input screen
