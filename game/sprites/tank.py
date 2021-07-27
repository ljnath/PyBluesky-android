import random
from typing import Tuple

from game.data.enums import SoundType
from game.environment import GameEnvironment
from game.sprites.tank_rocket import TankRocket
from pygame import sprite, transform


class Tank(sprite.Sprite):
    """
    Tank sprite class for creating and updating the tank
    """
    def __init__(self):
        """
        Creating the Tank. Tank can randomly come from either Left2Right or from Right2Left.
        It should  travel a minimum distance before actually firing the rocket
        """
        super(Tank, self).__init__()
        self.__game_env = GameEnvironment()

        self.__tank_move = self.__game_env.game_assets.tank_move.copy()
        self.__tank_attack = self.__game_env.game_assets.tank_attack.copy()

        self.__speed = random.randint(5, 10)

        # used to show tank firing animation before actually firing
        self.__read_to_fire = False
        self.__firing_animation_frame_index = 0
        self.__moving_animation_frame_index = 0

        # should the tank travel from left2right or from right2left; True= travel from left2right
        self.__is_left2right = random.choice([True, False])

        # randomly determining if the tank can fire, chance of fire is 33.33%
        self.__can_fire = False if random.choice([0, 1, 2]) == 0 else True

        # threshold distance to cover before firing
        self.__threshold_distance = int(random.randint(20, 30) * self.__game_env.static.screen_width / 100)

        # flip logic, if tank is moving from left2right, all the tank images are flipped
        if self.__is_left2right:
            self.__tank_move[:] = [transform.flip(_surf, True, False) for _surf in self.__tank_move]
            self.__tank_attack[:] = [transform.flip(_surf, True, False) for _surf in self.__tank_attack]
            x_pos = 0
        else:
            # if tank moves from right to left, speed and threshold_distance should be -ve
            self.__speed *= -1
            self.__threshold_distance -= self.__game_env.static.screen_width
            x_pos = self.__game_env.static.screen_width

        # 1st pic of the tank_move list is considered
        self.surf = self.__tank_move[self.__moving_animation_frame_index]

        # tank moves on the desert
        y_pos = self.__game_env.static.screen_height - self.surf.get_height() + 150
        self.rect = self.surf.get_rect(center=(x_pos, y_pos))

    def update(self, target: Tuple[int, int]) -> None:
        """
        Method to update and show the tank move and fire animation
        :param target: target position, used if the tank needs to fire
        """
        if self.__read_to_fire:
            # firing animation is shown
            # if the firing animation image is present, loading it onto the surface; else the fire is triggered
            if self.__firing_animation_frame_index < len(self.__tank_attack) - 1:
                self.surf = self.__tank_attack[self.__firing_animation_frame_index]
            else:
                self.__fire_rocket(target)
                self.__can_fire = False
                self.__read_to_fire = False
            # updating the index of animation image, so that the next frame can be shown
            self.__firing_animation_frame_index += 1
        else:
            # tank moving animation is shown
            # loading the next frame index, resetting to 0 if the frame index is higher then available frames
            self.__moving_animation_frame_index += 1
            if self.__moving_animation_frame_index == len(self.__tank_move):
                self.__moving_animation_frame_index = 0
            self.surf = self.__tank_move[self.__moving_animation_frame_index]

        # if tank can fire and if it has crossed the threshold distance, then the read_to_fire is activated
        # this will show the firing animation and will fire the rocket
        # tank can fire when the jet is in front of on top, it cannot fire in backward direction
        if self.__can_fire and self.rect.x > self.__threshold_distance:
            if self.__speed < 0 and self.surf.get_width() / 2 > target[0] or self.__speed > 0 and target[0] > self.surf.get_width() / 2:
                self.__read_to_fire = True

        # moving tank and killing it is either crosses the left or right of the screen
        self.rect.move_ip(self.__speed, 0)
        if self.__speed < 0 and self.rect.right < 0 or self.__speed > 0 and self.rect.left > self.__game_env.static.screen_width:
            self.kill()

    def __fire_rocket(self, target: Tuple[int, int]) -> None:
        """
        Method to fire rocket from the tank.
        A rocket is created at tank turrent targetted at the jet
        :param target: target position where the rocket need to hit
        """
        game_env = GameEnvironment()

        # the positon of the turrent in frame #5 is (226, 96)
        # calculating the position of the rocket from it, based on whether the tank directon
        # size of the image is 256x256 ; incase the tank is moving from right2left, the turrent position will be (256-x,256-y)
        if self.__is_left2right:
            source = (self.rect.x + 226, self.rect.y + 99)
        else:
            source = (self.rect.x + 256 - 226, self.rect.y + 256 - 99)
        tank_rocket = TankRocket(source, target, self.__is_left2right)

        game_env.dynamic.tank_rockets.add(tank_rocket)
        game_env.dynamic.sprites_to_draw.add(tank_rocket)
        game_env.game_assets.get_sound(SoundType.TANK_FIRE).play()
