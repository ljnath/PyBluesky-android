from game.environment import GameEnvironment
from pygame import sprite


# Star class which holds star attributes and behaviour
class Star(sprite.Sprite):
    """ Powerup sprite class for creating and updating the star in the game screen
    """
    def __init__(self):
        super(Star, self).__init__()
        game_env = GameEnvironment()
        self.surf = game_env.game_assets.powerup_star
        self.surf.set_colorkey((255, 255, 255), game_env.RLEACCEL)
        self.rect = self.surf.get_rect(center=game_env.get_random_point_on_top())               # powerup stars are created on top of screen
        self.__current_alpha = 255
        self.__transperant = False
        flash_rate = 6                                                                          # setting the blink rate of the star
        self.__alpha_delta = int(255 / flash_rate)                                              # calculating the alpha delta based on the blink rate

    def update(self) -> None:
        """
        Method to update the power-up star.
        Star moves from top to bottom in blinking fashion
        """
        game_env = GameEnvironment()
        self.rect.move_ip(0, 5)                                                                 # star moves down with speed 5
        if self.__current_alpha < 0 or self.__current_alpha > 255:                              # reversing the tranperancy value if alpha reaches threshold
            self.__transperant = ~self.__transperant                                            # flicking effect on the star
        self.__current_alpha += self.__alpha_delta if self.__transperant else -self.__alpha_delta
        self.surf.set_alpha(self.__current_alpha)
        if self.rect.top > game_env.static.screen_height:                                       # star is killed if it crosses the screens
            self.kill()
