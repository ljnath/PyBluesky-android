import random
from typing import Tuple

from game.data.enums import BackgroundType, JetMovement
from game.environment import GameEnvironment
from pygame import sprite


class Parallax(sprite.Sprite):
    def __init__(self, type: BackgroundType, position: Tuple[int, int] = None) -> None:
        sprite.Sprite.__init__(self)
        self.__background_type = type

        print(f'Creating {type} at position {position}')

        self.__game_env = GameEnvironment()
        self.surf = self.__game_env.game_assets.get_image(self.__background_type)
        self.__speed_of_cloud = 0

        # clouds can come from either direction, so the input position is updated accordingly
        # for others, the passed position is considered
        if self.__background_type in (BackgroundType.BIG_CLOUD_1,
                                      BackgroundType.BIG_CLOUD_2,
                                      BackgroundType.BIG_CLOUD_3,
                                      BackgroundType.BIG_CLOUD_4,
                                      BackgroundType.BIG_CLOUD_5,
                                      BackgroundType.SMALL_CLOUD_1,
                                      BackgroundType.SMALL_CLOUD_2,
                                      BackgroundType.MEDIUM_CLOUD_1,
                                      BackgroundType.MEDIUM_CLOUD_2,
                                      BackgroundType.MEDIUM_CLOUD_3):
            self.__speed_of_cloud = random.randint(1, 4) * -1
            x = random.SystemRandom().randint(self.__game_env.static.screen_width + 10, self.__game_env.static.screen_width + 100)
            y = random.SystemRandom().randint(50, 100)

            # should the cloud be created on left or right ? True: create on left
            if random.choice([True, False]):
                # say screen resolution is 1920x1080, x is 2000 and width of the cloud surface is 500;
                # then x = 1920 - 2000 - 500 = -580
                # cloud will be created at position -580; since the cloud width is 500, so practically the cloud is -80px from left side of the screen
                # the direction of the cloud is controlled by the speed polarity
                x = self.__game_env.static.screen_width - x - self.surf.get_width()
                y = random.SystemRandom().randint(50, 100)
                self.__speed_of_cloud *= -1

            # # speed of small cloud is less, randomly calculating one
            # if self.__background_type in (BackgroundType.SMALL_CLOUD_1, BackgroundType.SMALL_CLOUD_2):
            #     small_cloud_speed = random.randint(1, 3)
            #     self.__speed_of_cloud = small_cloud_speed * -1 if self.__speed_of_cloud < 0 else small_cloud_speed

            # speed of medium cloud is high, randomly calculating one
            elif self.__background_type in (BackgroundType.MEDIUM_CLOUD_1, BackgroundType.MEDIUM_CLOUD_2, BackgroundType.MEDIUM_CLOUD_3):
                y = random.SystemRandom().randint(50, self.__game_env.static.screen_width - 50)
                self.surf.set_colorkey((255, 255, 255), self.__game_env.RLEACCEL)
                medium_cloud_speed = random.randint(5, 10)
                self.__speed_of_cloud = medium_cloud_speed * -1 if self.__speed_of_cloud < 0 else medium_cloud_speed

            position = (x, y)

        self.rect = self.surf.get_rect(topleft=position)

    def update(self) -> None:
        """
        Method to update the game sprite depending on the background type
        """
        if self.__background_type in (BackgroundType.DAY, BackgroundType.NIGHT):
            # move from right to left at speed 1x
            self.rect.move_ip(-1, 0)
            if self.rect.right < 0:
                print(f'killing {self.__background_type}')
                self.kill()

        elif self.__background_type == BackgroundType.MOUNTAIN:
            # move from right to left at speed 3x
            self.rect.move_ip(-6, 0)
            if self.rect.right < 0:
                print(f'killing {self.__background_type}')
                self.kill()

        elif self.__background_type == BackgroundType.DESERT:
            # move from right to left at speed 8x
            self.rect.move_ip(-10, 0)
            if self.rect.right < 0:
                print(f'killing {self.__background_type}')
                self.kill()

        elif self.__background_type == BackgroundType.MOON:
            # moon should move opposite to the direction of the jet
            moon_speed = 1 if self.__game_env.dynamic.jet_movement == JetMovement.LEFT_2_RIGHT else -2
            self.rect.move_ip(moon_speed, 0)

            # moon should not wait at the screen boundary
            if self.rect.right < 0:
                self.rect.x = 0 - self.surf.get_width()
            elif self.rect.left > self.__game_env.static.screen_width:
                self.rect.x = self.__game_env.static.screen_width + self.surf.get_width()

        elif self.__background_type in (BackgroundType.BIG_CLOUD_1,
                                        BackgroundType.BIG_CLOUD_2,
                                        BackgroundType.BIG_CLOUD_3,
                                        BackgroundType.BIG_CLOUD_4,
                                        BackgroundType.BIG_CLOUD_5,
                                        BackgroundType.SMALL_CLOUD_1,
                                        BackgroundType.SMALL_CLOUD_2,
                                        BackgroundType.MEDIUM_CLOUD_1,
                                        BackgroundType.MEDIUM_CLOUD_2,
                                        BackgroundType.MEDIUM_CLOUD_3):
            self.rect.move_ip(self.__speed_of_cloud, 0)
            if self.__speed_of_cloud < 0 and self.rect.right < 0 or self.__speed_of_cloud > 0 and self.rect.left > self.__game_env.static.screen_width:
                print(f'killing {self.__background_type}')
                self.kill()
