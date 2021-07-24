import pygame_menu
from game.environment import GameEnvironment


class Menu:
    def __init__(self):
        """
        Constructor to create the menu.
        The default theme pygame_menu.themes.THEME_BLUE is modified for this game
        """
        self.__game_env = GameEnvironment()
        self.__game_theme = pygame_menu.themes.THEME_BLUE.copy()

        self.__game_theme.title_font = pygame_menu.font.FONT_COMIC_NEUE
        self.__game_theme.widget_font = pygame_menu.font.FONT_COMIC_NEUE

        self.__game_theme.background_color = (0, 0, 0, 0)             # transparent background
        self.__game_theme.title_font_color = (176, 196, 222)          # grey
        self.__game_theme.title_background_color = (176, 196, 222)    # grey
        self.__game_theme.widget_font_color = (0, 0, 250)             # dark blue
        self.__game_theme.selection_color = (250, 0, 0)               # dark red

        self.__game_theme.title_font_size = 60
        self.__game_theme.widget_font_size = 54

        self.__game_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE

        self.__game_theme.title_close_button = False

        # setting shadow to be the same color as widget to simulate bold font
        self.__game_theme.widget_font_shadow = True
        self.__game_theme.widget_font_shadow_color = (0, 0, 250)

        # for more bold, increase this
        self.__game_theme.widget_font_shadow_offset = 1

    def get_menu(self, title: str) -> pygame_menu.Menu:
        """
        method to create and return a pygame_menu.Menu
        :param titile : title of the menu
        :return menu : the menu created with given title
        """
        width_in_percent = 0.8
        height_in_percent = 0.65

        menu = pygame_menu.Menu(
            height=self.__game_env.static.screen_height * height_in_percent,
            theme=self.__game_theme,
            title=title,
            width=self.__game_env.static.screen_width * width_in_percent,
            touchscreen_motion_selection=False,
            touchscreen=True,
            center_content=True
        )
        return menu

    def add_link_to_mainmenu(self, menu: pygame_menu.Menu) -> pygame_menu.Menu:
        """
        method to add a button link to go back to the main menu
        :param menu : pygame_menu.Menu where the back button needs to be added
        :retunn menu : pygame_menu.Menu object with the back button added
        """
        # adding link button to HomeMenu
        menu.add.button('Back to Main Menu', pygame_menu.events.BACK, font_size=38)
        return menu
