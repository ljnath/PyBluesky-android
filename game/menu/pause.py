import pygame_menu
from game.menu import Menu
from game.menu.about import AboutMenu
from game.menu.help import HelpMenu
from game.menu.leaderboard import LeaderboardMenu


class PauseMenu(Menu):
    """
    Class to create the main menu
    """
    def __init__(self):
        super().__init__()
        help_menu = HelpMenu()
        about_menu = AboutMenu()
        leaderboard_menu = LeaderboardMenu()

        intemediate_space = 15

        self.__home_menu = super().get_menu("Game Paused")

        self.__home_menu.add.button('Yes', None)
        self.__home_menu.add.vertical_margin(intemediate_space)
        self.__home_menu.add.button('No', leaderboard_menu.Menu)

    @property
    def Menu(self):
        return self.__home_menu
