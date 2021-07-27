import math
from typing import Tuple

from game.data.enums import JetMovement, SoundType
from game.environment import GameEnvironment
from game.sprites.jet_missile import JetMissile
from pygame import sprite


class Jet(sprite.Sprite):
    """
    Jet sprite class for creating and updating the jet in the game screen
    """
    def __init__(self):
        """
        Creating the jet
        """
        super(Jet, self).__init__()                                                         # initilizing parent class pygame.sprite.Sprite
        game_env = GameEnvironment()
        self.surf = game_env.game_assets.jet
        self.rect = self.surf.get_rect(center=(50, game_env.static.screen_height / 2))      # getting rectangle from jet screen; setting the jet position as the middle of the scrren on the left
        self.__speed = 18

    def update(self, acceleration_values: Tuple[int, int, int]) -> None:
        """
        Method to update the jet based on acceleration values
        :param acceleration_values : Accleration value in (x-axis, y-axis, z-axis) format
        """
        game_env = GameEnvironment()
        if not acceleration_values or len(acceleration_values) != 3 or None in acceleration_values:
            return

        # maginfy the acceleration value factor to calculate the projected new jet position
        acceleration_magnify_factor = 80

        target_x = acceleration_values[0]
        target_y = acceleration_values[1]

        # calculating projected jet position based on current position and accelertation change
        # the values are reversed as the gameplay will be in landscape mode
        projected_x = self.rect.y + (target_y * acceleration_magnify_factor)
        projected_y = self.rect.x + (target_x * acceleration_magnify_factor)

        # determining the jet movement based on current and projected jet position and storing in environment variable
        game_env.dynamic.jet_movement = JetMovement.LEFT_2_RIGHT if projected_x > self.rect.x else JetMovement.RIGHT_2_LEFT

        self.auto_move((projected_x, projected_y))

    def update_on_keypress(self, pressed_keys):
        """
        Method to update the jet based on keyboard key press
        """
        game_env = GameEnvironment()
        if pressed_keys[game_env.K_UP]:                                     # if the UP key is pressed
            self.rect.move_ip(0, -self.__speed)                             # moving the jet on negtaive y-axis
        if pressed_keys[game_env.K_DOWN]:                                   # if the DOWN key is pressed
            self.rect.move_ip(0, self.__speed)                              # moving the jet on positive y-axis
        if pressed_keys[game_env.K_LEFT]:                                   # if the LEFT key is presssed
            game_env.dynamic.jet_movement = JetMovement.LEFT_2_RIGHT
            self.rect.move_ip(-self.__speed, 0)                             # moving the jet on negative x-axis
        if pressed_keys[game_env.K_RIGHT]:                                  # if the RIGHT key is pressed
            game_env.dynamic.jet_movement = JetMovement.RIGHT_2_LEFT
            self.rect.move_ip(self.__speed, 0)                              # moving the jet on positive x-axis
        self.__maintain_boundary()

    def auto_move(self, position: Tuple[int, int]) -> None:
        """
        Method to auto move the jet to the target position
        :param position : Target position (x_pos, y_pos) where the jet needs to move to
        """
        dx = position[0] - self.rect.x                                                                              # calculating x-coordinate difference of mouse and current jet position
        dy = position[1] - self.rect.y                                                                              # caluclating y-coordinate difference of mouse and current jet position
        if (dx >= -self.__speed and dx <= self.__speed) and (dy >= -self.__speed and dy <= self.__speed):           # jet will not move if the delta is less then its speed
            return
        angle = math.atan2(dy, dx)                                                                                  # calculating angle
        self.rect.x += self.__speed * math.cos(angle)                                                               # moving the x-coordinate of jet towards the mouse cursor
        self.rect.y += self.__speed * math.sin(angle)                                                               # moving the y-coordinate of jet towards the mouse cursor
        self.__maintain_boundary()

    def shoot(self) -> None:
        """
        Method to shoot bullets. A bullet sprite is created near to the jet to simulate the jet firing a bullet
        """
        game_env = GameEnvironment()
        if game_env.dynamic.ammo > 0:
            x = self.rect.x + self.rect.width + 8
            y = self.rect.y + 30
            jet_missile = JetMissile((x, y))                                                # create a jet missile from the wings of the jet
            game_env.dynamic.jet_missiles.add(jet_missile)                                  # add the jet missile to jet_missile group
            game_env.dynamic.sprites_to_draw.add(jet_missile)                               # add the jet missile to sprites_to_draw for drawing on screen
            game_env.dynamic.ammo -= 1
            game_env.dynamic.missiles_fired += 1
            game_env.game_assets.get_sound(SoundType.SHOOT).play()                          # play shooting sound
        else:
            game_env.dynamic.sprites_to_draw.add(game_env.dynamic.no_ammo_sprite)           # displaying the hint sprite

    def __maintain_boundary(self) -> None:
        """
        Method to prevent the jet from leaving the game screen
        """
        game_env = GameEnvironment()
        if self.rect.left < 0:
            self.rect.left = 0                                                                  # if the jet has moved left and have crossed the screen; the left position is set to 0 as it is the boundary
        if self.rect.top < 10:
            self.rect.top = 10                                                                  # jet cannot move 10 px
        if self.rect.right > game_env.static.screen_width:
            self.rect.right = game_env.static.screen_width                                      # jet cannot move outside the screen width towards right
        if self.rect.bottom > game_env.static.jet_bottom_boundry:
            self.rect.bottom = game_env.static.jet_bottom_boundry                               # jet cannot move below the jet_bottom_boundry
