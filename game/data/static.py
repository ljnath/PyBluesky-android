import os
from typing import Tuple

import urllib3
from game import IS_ANDROID

if IS_ANDROID:
    from android.storage import app_storage_path


class StaticData():
    """
    Class which holds all the static game values
    """
    def __init__(self):
        # initializing urllib3.PoolManager with default timeout of 3s and pool count as 2
        self.__http_pool_manager = urllib3.PoolManager(num_pools=2, timeout=3)
        self.__app_directory = None

        mountain_vertical_space_in_percent = 60.5
        desert_vertical_space_in_percent = 90.8
        tank_vertical_space_in_percent = 89.8
        jet_max_vertical_space_in_percent = 69.33
        scoretext_vertical_space_in_percent = 100

        self.__mountain_vertical_position = int(self.screen_height * mountain_vertical_space_in_percent / 100)
        self.__desert_vertical_position = int(self.screen_height * desert_vertical_space_in_percent / 100)
        self.__tank_vertical_position = int(self.screen_height * tank_vertical_space_in_percent / 100)
        self.__max_jet_vertical_position = int(self.screen_height * jet_max_vertical_space_in_percent / 100)
        self.__scoretext_vertical_position = int(self.screen_height * scoretext_vertical_space_in_percent / 100)

    @property
    def app_name(self) -> str:
        """
        Application name
        """
        return 'PyBluesky'

    @property
    def app_version(self) -> str:
        """
        Application version
        """
        return '1.1.0'

    @property
    def screen_width(self):
        """
        Width of the game screen, fixed to 1920 so that it scales automatically when actual size is different from this
        """
        return 1280 if IS_ANDROID else 1920

    @property
    def screen_height(self):
        """
        Height of the game screen, fixed to 1080 so that it scales automatically when actual size is different from this
        """
        return 720  if IS_ANDROID else 1080

    @property
    def http_pool_manager(self) -> urllib3.PoolManager:
        """
        HTTP pool used for all network communication
        """
        return self.__http_pool_manager

    @property
    def big_cloud_interval(self) -> int:
        """
        Interval in second after which a big cloud needs to be created
        """
        return 15

    @property
    def small_cloud_interval(self) -> int:
        """
        Interval in second after which a small cloud needs to be created
        """
        return 10

    @property
    def missile_per_sec(self) -> int:
        """
        Number of missiles that needs to be created per second
        """
        return 1

    @property
    def fps(self) -> int:
        """
        Maximum FPS of the game
        """
        return 30

    @property
    def max_ammo(self) -> int:
        """
        Maximum allowed ammo
        """
        return 999

    @property
    def name_length(self) -> int:
        """
        Maximum allowed length of the player name
        """
        return 12

    @property
    def score_sprite_size(self) -> int:
        """
        Size of the score text sprite
        """
        return int(self.screen_height * 4 / 100)

    @property
    def tank_activates_at(self) -> int:
        """
        Game level when the tank activates
        """
        return 6

    @property
    def jet_bottom_boundry(self) -> int:
        """
        Property which defines the bottom boundary of a jet.
        The same property is also used for incoming missile creation
        """
        return self.__max_jet_vertical_position

    @property
    def mountain_horizontal_position(self) -> int:
        """
        Position of mountain from top mountain will start after distance_from_top_in_percent %
        """
        return self.__mountain_vertical_position

    @property
    def desert_horizontal_position(self) -> int:
        """
        Position of desert from top
        """
        return self.__desert_vertical_position

    @property
    def tank_horizontal_position(self) -> int:
        """
        Position of tank from top
        """
        return self.__tank_vertical_position

    @property
    def scoretext_horizontal_position(self) -> int:
        """
        Position of scoretext from top
        """
        return self.__scoretext_vertical_position

    @property
    def text_default_color(self) -> Tuple[int, int, int]:
        """
        Color of game texts; default is red
        """
        return (240, 0, 0)

    @property
    def text_selection_color(self) -> Tuple[int, int, int]:
        """
        Color of game texts when selected; default is blue
        """
        return (0, 0, 240)

    @property
    def background_greenish_blue(self) -> Tuple[int, int, int]:
        """
        Background color used during the gameplay
        """
        return (208, 244, 247)

    @property
    def background_skyblue(self) -> Tuple[int, int, int]:
        """
        Background color used in game menu and name-input menu
        """
        return (196, 226, 255)

    @property
    def app_directory(self) -> str:
        """
        Absolute path of the app directory
        If the app directory is not present, then is evaluated based on environment, stored and returned
        """
        if not self.__app_directory:
            if IS_ANDROID:
                return f'{app_storage_path()}/app'
            else:
                import os
                from pathlib import Path
                current_filepath = Path(os.path.realpath(__file__))
                self.__app_directory = str(current_filepath.parent.parent.parent.absolute())

        return self.__app_directory

    @property
    def images_asset_directory(self) -> str:
        """
        Absolute path of the images directory
        """
        return os.path.join(self.app_directory, 'assets', 'images')

    @property
    def sounds_asset_directory(self) -> str:
        """
        Absolute path of the sounds directory
        """
        return os.path.join(self.app_directory, 'assets', 'sounds')

    @property
    def fonts_asset_directory(self) -> str:
        """
        Absolute path of the font directory
        """
        return os.path.join(self.app_directory, 'assets', 'fonts')

    @property
    def icon_asset_directory(self) -> str:
        """
        Absolute path of the icon directory
        """
        return os.path.join(self.app_directory, 'assets', 'icons')

    @property
    def game_log_file(self) -> str:
        """
        Absolute path to the game log file
        """
        return f'{self.app_directory}/game.log'

    @property
    def leaders_file(self) -> str:
        """
        Absolute path of the leaders file
        """
        return f'{self.app_directory}/leaders.dat'

    @property
    def offline_score_file(self) -> str:
        """
        Absolute path of the leaders file
        """
        return f'{self.app_directory}/scores.dat'

    @property
    def config_file(self) -> str:
        """
        Absolute path to the player name file
        """
        return f'{self.app_directory}/config.dat'
