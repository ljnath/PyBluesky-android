from game.environment import GameEnvironment
from pygame.font import Font
from pygame.sprite import Sprite


class Text(Sprite):
    """ Text class for create sprite out of text
    """
    def __init__(self, text='', size=0, color=None, pos_x=None, pos_y=None):
        Sprite.__init__(self)                                                                   # initializing parent class
        self.__game_env = GameEnvironment()
        self.color = self.__game_env.static.text_default_color if color is None else color      # storing argument color in class variable
        self.font = Font(self.__game_env.static.game_font, size)                                # loading font and creating class variable font with given size
        self.surf = self.font.render(text, 1, self.color)                                       # creating surface by rendering the text
        pos_x = self.__game_env.static.screen_width / 2 if pos_x is None else pos_x             # default position is set to center of screen
        pos_y = self.__game_env.static.screen_height / 2 if pos_y is None else pos_y            # default position is set to center of screen
        self.rect = self.surf.get_rect(center=(pos_x, pos_y))                                   # creating rectangle from the surface
        self.__move_forward = True
        self.__move_up = True

    def render(self, text):
        self.surf = self.font.render(text, 2, self.color)                                   # dynamically updating the surface with updated text

    def moveOnXaxis(self, speed):
        """ Method to move the text across the X axis
        """
        if not self.__move_forward and self.rect.x <= 0:                                    # detecting if the sprite should move forward or backward
            self.__move_forward = True
        elif self.__move_forward and self.rect.x + self.rect.width >= self.__game_env.static.screen_width:
            self.__move_forward = False
        self.rect.x += speed if self.__move_forward else (speed * -1)

    def moveOnYaxis(self, speed):
        """ Method to move the text across the Y axis
        """
        if not self.__move_up and self.rect.y <= 0:                                         # detecting if the sprite should move up or down
            self.__move_up = True
        elif self.__move_up and self.rect.y + self.rect.height >= self.__game_env.static.screen_height:
            self.__move_up = False
        self.rect.y += speed if self.__move_up else (speed * -1)
