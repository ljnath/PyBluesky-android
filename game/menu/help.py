import pygame_menu
from game.menu import Menu


class HelpMenu(Menu):
    """
    Class to cerate the Help menu
    """
    def __init__(self):
        super().__init__()

        self.__help_menu = super().get_menu('Help')

        # adding help text
        self.__help_menu.add.label('Your objective should you choose to accept, is to navigate your jet safely without getting hit by the incoming enemy', align=pygame_menu.locals.ALIGN_LEFT, font_size=28)
        self.__help_menu.add.label('missiles. You can also shoot down the enemy missiles to protect yourslf and navigate your way through. Initally you will be', align=pygame_menu.locals.ALIGN_LEFT, font_size=28)
        self.__help_menu.add.label('armed with 100 special missiles. Level-ups will awards you another 100 special missiles and a power-up star which will', align=pygame_menu.locals.ALIGN_LEFT, font_size=28)
        self.__help_menu.add.label('instantly deactivate all the enemy missiles. Intially your jet comes with 100% health which is indicated on top right corner of', align=pygame_menu.locals.ALIGN_LEFT, font_size=28)
        self.__help_menu.add.label('the screen. When hit by an enemy misile, the health drops by 20%. When it reaches 0%, the game ends.', align=pygame_menu.locals.ALIGN_LEFT, font_size=28)
        self.__help_menu.add.label('Your jet can carry a maximum 999 special missiles.', align=pygame_menu.locals.ALIGN_LEFT, font_size=28)
        self.__help_menu.add.vertical_margin(20)
        self.__help_menu.add.label('During gameplay, move your device horizontally and vertically to control your jet and tap on the screen to shoot missiles', align=pygame_menu.locals.ALIGN_LEFT, font_size=28)
        self.__help_menu.add.label('Game levels, score and other details are shown on top-right corner of the screen', align=pygame_menu.locals.ALIGN_LEFT, font_size=28)
        self.__help_menu.add.vertical_margin(20)
        self.__help_menu.add.label('The scoring system is shown below', align=pygame_menu.locals.ALIGN_LEFT, font_size=28)

        # creating score table
        score_table = self.__help_menu.add.table(table_id='score_table', font_size=28)
        score_table.default_cell_padding = 5
        score_table.add_row(['Destroy enemy missile   ', '10'], cell_border_width=0)
        score_table.add_row(['Catch Power-Up star   ', '100'], cell_border_width=0)
        score_table.add_row(['Level-up   ', '10'], cell_border_width=0)
        self.__help_menu.add.vertical_margin(50)

        # calling method to add back to the main menu
        super().add_link_to_mainmenu(self.__help_menu)

    @property
    def Menu(self) -> pygame_menu.Menu:
        """
        Property to get the HelpMenu
        """
        return self.__help_menu
