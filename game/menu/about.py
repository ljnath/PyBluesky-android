import pygame_menu
from game.environment import GameEnvironment
from game.menu import Menu


class AboutMenu(Menu):
    """
    Class to create the About menu
    """
    def __init__(self):
        super().__init__()
        game_env = GameEnvironment()

        self.__about_menu = super().get_menu('About')
        self.__about_menu.add.label(game_env.static.app_name, align=pygame_menu.locals.ALIGN_CENTER, font_size=60)
        self.__about_menu.add.label(f'Version {game_env.static.app_version}', align=pygame_menu.locals.ALIGN_CENTER, font_size=28)
        self.__about_menu.add.vertical_margin(120)
        self.__about_menu.add.label('Developer: Lakhya Jyoti Nath', align=pygame_menu.locals.ALIGN_CENTER, font_size=32)
        self.__about_menu.add.label('Email: ljnath@ljnath.com', align=pygame_menu.locals.ALIGN_CENTER, font_size=32)
        self.__about_menu.add.url(href='https://ljnath.com', title='Visit Homepage', align=pygame_menu.locals.ALIGN_CENTER, font_size=32)
        self.__about_menu.add.vertical_margin(100)
        self.__about_menu.add.label("Copyright © 2021 Lakhya's Innovation Inc.", align=pygame_menu.locals.ALIGN_CENTER, font_size=28)
        self.__about_menu.add.vertical_margin(50)

        # calling method to add back to the main menu
        super().add_link_to_mainmenu(self.__about_menu)

    @property
    def Menu(self):
        return self.__about_menu
