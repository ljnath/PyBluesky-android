import random
from typing import Tuple

from pygame import image
from pygame.locals import (  # importing here to avoid reimporting in all the sub modules
    FULLSCREEN, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, RLEACCEL,
    SRCALPHA, TEXTINPUT, VIDEORESIZE)

from game.common.singleton import Singleton
from game.data.dynamic import DynamicData
from game.data.static import StaticData


class GameEnvironment(metaclass=Singleton):
    """ Game environment which holds the game contants, variables as well as pygame constants
    """
    def __init__(self):
        self.__static_data = StaticData()
        self.__dynamic_data = DynamicData()

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

    def reset(self):
        self.__dynamic_data.load_defaults()

    @property
    def vegetation_size(self):
        return self.get_image_size(self.__static_data.vegetation[0])

    @property
    def static(self):
        return self.__static_data

    @property
    def dynamic(self):
        return self.__dynamic_data

    @property
    def RLEACCEL(self):
        return RLEACCEL

    @property
    def SRCALPHA(self):
        return SRCALPHA

    @property
    def FULLSCREEN(self):
        return FULLSCREEN

    @property
    def QUIT(self):
        return QUIT

    @property
    def MOUSEBUTTONUP(self):
        return MOUSEBUTTONUP

    @property
    def MOUSEBUTTONDOWN(self):
        return MOUSEBUTTONDOWN

    @property
    def VIDEORESIZE(self):
        return VIDEORESIZE

    @property
    def KEYDOWN(self):
        return KEYDOWN

    @property
    def TEXTINPUT(self):
        return TEXTINPUT
