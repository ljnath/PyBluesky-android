"""
Menu layout
+----------------------------------------+
|              === HINT ===              |
|              <user-input>              |
|              ============              |
|                                        |
|            CLEAR          OK           |
+----------------------------------------+
"""
import re

from game.environment import GameEnvironment
from game.sprites.text import Text
from pygame.surface import Surface
from pygame.key import start_text_input, stop_text_input
from game.data.enums import Choice


class NameInputText(Text):
    """ NameInputText class extended from Text class.
        Class is responsible for creating the sprite for taking player name as input
    """
    def __init__(self):
        Text.__init__(self, size=32)                                                    # initilizing parent class with default text color as red
        self.__game_env = GameEnvironment()
        self.__font_size = 56
        self.__player_name = ''
        self.__user_choice = Choice.UNSELECTED
        self.__choice_ok = Choice.OK
        self.__choice_clear = Choice.CLEAR

        self.__header = Text("==== ENTER YOUR NAME ====", self.__font_size)
        self.__username = Text(self.__player_name, self.__font_size)
        self.__footer = Text("===============================", self.__font_size)

        self.__ok_text = Text(f"< {self.__choice_ok.value} >", self.__font_size, self.color)
        self.__clear_text = Text(f"< {self.__choice_clear.value} >", self.__font_size, self.color)

        self.__ok_text_selected = Text(f"< {self.__choice_ok.value} >", self.__font_size, self.__game_env.static.text_selection_color)
        self.__clear_text_selected = Text(f"< {self.__choice_clear.value} >", self.__font_size, self.__game_env.static.text_selection_color)

        self.__max_surface_height = self.__footer.surf.get_height()
        self.__max_surface_width = self.__footer.surf.get_width()

        self.__render()

        # updating rect position of header rect
        self.rect = self.surf.get_rect(center=(self.__game_env.static.screen_width / 2, self.__game_env.static.screen_height / 2))

        pos_x = self.rect.left
        pos_y = self.rect.top
        self.__header.rect.update(pos_x, pos_y, self.__max_surface_width, self.__max_surface_height)

        # updating position of the input rect, the width and height is considered to be same as the header surface
        pos_y += self.__max_surface_height
        self.__username.rect.update(pos_x, pos_y, self.__max_surface_width, self.__max_surface_height)

        # updating position of footer rect; pos_x will be same; need to re-calculate pos_y
        pos_y += self.__max_surface_height
        self.__footer.rect.update(pos_x, pos_y, self.__max_surface_width, self.__max_surface_height)

        # updating position of CLEAR rect; pos_x will be same, only the pos_y will be different
        pos_y += self.__max_surface_height * 2
        self.__clear_text.rect.update(pos_x, pos_y, self.__clear_text.surf.get_width(), self.__max_surface_height)
        self.__clear_text_selected.rect.update(pos_x, pos_y, self.__clear_text.surf.get_width(), self.__max_surface_height)

        # updating the position for OK rect, pos_x will be differnet as OK text is to the right of CLEAR text; pos_y will be unchanged
        pos_x += self.surf.get_width() - self.__ok_text.surf.get_width()
        self.__ok_text.rect.update(pos_x, pos_y, self.__ok_text.surf.get_width(), self.__max_surface_height)
        self.__ok_text_selected.rect.update(pos_x, pos_y, self.__ok_text.surf.get_width(), self.__max_surface_height)

    def __render(self):
        self.__username = Text(self.__player_name, self.__font_size)
        # creating a single surface for all the text sprites, meuu layout is shown above
        # width of the surface should be same as the spirte with max width (ie the footer sprite)
        # max_surface_height * 6 because total 5 sprites + 1 seperator sprite will be included
        self.surf = Surface((self.__max_surface_width, self.__max_surface_height * 6), self.__game_env.SRCALPHA)
        self.surf.blit(self.__header.surf, (self.__max_surface_width / 2 - self.__header.surf.get_width() / 2, 0))
        self.surf.blit(self.__username.surf, (self.__max_surface_width / 2 - self.__username.surf.get_width() / 2, self.__max_surface_height))
        self.surf.blit(self.__footer.surf, (self.__max_surface_width / 2 - self.__footer.surf.get_width() / 2, self.__max_surface_height * 2))    # *3 will be skipped to introduce a seperator

        self.surf.blit(self.__clear_text_selected.surf if self.__user_choice == Choice.CLEAR else self.__clear_text.surf,
                       (0, self.__max_surface_height * 4))
        self.surf.blit(self.__ok_text_selected.surf if self.__user_choice == Choice.OK else self.__ok_text.surf,
                       (self.__max_surface_width - self.__ok_text.surf.get_width(), self.__max_surface_height * 4))

    def update(self, key):
        game_env = GameEnvironment()
        if key and re.match(r'[a-zA-Z0-9@. ]', key):                                    # basic input validation; user cannot enter rubbish
            if len(self.__player_name) <= game_env.static.name_length:                  # to avoid longer name
                self.__player_name += key
        # re-rendering the surface after updating the input text
        self.__render()

    def check_input(self, position):
        print(position)
        start_keyboard = False

        if self.__header.rect.collidepoint(position) or self.__username.rect.collidepoint(position) or self.__footer.rect.collidepoint(position):
            start_keyboard = True
            self.__user_choice = Choice.UNSELECTED

        elif self.__clear_text.rect.collidepoint(position) or self.__clear_text_selected.rect.collidepoint(position):
            if self.__user_choice == Choice.CLEAR:
                self.__game_env.dynamic.user_choice = Choice.CLEAR
                self.__player_name = ''
            self.__user_choice = Choice.CLEAR
            self.__render()
        elif self.__ok_text.rect.collidepoint(position) or self.__ok_text_selected.rect.collidepoint(position):
            if self.__user_choice == Choice.OK:
                self.__game_env.dynamic.user_choice = Choice.OK
                self.__player_name.strip()
                if len(self.__player_name) > 0:                                     # to avoid spaces as name
                    self.__game_env.dynamic.player_name = self.__player_name.strip()
            self.__user_choice = Choice.OK
            self.__render()

        if start_keyboard:
            start_text_input()
        else:
            stop_text_input()
