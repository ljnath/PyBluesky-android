import random
from typing import Tuple

from pygame import image
from pygame.locals import (  # importing here to avoid reimporting in other places
    FULLSCREEN, K_DOWN, K_LEFT, K_RIGHT, K_UP, KEYDOWN, MOUSEBUTTONDOWN,
    MOUSEBUTTONUP, QUIT, RLEACCEL, SRCALPHA, TEXTINPUT, VIDEORESIZE)

from game.common.singleton import Singleton
from game.data.dynamic import DynamicData
from game.data.game_assets import GameAssets
from game.data.static import StaticData


class GameEnvironment(metaclass=Singleton):
    """
    Game environment class which holds all game constants, static game values as well as dynamic game variabled
    """
    def __init__(self):
        self.__static_data = StaticData()
        self.__dynamic_data = DynamicData()
        self.__game_assets = GameAssets()

    def get_random_point_on_right(self) -> Tuple[int, int]:
        """
        Method to get a random point on the right of the screen
        The X-pos is created somewhere between 20 to 100 px from the extreme right
        Y-pos can be anywhere along the height of the screen

        :return: random position as tuple
        """
        pos_x = random.randint(self.__static_data.screen_width + 20, self.__static_data.screen_width + 100)
        pos_y = random.randint(0, self.__static_data.screen_height)
        return (pos_x, pos_y)

    def get_random_point_on_top(self) -> Tuple[int, int]:
        """
        Method to get a random point on top of the screen
        X-pos can be anywhere along the width of the screen, while the Y-pos should be around 5 to 10 pixel from the screen height
        No point of creating point too high as it will not be visible in the screen

        :return: random position as tuple
        """
        pos_x = random.randint(0, self.__static_data.screen_width)
        pos_y = random.randint(5, 15)
        return (pos_x, pos_y * -1)

    def get_image_size(self, image_file: str) -> Tuple[int, int]:
        """
        Method to get the width and height of a image file in px
        :param image_file: input file whose size needs to be determined

        :return: width and height as a tuple
        """
        image_surf = image.load(image_file)
        return (image_surf.get_width(), image_surf.get_height())

    def reset_game_stats(self) -> None:
        """
        Method to rest the game stats to default
        """
        self.__dynamic_data.load_defaults()

    """
    GAME CONSTANTS
    """

    @property
    def static(self) -> StaticData:
        return self.__static_data

    @property
    def dynamic(self) -> DynamicData:
        return self.__dynamic_data

    @property
    def game_assets(self) -> GameAssets:
        return self.__game_assets

    @property
    def RLEACCEL(self) -> int:
        return RLEACCEL

    @property
    def SRCALPHA(self) -> int:
        return SRCALPHA

    @property
    def FULLSCREEN(self) -> int:
        return FULLSCREEN

    @property
    def QUIT(self) -> int:
        return QUIT

    @property
    def MOUSEBUTTONUP(self) -> int:
        return MOUSEBUTTONUP

    @property
    def MOUSEBUTTONDOWN(self) -> int:
        return MOUSEBUTTONDOWN

    @property
    def VIDEORESIZE(self) -> int:
        return VIDEORESIZE

    @property
    def KEYDOWN(self) -> int:
        return KEYDOWN

    @property
    def TEXTINPUT(self) -> int:
        return TEXTINPUT

    @property
    def K_UP(self) -> int:
        return K_UP

    @property
    def K_DOWN(self) -> int:
        return K_DOWN

    @property
    def K_LEFT(self) -> int:
        return K_LEFT

    @property
    def K_RIGHT(self) -> int:
        return K_RIGHT
