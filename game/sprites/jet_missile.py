import math
from typing import Tuple

from game.environment import GameEnvironment
from pygame import sprite


class JetMissile(sprite.Sprite):
    """
    JetMissile sprite is the missile shot by the jet
    """
    def __init__(self, position: Tuple[int, int]):
        """
        Constructor to create a JetMissile sprite
        :prarm position : Position where the JetMissile should be created
        """
        super(JetMissile, self).__init__()
        game_env = GameEnvironment()
        self.__speed = 15
        self.surf = game_env.game_assets.jet_missile
        self.rect = self.surf.get_rect(center=position)

    def update(self) -> None:
        """
        Method to update the JetMissile sprite
        """
        game_env = GameEnvironment()
        dx = game_env.static.screen_width - self.rect.x
        dy = 0
        angle = math.atan2(dy, dx)
        self.rect.x += self.__speed * math.cos(angle)
        self.rect.y += self.__speed * math.sin(angle)

        # killing the missile if it crosses the screen completely
        if self.rect.left > game_env.static.screen_width:
            self.kill()
