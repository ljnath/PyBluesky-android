
import json
import os
import re
from datetime import datetime

import pygame
from game.data.enums import Choice, JetMovement, Screen
from game.data.static import StaticData


class DynamicData():
    """
    DynamicData class holding all game's dynamic data
    """
    def __init__(self):
        self.__static = StaticData()
        self.__is_night = True if 19 <= datetime.now().hour <= 23 or 0 <= datetime.now().hour <= 4 else False     # 19:00 Hrs to 4:00 Hrs is considered as night
        self.__game_surface = None
        self.__main_menu = None
        self.__game_clock = None
        self.__no_ammo_sprite = None
        self.__play_background_music = False
        self.__jet_health = 100
        self.__incoming_missiles_rate = self.__static.missile_per_sec
        self.__player_name = 'dev'
        self.__sprites_to_draw = pygame.sprite.Group()
        self.__jet_missiles = pygame.sprite.Group()
        self.__tank_rockets = pygame.sprite.Group()
        self.__user_choice = Choice.UNSELECTED
        self.__jet_movement = JetMovement.LEFT_2_RIGHT

        # loading the player name from file, name can be max 20 character long
        if os.path.exists(self.__static.config_file):
            try:
                self.__load_config()
            except Exception:
                self.__player_name = ''
                self.__play_background_music = True

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
        self.__missiles_fired = 0
        self.__missiles_destroyed = 0
        self.__incoming_missiles_rate = self.__static.missile_per_sec
        self.__tank_rockets.empty()
        self.__sprites_to_draw.empty()

    def __load_config(self) -> None:
        """
        Method to read and load player config file into class variable
        """
        with open(self.__static.config_file) as file_reader:
            config = json.load(file_reader)
            self.__play_background_music = config['background_music']
            name = config['player_name'].strip()[: self.__static.name_length]
            self.__player_name = name if name and re.match(r'[a-zA-Z0-9@. ]', name) else ''

    def __save_config(self) -> None:
        """
        Method to same user config (player-name & music playback) option to file
        """
        with open(self.__static.config_file, 'w') as file_handler:
            config = {'player_name': self.__player_name,
                      'background_music': self.__play_background_music
                      }
            json.dump(config, file_handler)

    @property
    def is_night(self) -> bool:
        """
        Property which checks the current time and determins if it is day or night
        :return : True if night else False
        """
        return self.__is_night

    @property
    def sprites_to_draw(self) -> pygame.sprite.Group:
        return self.__sprites_to_draw

    @sprites_to_draw.setter
    def sprites_to_draw(self, value: pygame.sprite.Group) -> None:
        self.__sprites_to_draw = value

    @property
    def jet_missiles(self) -> pygame.sprite.Group:
        return self.__jet_missiles

    @jet_missiles.setter
    def jet_missiles(self, value: pygame.sprite.Group) -> None:
        self.__jet_missiles = value

    @property
    def tank_rockets(self) -> pygame.sprite.Group:
        return self.__tank_rockets

    @tank_rockets.setter
    def tank_rockets(self, value: pygame.sprite.Group) -> None:
        self.__tank_rockets = value

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
        self.__save_config()

    @property
    def play_music(self) -> bool:
        """
        Property indicating if the background music needs to be played or not
        """
        return self.__play_background_music

    @play_music.setter
    def play_music(self, value: bool) -> None:
        self.__play_background_music = value
        self.__save_config()

    @property
    def missiles_fired(self) -> int:
        return self.__missiles_fired

    @missiles_fired.setter
    def missiles_fired(self, value: int) -> None:
        self.__missiles_fired = value

    @property
    def missiles_destroyed(self) -> int:
        return self.__missiles_destroyed

    @missiles_destroyed.setter
    def missiles_destroyed(self, value: int) -> None:
        self.__missiles_destroyed = value

    @property
    def accuracy(self) -> float:
        return 0 if self.missiles_fired == 0 else round(self.missiles_destroyed / self.missiles_fired * 100, 3)

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

    @property
    def jet_movement(self) -> JetMovement:
        return self.__jet_movement

    @jet_movement.setter
    def jet_movement(self, value: JetMovement) -> None:
        self.__jet_movement = value

    @property
    def incoming_missiles_rate(self) -> int:
        return self.__incoming_missiles_rate

    @incoming_missiles_rate.setter
    def incoming_missiles_rate(self, value: int) -> None:
        self.__incoming_missiles_rate = value
