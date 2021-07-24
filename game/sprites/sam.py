import math
from typing import Tuple

from game.environment import GameEnvironment
from pygame import image, sprite, transform


class Sam(sprite.Sprite):
    """
    SurfaceToAirMissile (SAM) sprite for create and moving bullet
    """
    def __init__(self, source: Tuple[int, int], target: Tuple[int, int], flip: bool):
        """
        Creating a SAM which aims to to the jet.
        Intiailly the position of the jet is determned and angle is measured.
        Next the SAM image is rotated towards the jet
        :param source: Source position of the SAM
        :param target: Target position where the SAM needs to aim
        :param flip : If the SAM launcher is travelling from left2right
        """
        super(Sam, self).__init__()
        game_env = GameEnvironment()
        self.__angle = math.atan2(target[1] - source[1], target[0] - source[0])     # sam angle of fire in radian
        self.__speed = 7 + (1 if game_env.dynamic.game_level % 2 == 0 else 0)       # default sam speed is 5 and increased each level

        if flip:                                                                    # sam image rotational angle based on the fire position
            rotation_angle = 90 - self.__angle * (180 / 3.1415)
        else:
            rotation_angle = 270 + self.__angle * (180 / 3.1415)

        self.surf = image.load(game_env.static.sam).convert()                       # loading sam image
        self.surf = transform.rotate(self.surf, rotation_angle)                     # rotating the image
        self.surf = transform.flip(self.surf, flip, ~flip)                          # flipping image as necessary
        self.surf.set_colorkey((255, 255, 255), game_env.RLEACCEL)                  # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays
        self.rect = self.surf.get_rect(center=(source[0], source[1]))               # setting the position of the bullet as the input (souce_x, y_pos)

    def update(self) -> None:
        """
        Method to update the SAM
        """
        game_env = GameEnvironment()
        self.rect.x += self.__speed * math.cos(self.__angle)
        self.rect.y += self.__speed * math.sin(self.__angle)
        if self.rect.right < 0 or self.rect.left > game_env.static.screen_width or self.rect.bottom < 0:
            self.kill()
