import pygame_menu
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
        help_menu = HelpMenu()
        about_menu = AboutMenu()
        leaderboard_menu = LeaderboardMenu()

        intemediate_space = 15

        self.__home_menu = super().get_menu("Main Menu")

        self.__home_menu.add.button('Play', None, button_id='play')
        self.__home_menu.add.vertical_margin(intemediate_space)
        self.__home_menu.add.button('Hall of Fame', leaderboard_menu.Menu, button_id='hall_of_fame')
        self.__home_menu.add.vertical_margin(intemediate_space)
        self.__home_menu.add.button('Help', help_menu.Menu, button_id='help')
        self.__home_menu.add.vertical_margin(intemediate_space)
        self.__home_menu.add.button('About', about_menu.Menu, button_id='about')
        self.__home_menu.add.vertical_margin(intemediate_space)
        self.__home_menu.add.button('Exit', pygame_menu.events.EXIT, button_id='exit')

    @property
    def Menu(self) -> pygame_menu.Menu:
        """
        Property to get the MainMenu
        """
        return self.__home_menu
