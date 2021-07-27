from typing import Tuple

from game.environment import GameEnvironment
from pygame.sprite import Sprite


class Text(Sprite):
    """ Text class for create sprite out of text
    """
    def __init__(self, text: str = '', size: int = 0, color: Tuple[int, int, int] = None, pos_x: int = None, pos_y: int = None) -> None:
        """
        Constructor for creating a text sprite
        :param text : Text which needs to used for creating the text sprite. This text will be displayed in the surface
        :param size : Size of the text
        :param color : Color of the text in RGB formar
        :param pos_x : X position of the text surface
        :param pos_y : Y position of the text surface
        """
        Sprite.__init__(self)                                                                   # initializing parent class
        self.__game_env = GameEnvironment()
        self.color = self.__game_env.static.text_default_color if color is None else color      # storing argument color in class variable
        self.font = self.__game_env.game_assets.get_font(size)                                  # loading font and creating class variable font with given size
        self.surf = self.font.render(text, 1, self.color)                                       # creating surface by rendering the text
        pos_x = self.__game_env.static.screen_width / 2 if pos_x is None else pos_x             # default position is set to center of screen
        pos_y = self.__game_env.static.screen_height / 2 if pos_y is None else pos_y            # default position is set to center of screen
        self.rect = self.surf.get_rect(center=(pos_x, pos_y))                                   # creating rectangle from the surface
        self.__move_forward = True
        self.__move_up = True

    def render(self, text: str) -> None:
        """
        Method for rendering a text on the surface
        :param text: text which neds to be drawn
        """
        self.surf = self.font.render(text, 2, self.color)                                   # dynamically updating the surface with updated text

    def moveOnXaxis(self, speed: int) -> None:
        """
        Method to move the text across the X axis
        :param speed : speed of movement
        """
        if not self.__move_forward and self.rect.x <= 0:                                    # detecting if the sprite should move forward or backward
            self.__move_forward = True
        elif self.__move_forward and self.rect.x + self.rect.width >= self.__game_env.static.screen_width:
            self.__move_forward = False
        self.rect.x += speed if self.__move_forward else (speed * -1)

    def moveOnYaxis(self, speed: int) -> None:
        """
        Method to move the text across the Y axis
        :param speed : speed of movement
        """
        if not self.__move_up and self.rect.y <= 0:                                         # detecting if the sprite should move up or down
            self.__move_up = True
        elif self.__move_up and self.rect.y + self.rect.height >= self.__game_env.static.screen_height:
            self.__move_up = False
        self.rect.y += speed if self.__move_up else (speed * -1)
