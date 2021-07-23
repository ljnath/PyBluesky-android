import math

from game.environment import GameEnvironment
from game.sprites.bullet import Bullet
from pygame import image, sprite


# Jet class which holds jet attributes and behaviour
class Jet(sprite.Sprite):
    """ Jet sprite class for creating and updating the jet in the game screen
    """
    def __init__(self):
        super(Jet, self).__init__()                                                         # initilizing parent class pygame.sprite.Sprite
        game_env = GameEnvironment()
        self.surf = image.load(game_env.static.jet_image).convert()                         # loading jet image from file
        self.surf.set_colorkey((255, 255, 255), game_env.RLEACCEL)                          # setting the white color as the transperant area; RLEACCEL is used for better performance on non accelerated displays
        self.rect = self.surf.get_rect(center=(50, game_env.static.screen_height / 2))      # getting rectangle from jet screen; setting the jet position as the middle of the scrren on the left

    def update(self, acceleration_values):
        if not acceleration_values or len(acceleration_values) != 3 or None in acceleration_values:
            return

        # maginfy the acceleration value factor to calculate the projected new jet position
        acceleration_magnify_factor = 50

        x_axis = acceleration_values[0]
        y_axis = acceleration_values[1]

        # calculating projected jet position based on current position and accelertation change
        # the values are reversed as the gameplay will be in landscape mode
        projected_x = self.rect.y + (y_axis * acceleration_magnify_factor)
        projected_y = self.rect.x + (x_axis * acceleration_magnify_factor)

        self.auto_move((projected_x, projected_y))

    def auto_move(self, position):
        speed = 12
        dx = position[0] - self.rect.x                                                                              # calculating x-coordinate difference of mouse and current jet position
        dy = position[1] - self.rect.y                                                                              # caluclating y-coordinate difference of mouse and current jet position
        if (dx >= -speed and dx <= speed) and (dy >= -speed and dy <= speed):                                       # jet will not move if the delta is less then its speed
            return
        angle = math.atan2(dy, dx)                                                                                  # calculating angle
        self.rect.x += speed * math.cos(angle)                                                                      # moving the x-coordinate of jet towards the mouse cursor
        self.rect.y += speed * math.sin(angle)                                                                      # moving the y-coordinate of jet towards the mouse cursor
        self.__maintain_boundary()

    def shoot(self):
        game_env = GameEnvironment()
        if game_env.dynamic.ammo > 0:
            bullet = Bullet(self.rect.x + self.rect.width + 8, self.rect.y + 30)           # create a bullet where the jet is located
            game_env.dynamic.bullets.add(bullet)                                            # add the bullet to bullet group
            game_env.dynamic.all_sprites.add(bullet)                                        # add the bullet tp all_sprites
            game_env.dynamic.shoot_sound.play()                                             # play shooting sound
            game_env.dynamic.ammo -= 1
            game_env.dynamic.bullets_fired += 1
        else:
            game_env.dynamic.all_sprites.add(game_env.dynamic.no_ammo_sprite)               # displaying the hint sprite

    def __maintain_boundary(self):
        game_env = GameEnvironment()
        if self.rect.left < 0:
            self.rect.left = 0                                                                  # if the jet has moved left and have crossed the screen; the left position is set to 0 as it is the boundary
        if self.rect.top < game_env.static.score_sprite_size:
            self.rect.top = game_env.static.score_sprite_size                                  # jet cannot move above the scrore sprite
        if self.rect.right > game_env.static.screen_width:
            self.rect.right = game_env.static.screen_width                                      # if the jet has moved right and have crossed the screen; the right position is set to screen width as it is the boundary
        if self.rect.bottom > game_env.static.screen_height - game_env.vegetation_size[1] / 2:
            self.rect.bottom = game_env.static.screen_height - game_env.vegetation_size[1] / 2   # if the jet has moved bottom and have crossed the screen; the bottom position is set to screen width as it is the boundary
