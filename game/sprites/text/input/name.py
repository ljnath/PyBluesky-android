import re

from game.environment import GameEnvironment
from game.sprites.text import Text
from pygame.surface import Surface
from pygame.key import start_text_input, stop_text_input


class NameInputText(Text):
    """ NameInputText class extended from Text class.
        Class is responsible for creating the sprite for taking player name as input
    """
    def __init__(self):
        Text.__init__(self, size=32)                                                    # initilizing parent class with default text color as red
        game_env = GameEnvironment()
        self.__is_rect_updated = False
        self.__player_name = ''
        self.__header = Text("=== ENTER YOUR NAME ===", 36)
        self.__footer = Text("===============================", 36)
        self.__seperator = Text(' ', 36)
        self.__clear = Text("< CLEAR >", 36)
        self.__ok = Text("< OK >", 36)

        max_surface_height = self.__footer.surf.get_height()
        max_surface_width = self.__footer.surf.get_width()

        # creating a single bottom surface to hold the footer, seperator and user buttons
        # width of the bottom surface is same as the width of the header text and height is same as footer + seperator + choice-texts (CLEAR & OK)
        self.__bottom_surface = Surface((max_surface_width, max_surface_height * 3), game_env.SRCALPHA)
        self.__bottom_surface.blit(self.__footer.surf, (0, 0))
        self.__bottom_surface.blit(self.__seperator.surf, (0, max_surface_height))
        self.__bottom_surface.blit(self.__clear.surf, (0, max_surface_height * 2))
        self.__bottom_surface.blit(self.__ok.surf, (max_surface_width - self.__ok.surf.get_width(), max_surface_height * 2))

        self.__render()

    def update(self, key):
        game_env = GameEnvironment()
        if key and re.match(r'[a-zA-Z0-9@. ]', key):                                    # basic input validation; user cannot enter rubbish
            if len(self.__player_name) <= game_env.static.name_length:                  # to avoid longer name
                self.__player_name += key

        # re-rendering the surface after updating the input text
        self.__render()

    def check_for_touch(self, position):
        start_keyboard = False

        if self.__header.rect.collidepoint(position):
            start_keyboard = True
        elif self.__input.rect.collidepoint(position):
            start_keyboard = True
        elif self.__footer.rect.collidepoint(position):
            start_keyboard = True
        elif self.__clear.rect.collidepoint(position):
            self.__player_name = ''
            self.__render()
        elif self.__ok.rect.collidepoint(position):
            if len(self.__player_name.strip()) > 0:                                     # to avoid spaces as name
                game_env = GameEnvironment()
                game_env.dynamic.player_name = self.__player_name.strip()
            else:
                self.__player_name.strip()

        if start_keyboard:
            start_text_input()
        else:
            stop_text_input()

    def __render(self):
        game_env = GameEnvironment()
        # self.__input = self.font.render(self.__player_name, 1, self.color)
        self.__input = Text(self.__player_name, 36)

        max_surface_height = self.__footer.surf.get_height()
        max_surface_width = self.__footer.surf.get_width()

        # creating a new surface to stitch all header, input and footer surface together
        self.surf = Surface((max_surface_width, max_surface_height * 5), game_env.SRCALPHA)

        # stitching the header, input and footer surface into one
        self.surf.blit(self.__header.surf, (self.surf.get_width() / 2 - self.__header.surf.get_width() / 2, 0))
        self.surf.blit(self.__input.surf, (self.surf.get_width() / 2 - self.__input.surf.get_width() / 2, max_surface_height))
        self.surf.blit(self.__bottom_surface, (self.surf.get_width() / 2 - self.__bottom_surface.get_width() / 2, max_surface_height * 2))

        # creating rect from the stitched surface
        self.rect = self.surf.get_rect(center=(game_env.static.screen_width / 2, game_env.static.screen_height / 2))

        # updating positions if it hasn't been done yet; the default x and y for the header rect is 0,0
        # so comparing against that
        if not self.__is_rect_updated:
            self.__is_rect_updated = True

            # updating position of header rect
            pos_x = self.rect.left
            pos_y = self.rect.top
            self.__header.rect.update(pos_x, pos_y, max_surface_width, max_surface_height)

            # updating position of the input rect, the width and height is considered to be same as the header surface
            pos_y += max_surface_height
            self.__input.rect.update(pos_x, pos_y, max_surface_width, max_surface_height)

            # updating position of footer rect; pos_x will be same; need to re-calculate pos_y
            pos_y += max_surface_height
            self.__footer.rect.update(pos_x, pos_y, max_surface_width, max_surface_height)

            # updating position of CLEAR rect; pos_x will be same, only the pos_y will be different
            pos_y += max_surface_height * 2
            self.__clear.rect.update(pos_x, pos_y, self.__clear.surf.get_width(), max_surface_height)

            # updating the position for OK rect, pos_x will be differnet as OK text is to the right of CLEAR text; pos_y will be unchanged
            pos_x += self.surf.get_width() - self.__ok.surf.get_width()
            self.__ok.rect.update(pos_x, pos_y, self.__ok.surf.get_width(), max_surface_height)
