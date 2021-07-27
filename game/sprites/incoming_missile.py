import random

from game.environment import GameEnvironment
from pygame import sprite


class IncomingMissile(sprite.Sprite):
    """
    IncomingMissile sprite class for creating and updating the enemy missile in the game screen
    """
    def __init__(self):
        """
        Creating a missile
        """
        super(IncomingMissile, self).__init__()
        game_env = GameEnvironment()
        self.surf = game_env.game_assets.incoming_missile_activated

        # generating random position for the incoming missile; but missile cannot on or above the scrore sprite
        # and creating rect from the missile image
        pos_x = random.randint(game_env.static.screen_width + 10, game_env.static.screen_width + 60)
        pos_y = random.randint(10, game_env.static.jet_bottom_boundry)
        self.rect = self.surf.get_rect(center=(pos_x, pos_y))

        # activated missile will travel from right-2-left, deactivated one will drop down
        self.__activated = True

        # generating random speed for the missle
        self.__speed = random.randint(5, 20)

        # increasing missile speed by 5% every 10th level
        boost_factor = game_env.dynamic.game_level // 10
        self.__speed += int(self.__speed * (boost_factor * 5) / 100)

    def update(self) -> None:
        """
        Method for updating the enemy missile position.
        Activated missiles moves towards left and deactivated missiles moves towards bottom
        """
        game_env = GameEnvironment()
        if self.__activated:
            # missile moves from right to left
            self.rect.move_ip(-self.__speed, 0)
        else:
            # missile drops down
            self.rect.move_ip(0, 25)

        # killinh missile if it has completely moved left or fall through the bottom
        if self.rect.right < 0 or self.rect.bottom > game_env.static.screen_height:
            self.kill()

    def deactivate(self) -> None:
        """
        Method to deactivate a missile.
        The activate property of the missile is toggled and the image image is updated
        """
        game_env = GameEnvironment()
        self.__activated = False
        self.surf = game_env.game_assets.incoming_missile_deactivated
