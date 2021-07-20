
import os
import re

from pygame.mixer import Sound
from pygame.sprite import Group

from game.data.enums import Screen, StartChoice
from game.data.static import StaticData


class DynamicData():
    """ Class which holds all the game variables
    """
    def __init__(self):
        self.__static = StaticData()
        self.__game_surface = None
        self.__main_menu = None
        self.__game_clock = None
        self.__pause_menu = None
        self.__collision_sound = Sound(self.__static.game_sound.get('collision'))
        self.__levelup_sound = Sound(self.__static.game_sound.get('levelup'))
        self.__shoot_sound = Sound(self.__static.game_sound.get('shoot'))
        self.__hit_sound = Sound(self.__static.game_sound.get('hit'))
        self.__powerup_sound = Sound(self.__static.game_sound.get('powerup'))
        self.__samfire_sound = Sound(self.__static.game_sound.get('samfire'))
        self.__game_start_choice = StartChoice.START
        self.__all_sprites = Group()
        self.__bullets = Group()
        self.__sam_missiles = Group()
        self.__no_ammo_sprite = None
        self.__update_available = False
        self.__replay = True
        self.__exit = False
        self.__update_url = None
        self.__player_name = ''

        # loading the player name from file, name can be max 20 character long
        if os.path.exists(self.__static.player_file):
            with open(self.__static.player_file) as file_reader:
                name = file_reader.read().strip()[: self.__static.name_length]
                self.__player_name = name if name and re.match(r'[a-zA-Z0-9@. ]', name) else ''

        self.__active_screen = Screen.NAME_INPUT if not self.__player_name else Screen.GAME_MENU
        self.load_defaults()

    def load_defaults(self):
        self.__ammo = 100
        self.__game_level = 1
        self.__game_score = 0
        self.__game_playtime = 0
        self.__bullet_fired = 0
        self.__missles_destroyed = 0
        self.__sam_missiles.empty()

    @property
    def collision_sound(self):
        return self.__collision_sound

    @property
    def levelup_sound(self):
        return self.__levelup_sound

    @property
    def shoot_sound(self):
        return self.__shoot_sound

    @property
    def hit_sound(self):
        return self.__hit_sound

    @property
    def powerup_sound(self):
        return self.__powerup_sound

    @property
    def samfire_sound(self):
        return self.__samfire_sound

    @property
    def game_start_choice(self):
        return self.__game_start_choice

    @game_start_choice.setter
    def game_start_choice(self, value):
        self.__game_start_choice = value

    @property
    def all_sprites(self):
        return self.__all_sprites

    @all_sprites.setter
    def all_sprites(self, value):
        self.__all_sprites = value

    @property
    def bullets(self):
        return self.__bullets

    @bullets.setter
    def bullets(self, value):
        self.__bullets = value

    @property
    def sam_missiles(self):
        return self.__sam_missiles

    @sam_missiles.setter
    def sam_missiles(self, value):
        self.__sam_missiles = value

    @property
    def ammo(self):
        return self.__ammo

    @ammo.setter
    def ammo(self, value):
        self.__ammo = value if value <= self.__static.max_ammo else self.__static.max_ammo

    @property
    def no_ammo_sprite(self):
        return self.__no_ammo_sprite

    @no_ammo_sprite.setter
    def no_ammo_sprite(self, value):
        self.__no_ammo_sprite = value

    @property
    def game_level(self):
        return self.__game_level

    @game_level.setter
    def game_level(self, value):
        self.__game_level = value

    @property
    def update_available(self):
        return self.__update_available

    @update_available.setter
    def update_available(self, value):
        self.__update_available = value

    @property
    def active_screen(self):
        return self.__active_screen

    @active_screen.setter
    def active_screen(self, value):
        self.__active_screen = value

    @property
    def game_score(self):
        return self.__game_score

    @game_score.setter
    def game_score(self, value):
        self.__game_score = value

    @property
    def game_playtime(self):
        return self.__game_playtime

    @game_playtime.setter
    def game_playtime(self, value):
        self.__game_playtime = value

    @property
    def replay(self):
        return self.__replay

    @replay.setter
    def replay(self, value):
        self.__replay = value

    @property
    def exit(self):
        return self.__exit

    @exit.setter
    def exit(self, value):
        self.__exit = value

    @property
    def player_name(self):
        return self.__player_name

    @player_name.setter
    def player_name(self, value):
        self.__player_name = value
        # saving the player name to file for future reference
        with open(self.__static.player_file, 'w') as file_writter:
            file_writter.write(self.__player_name)

    @property
    def bullets_fired(self):
        return self.__bullet_fired

    @bullets_fired.setter
    def bullets_fired(self, value):
        self.__bullet_fired = value

    @property
    def missiles_destroyed(self):
        return self.__missles_destroyed

    @missiles_destroyed.setter
    def missiles_destroyed(self, value):
        self.__missles_destroyed = value

    @property
    def accuracy(self):
        return 0 if self.bullets_fired == 0 else round(self.missiles_destroyed / self.bullets_fired * 100, 3)

    @property
    def update_url(self):
        return self.__update_url

    @update_url.setter
    def update_url(self, value):
        self.__update_url = value

    @property
    def game_surface(self):
        return self.__game_surface

    @game_surface.setter
    def game_surface(self, value):
        self.__game_surface = value

    @property
    def main_menu(self):
        return self.__main_menu

    @main_menu.setter
    def main_menu(self, value):
        self.__main_menu = value

    @property
    def pause_menu(self):
        return self.__pause_menu

    @pause_menu.setter
    def pause_menu(self, value):
        self.__pause_menu = value

    @property
    def game_clock(self):
        return self.__game_clock

    @game_clock.setter
    def game_clock(self, value):
        self.__game_clock = value
