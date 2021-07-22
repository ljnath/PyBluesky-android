import random

from game.environment import GameEnvironment
from pygame import image, sprite


# Missile class which holds missile attributes and behaviour
class Missile(sprite.Sprite):
    """ Missile sprite class for creating and updating the missile in the game screen
    """
    def __init__(self):
        super(Missile, self).__init__()                                                                                 # initilizing parent class pygame.sprite.Sprite
        game_env = GameEnvironment()
        self.surf = image.load(game_env.static.missile_activated_image).convert()                                       # loading missile image from file
        self.surf.set_colorkey((255, 255, 255), game_env.RLEACCEL)                                                      # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays

        # generating random missile position
        # but missile cannot on or above the scrore sprite
        pos_x = random.randint(game_env.static.screen_width + 10, game_env.static.screen_width + 60)
        pos_y = random.randint(game_env.static.score_sprite_width, game_env.static.screen_height - game_env.vegetation_size[1] / 2)
        self.rect = self.surf.get_rect(center=(pos_x, pos_y))                                                           # create rectange from the missile screen
        self.__activated = True                                                                                         # bad missiles will drop down
        self.__speed = random.randint(5, 20)                                                                            # generating random speed for the missle
        boost_factor = game_env.dynamic.game_level // 10                                                                # increasing missile speed by 5% every 10th level
        self.__speed += int(self.__speed * (boost_factor * 5) / 100)

    def update(self):
        game_env = GameEnvironment()
        if not self.__activated:
            self.rect.move_ip(0, 10)                                                            # missile moves down
        else:
            self.rect.move_ip(-self.__speed, 0)                                                 # missile moves towards jet

        if self.rect.right < 0 or self.rect.bottom > game_env.static.screen_height:             # if the missile has completly moved from the screen, the missile is killed
            self.kill()

    def deactivate(self):
        game_env = GameEnvironment()
        self.__activated = False                                                                # marking the current missile as bad
        self.surf = image.load(game_env.static.missile_deactivated_image).convert()             # updating missle image when deactivated
        self.surf.set_colorkey((255, 255, 255), game_env.RLEACCEL)                              # adding transperacny to image
