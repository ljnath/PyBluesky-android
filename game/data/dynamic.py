
import os
import re

import pygame
from game.data.enums import Choice, Screen
from game.data.static import StaticData


class DynamicData():
    """
    DynamicData class holding all game's dynamic data
    """
    def __init__(self):
        self.__static = StaticData()
        self.__game_surface = None
        self.__main_menu = None
        self.__game_clock = None
        self.__no_ammo_sprite = None
        self.__update_available = False
        self.__update_url = None
        self.__jet_health = 100
        self.__player_name = ''
        self.__all_sprites = pygame.sprite.Group()
        self.__bullets = pygame.sprite.Group()
        self.__sam_missiles = pygame.sprite.Group()
        self.__user_choice = Choice.UNSELECTED
        self.__collision_sound = pygame.mixer.Sound(self.__static.game_sound.get('collision'))
        self.__levelup_sound = pygame.mixer.Sound(self.__static.game_sound.get('levelup'))
        self.__shoot_sound = pygame.mixer.Sound(self.__static.game_sound.get('shoot'))
        self.__hit_sound = pygame.mixer.Sound(self.__static.game_sound.get('hit'))
        self.__powerup_sound = pygame.mixer.Sound(self.__static.game_sound.get('powerup'))
        self.__samfire_sound = pygame.mixer.Sound(self.__static.game_sound.get('samfire'))

        # loading the player name from file, name can be max 20 character long
        if os.path.exists(self.__static.player_file):
            with open(self.__static.player_file) as file_reader:
                name = file_reader.read().strip()[: self.__static.name_length]
                self.__player_name = name if name and re.match(r'[a-zA-Z0-9@. ]', name) else ''

        self.__active_screen = Screen.NAME_INPUT if not self.__player_name else Screen.GAMEPLAY
        self.load_defaults()

    def load_defaults(self):
        """
        Method which resets all game stats for new gameplay or game replay
        """
        self.__ammo = 100
        self.__jet_health = 100
        self.__game_level = 1
        self.__game_score = 0
        self.__game_playtime = 0
        self.__bullet_fired = 0
        self.__missles_destroyed = 0
        self.__sam_missiles.empty()

    @property
    def collision_sound(self) -> pygame.mixer.Sound:
        return self.__collision_sound

    @property
    def levelup_sound(self) -> pygame.mixer.Sound:
        return self.__levelup_sound

    @property
    def shoot_sound(self) -> pygame.mixer.Sound:
        return self.__shoot_sound

    @property
    def hit_sound(self) -> pygame.mixer.Sound:
        return self.__hit_sound

    @property
    def powerup_sound(self) -> pygame.mixer.Sound:
        return self.__powerup_sound

    @property
    def samfire_sound(self) -> pygame.mixer.Sound:
        return self.__samfire_sound

    @property
    def all_sprites(self) -> pygame.sprite.Group:
        return self.__all_sprites

    @all_sprites.setter
    def all_sprites(self, value: pygame.sprite.Group) -> None:
        self.__all_sprites = value

    @property
    def bullets(self) -> pygame.sprite.Group:
        return self.__bullets

    @bullets.setter
    def bullets(self, value: pygame.sprite.Group) -> None:
        self.__bullets = value

    @property
    def sam_missiles(self) -> pygame.sprite.Group:
        return self.__sam_missiles

    @sam_missiles.setter
    def sam_missiles(self, value: pygame.sprite.Group) -> None:
        self.__sam_missiles = value

    @property
    def ammo(self) -> pygame.sprite.Group:
        return self.__ammo

    @ammo.setter
    def ammo(self, value: pygame.sprite.Group) -> None:
        self.__ammo = value if value <= self.__static.max_ammo else self.__static.max_ammo

    @property
    def no_ammo_sprite(self):
        return self.__no_ammo_sprite

    @no_ammo_sprite.setter
    def no_ammo_sprite(self, value) -> None:
        self.__no_ammo_sprite = value

    @property
    def game_level(self) -> int:
        return self.__game_level

    @game_level.setter
    def game_level(self, value: int) -> None:
        self.__game_level = value

    @property
    def update_available(self) -> bool:
        return self.__update_available

    @update_available.setter
    def update_available(self, value: bool) -> None:
        self.__update_available = value

    @property
    def active_screen(self) -> Screen:
        return self.__active_screen

    @active_screen.setter
    def active_screen(self, value: Screen) -> None:
        self.__active_screen = value

    @property
    def game_score(self) -> int:
        return self.__game_score

    @game_score.setter
    def game_score(self, value: int) -> None:
        self.__game_score = value

    @property
    def game_playtime(self) -> int:
        return self.__game_playtime

    @game_playtime.setter
    def game_playtime(self, value: int) -> None:
        self.__game_playtime = value

    @property
    def player_name(self) -> str:
        return self.__player_name

    @player_name.setter
    def player_name(self, value: str) -> None:
        self.__player_name = value
        # saving the player name to file for future reference
        with open(self.__static.player_file, 'w') as file_writter:
            file_writter.write(self.__player_name)

    @property
    def bullets_fired(self) -> int:
        return self.__bullet_fired

    @bullets_fired.setter
    def bullets_fired(self, value: int) -> None:
        self.__bullet_fired = value

    @property
    def missiles_destroyed(self) -> int:
        return self.__missles_destroyed

    @missiles_destroyed.setter
    def missiles_destroyed(self, value: int) -> None:
        self.__missles_destroyed = value

    @property
    def accuracy(self) -> float:
        return 0 if self.bullets_fired == 0 else round(self.missiles_destroyed / self.bullets_fired * 100, 3)

    @property
    def update_url(self) -> str:
        return self.__update_url

    @update_url.setter
    def update_url(self, value: str) -> None:
        self.__update_url = value

    @property
    def game_surface(self) -> pygame.Surface:
        return self.__game_surface

    @game_surface.setter
    def game_surface(self, value: pygame.Surface) -> None:
        self.__game_surface = value

    @property
    def main_menu(self):
        return self.__main_menu

    @main_menu.setter
    def main_menu(self, value) -> None:
        self.__main_menu = value

    @property
    def game_clock(self) -> pygame.time.Clock:
        return self.__game_clock

    @game_clock.setter
    def game_clock(self, value: pygame.time.Clock) -> None:
        self.__game_clock = value

    @property
    def user_choice(self) -> Choice:
        return self.__user_choice

    @user_choice.setter
    def user_choice(self, value: Choice) -> None:
        self.__user_choice = value

    @property
    def jet_health(self) -> int:
        return self.__jet_health

    @jet_health.setter
    def jet_health(self, value: int) -> None:
        self.__jet_health = value
