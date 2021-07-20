import time

import pygame_menu
from game.environment import GameEnvironment
from game.handlers.leaderboard import LeaderBoardHandler
from game.menu import Menu


class LeaderboardMenu(Menu):
    """
    Class to create the leaderboard menu
    """
    def __init__(self):
        super().__init__()
        self.__leaderboard_menu = super().get_menu('Hall of Fame')

    def __update_menu(self):
        """
        method to update the leaderboard menu
        """
        # clearing all widgets from the menu
        self.__leaderboard_menu.clear()

        # loading all leaders from local file
        leaders = LeaderBoardHandler().load()

        # if no leaders are preset then generic message is shown else the leaderboard table is created with all details
        if len(leaders) == 0:
            self.__leaderboard_menu.add.label('No record found.', align=pygame_menu.locals.ALIGN_CENTER, font_size=32)
            self.__leaderboard_menu.add.label('Please try after sometime and make sure that your phone has internet connectivity.', align=pygame_menu.locals.ALIGN_CENTER, font_size=32)
            self.__leaderboard_menu.add.vertical_margin(200)
        else:
            game_env = GameEnvironment()
            name_length = game_env.static.name_length * 3

            # creating leaders table with no border
            leaders_table = self.__leaderboard_menu.add.table(table_id='leaders', font_size=28, border_width=0)
            leaders_table.default_cell_padding = 5

            # adding the table header with no cell border
            leaders_table.add_row(['RANK',
                                   'NAME',
                                   'SCORE  ',
                                   'LEVEL  ',
                                   'ACCURACY  ',
                                   'SUBMISSION TIME'
                                   ], cell_border_width=0, cell_align=pygame_menu.locals.ALIGN_LEFT, cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

            # populating table
            for index, score in enumerate(leaders['scores']):
                row = [
                    str(index + 1),
                    score['name'][:name_length].ljust(name_length),
                    str(score['score']).ljust(12),
                    str(score['level']).ljust(7),
                    str(f"{score['accuracy']}%").ljust(10),
                    str(time.ctime(int(score['epoch']))).ljust(25)]

                leaders_table.add_row(row, cell_align=pygame_menu.locals.ALIGN_LEFT, cell_border_width=0)
            self.__leaderboard_menu.add.vertical_margin(50)

        # calling method to add back to the main menu
        super().add_link_to_mainmenu(self.__leaderboard_menu)

    @property
    def Menu(self):
        self.__update_menu()
        return self.__leaderboard_menu
