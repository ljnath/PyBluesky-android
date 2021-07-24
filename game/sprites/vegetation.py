import math
import random

from game.environment import GameEnvironment
from pygame import image, sprite


class Vegetation(sprite.Sprite):
    """ Vegetation sprite class for creating and updating the vegetation in the game screen
    """
    def __init__(self, x_pos: int = None, y_pos: int = None):
        """
        Method to create a vegeration from a randomly selected vegeration image
        :param x_pos: Starting X-position of the vegetation
        :param y_pos: Starting Y-position of the vegetation
        """
        super(Vegetation, self).__init__()
        game_env = GameEnvironment()
        self.surf = image.load(random.choice(game_env.static.vegetation)).convert()
        ground = image.load(game_env.static.ground).convert()
        grass = image.load(game_env.static.grass).convert()
        grass.set_colorkey((255, 255, 255), game_env.RLEACCEL)

        pos = 0
        for _ in range(math.ceil(self.surf.get_width() / ground.get_width())):
            self.surf.blit(ground, (pos, self.surf.get_height() - 40))
            if random.choice([True, False]):
                self.surf.blit(grass, (pos - 38, self.surf.get_height() - 40 - 28))
            pos += ground.get_width()
        x_pos = game_env.static.screen_width if x_pos is None else x_pos
        y_pos = game_env.static.screen_height - self.surf.get_height() / 2 if y_pos is None else y_pos
        self.rect = self.surf.get_rect(center=(x_pos, y_pos))
        self.__speed = 6

    def update(self) -> None:
        """
        Method to update the vegetation
        """
        self.rect.move_ip(-self.__speed, 0)
        if self.rect.right < 0:
            self.kill()
