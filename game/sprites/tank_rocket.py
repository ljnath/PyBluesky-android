import math
from typing import Tuple

from game.environment import GameEnvironment
from pygame import sprite, transform


class TankRocket(sprite.Sprite):
    """
    TankRocket sprite for creating the rocket fired by the tank
    """
    def __init__(self, source: Tuple[int, int], target: Tuple[int, int], is_flip: bool):
        """
        Creating a tank rocket which travels towards the jet
        Intiailly the position of the jet is determned and angle is measured.
        Next the rocket image is rotated towards the jet
        :param source: Source position of the tank rocket
        :param target: Target position where the tank missile should hit
        :param is_flip : If the tank is travelling from left2right
        """
        super(TankRocket, self).__init__()
        game_env = GameEnvironment()

        # calculating the speed of the tank rocket, default speed is 7
        # the speed increased by 1 after each level
        # if game_level = 10, tank_activates_at = 6; then speed = 7 + ( 10 - 6 if 10 > 6 else 0 ) => speed = 7 + 4 => speed = 11
        self.__speed = 7 + (game_env.dynamic.game_level - game_env.static.tank_activates_at if game_env.dynamic.game_level > game_env.static.tank_activates_at else 0)

        # calculating the angle of fire in radian
        self.__angle = math.atan2(target[1] - source[1], target[0] - source[0])

        # if the tank is travelling from left to right, then the rocket image needs to be flipped
        if is_flip:
            rotation_angle = 90 - self.__angle * (180 / 3.1415)
        else:
            rotation_angle = 270 + self.__angle * (180 / 3.1415)

        self.surf = game_env.game_assets.tank_rocket

        self.surf = transform.rotate(self.surf, rotation_angle)                     # rotating the image
        self.surf = transform.flip(self.surf, is_flip, ~is_flip)                    # flipping image as necessary
        self.rect = self.surf.get_rect(center=source)                               # setting the position of the rocket as the input (souce_x, y_pos)

    def update(self) -> None:
        """
        Method to update the rocket
        """
        game_env = GameEnvironment()
        self.rect.x += self.__speed * math.cos(self.__angle)
        self.rect.y += self.__speed * math.sin(self.__angle)

        # killing the rocket if it crossed the left, right ot top of the screen
        if self.rect.right < 0 or self.rect.left > game_env.static.screen_width or self.rect.bottom < 0:
            self.kill()
