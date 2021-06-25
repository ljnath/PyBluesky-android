from enum import Enum


class StartChoice(Enum):
    """ StartChoice enumerator which holds the game start choice (start or exit) for the game
    """
    START = 1,
    EXIT = 2


class Screen(Enum):
    """ TitleScreen enumerator which holds the available title screens
    """
    GAME_MENU = 0,
    HELP = 1,
    LEADERBOARD = 2
    REPLAY_MENU = 3
    NAME_INPUT = 4
    EXIT_MENU = 5
    GAME_SCREEN = 6
