from typing import Any, Tuple

import pygame_menu
from game.environment import GameEnvironment
from game.menu import Menu
from game.menu.about import AboutMenu
from game.menu.help import HelpMenu
from game.menu.leaderboard import LeaderboardMenu


class MainMenu(Menu):
    """
    Class to create the main menu
    """
    def __init__(self):
        super().__init__()
        self.__game_env = GameEnvironment()
        help_menu = HelpMenu()
        about_menu = AboutMenu()
        leaderboard_menu = LeaderboardMenu()

        intemediate_space = 20

        music_selector_items = [('On', True), ('Off', False)]
        if not self.__game_env.dynamic.play_music:
            music_selector_items.reverse()

        self.__main_menu = super().get_menu("Main Menu")
        self.__main_menu.add.button('Play', None, button_id='play')
        self.__main_menu.add.vertical_margin(intemediate_space)
        self.__main_menu.add.selector(title='Music  ', items=music_selector_items, onchange=self.__update_music_playback_option)
        self.__main_menu.add.vertical_margin(intemediate_space)
        self.__main_menu.add.button('Hall of Fame', leaderboard_menu.Menu, button_id='hall_of_fame')
        self.__main_menu.add.vertical_margin(intemediate_space)
        self.__main_menu.add.button('Help', help_menu.Menu, button_id='help')
        self.__main_menu.add.vertical_margin(intemediate_space)
        self.__main_menu.add.button('About', about_menu.Menu, button_id='about')
        self.__main_menu.add.vertical_margin(intemediate_space)
        self.__main_menu.add.button('Exit', pygame_menu.events.EXIT, button_id='exit')

    @property
    def Menu(self) -> pygame_menu.Menu:
        """
        Property to get the MainMenu
        """
        return self.__main_menu

    def __update_music_playback_option(self, _: Tuple[Any, int], music: bool) -> None:
        """
        Method to update the environment 'play_music' based on the changed value in the selector
        :param value: Tuple containing the data of the selected object
        :param music: Selector value
        """
        if music != self.__game_env.dynamic.play_music:
            self.__game_env.dynamic.play_music = music
