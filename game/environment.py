import os
import random

from pygame import image
from pygame.locals import (
    MOUSEMOTION,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    FULLSCREEN,
    QUIT,
    RLEACCEL,
    SRCALPHA,
    VIDEORESIZE,
    KEYDOWN
)

from game.common.singleton import Singleton
from game.data.dynamic import DynamicData
from game.data.static import StaticData

# importing here to avoid reimporting in all the sub modules


class GameEnvironment(metaclass=Singleton):
    """ Game environment which holds the game contants, variables as well as pygame constants
    """
    def __init__(self):
        self.__static_data = StaticData()
        self.__dynamic_data = DynamicData()

    def get_random_point_on_right(self):
        pos_x = random.randint(self.__static_data.screen_width + 20, self.__static_data.screen_width + 100)     # generating random x position
        pos_y = random.randint(0, self.__static_data.screen_height)                                             # generating random y position
        return (pos_x, pos_y)

    def get_random_point_on_top(self):
        pos_x = random.randint(0, self.__static_data.screen_width)                      # generating random x position
        pos_y = random.randint(10, 20)                                                  # generating random y position
        return (pos_x, pos_y * -1)

    def get_image_size(self, image_file):
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
    def MOUSEMOTION(self):
        return MOUSEMOTION

    @property
    def VIDEORESIZE(self):
        return VIDEORESIZE

    @property
    def KEYDOWN(self):
        return KEYDOWN
