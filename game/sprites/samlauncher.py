import random
from typing import Tuple

from game.environment import GameEnvironment
from game.sprites.sam import Sam
from pygame import image, sprite, transform


class SamLauncher(sprite.Sprite):
    """
    SamLauncher sprite class for creating and updating the vegetation in the game screen
    """
    def __init__(self):
        """
        Creating the SAM launcher with the SAM launcher image
        The SAM launcher can randomly come from wither Left2Right or from Right2Left.
        It also needs to travel a minimum distance before actually firing a SAM
        """
        super(SamLauncher, self).__init__()
        game_env = GameEnvironment()
        self.surf = image.load(game_env.static.sam_launcher).convert()
        self.surf.set_colorkey((255, 255, 255), game_env.RLEACCEL)
        self.__speed = random.randint(8, 12)                                                    # speed of the sam launcher
        self.__flip = random.choice([True, False])                                              # random filp choice, filp-launcher will travel from left2right, else from right2left
        self.__fired = False if random.choice([0, 1, 2]) == 0 else True                         # random choice is the launcher will fire or not; reducing launch probabity to 33%
        self.__min_distance = int(random.randint(10, 30) * game_env.static.screen_width / 100)  # min distance to cover before the launcher can fire

        # flip logic
        if self.__flip:
            self.surf = transform.flip(self.surf, True, False)
            x_pos = 0
        else:
            x_pos = game_env.static.screen_width
            self.__speed *= -1
            self.__min_distance -= game_env.static.screen_width

        y_pos = game_env.static.screen_height - self.surf.get_height() - 15
        self.rect = self.surf.get_rect(center=(x_pos, y_pos))

    def update(self, target: Tuple[int, int]) -> None:
        """
        Method to update the SAM launcher
        :param target: target position, used if the launcher thinks to fires the SAM
        """
        if not self.__fired and self.rect.x > self.__min_distance:    # if not fired and if the launcher has crossed the minimum diatance
            self.fire(target)
            self.__fired = True

        game_env = GameEnvironment()
        self.rect.move_ip(self.__speed, 0)
        if self.rect.right < 0 or self.rect.left > game_env.static.screen_width:
            self.kill()

    def fire(self, target: Tuple[int, int]) -> None:
        """
        Method to create SAM starting the SAM launcher position
        :param target: target position where the SAM needs to be fired
        """
        game_env = GameEnvironment()
        sam = Sam((self.rect.x, self.rect.y), target, self.__flip)
        game_env.dynamic.sam_missiles.add(sam)
        game_env.dynamic.all_sprites.add(sam)
        game_env.dynamic.samfire_sound.play()
