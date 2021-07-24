
from typing import Dict, Tuple

import urllib3
from android.storage import app_storage_path


class StaticData():
    """
    Class which holds all the static game values
    """
    def __init__(self):
        # initializing urllib3.PoolManager with default timeout of 3s and pool count as 2
        self.__http_pool_manager = urllib3.PoolManager(num_pools=2, timeout=3)

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
        return '1.0.0'

    @property
    def screen_width(self):
        """
        Width of the game screen, fixed to 1920 so that it scales automatically when actual size is different from this
        """
        return 1920

    @property
    def screen_height(self):
        """
        Height of the game screen, fixed to 1080 so that it scales automatically when actual size is different from this
        """
        return 1080

    @property
    def http_pool_manager(self) -> urllib3.PoolManager:
        """
        HTTP pool used for all network communication
        """
        return self.__http_pool_manager

    @property
    def cloud_per_sec(self) -> int:
        """
        Number of clouds that needs to be created per second
        """
        return 1

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
        return 60

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
    def android_app_directory(self) -> str:
        """
        Absolute path of the android app directory
        """
        return f'{app_storage_path()}/app'

    @property
    def images_asset_directory(self) -> str:
        """
        Absolute path of the images directory
        """
        return f'{self.android_app_directory}/assets/images'

    @property
    def audio_asset_directory(self) -> str:
        """
        Absolute path of the audio directory
        """
        return f'{self.android_app_directory}/assets/audio'

    @property
    def fonts_asset_directory(self) -> str:
        """
        Absolute path of the font directory
        """
        return f'{self.android_app_directory}/assets/fonts'

    @property
    def icon_asset_directory(self) -> str:
        """
        Absolute path of the icon directory
        """
        return f'{self.android_app_directory}/assets/icon'

    @property
    def game_font(self) -> str:
        return f'{self.fonts_asset_directory}/arcade.ttf'               # game font file path

    @property
    def game_log_file(self) -> str:
        """
        Absolute path to the game log file
        """
        return f'{self.android_app_directory}/game.log'

    @property
    def leaders_file(self) -> str:
        """
        Absolute path of the leaders file
        """
        return f'{self.android_app_directory}/leaders.dat'

    @property
    def offline_score_file(self) -> str:
        """
        Absolute path of the leaders file
        """
        return f'{self.android_app_directory}/offline.dat'

    @property
    def player_file(self) -> str:
        """
        Absolute path to the player name file
        """
        return f'{self.android_app_directory}/player.dat'

    @property
    def clouds(self) -> Tuple[str, str, str]:
        """
        Property to return a tuple of all available cloud images
        """
        return (
            f'{self.images_asset_directory}/cloud1.png',
            f'{self.images_asset_directory}/cloud2.png',
            f'{self.images_asset_directory}/cloud3.png'
        )

    @property
    def vegetation(self) -> Tuple[str, str]:
        """
        Property to return a tuple of all available vegetation images
        """
        return (
            f'{self.images_asset_directory}/vegetation_plain.png',
            f'{self.images_asset_directory}/vegetation_tree.png'
        )

    @property
    def ground(self) -> str:
        return f'{self.images_asset_directory}/ground.png'

    @property
    def grass(self) -> str:
        return f'{self.images_asset_directory}/grass.png'

    @property
    def sam_launcher(self) -> str:
        return f'{self.images_asset_directory}/samlauncher.png'

    @property
    def sam(self) -> str:
        return f'{self.images_asset_directory}/sam.png'

    @property
    def missile_activated_image(self) -> str:
        return f'{self.images_asset_directory}/missile_activated.png'

    @property
    def missile_deactivated_image(self) -> str:
        return f'{self.images_asset_directory}/missile_deactivated.png'

    @property
    def jet_image(self) -> str:
        return f'{self.images_asset_directory}/jet.png'

    @property
    def powerup_image(self) -> str:
        return f'{self.images_asset_directory}/star.png'

    @property
    def bullet_image(self) -> str:
        return f'{self.images_asset_directory}/bullet.png'

    @property
    def game_sound(self) -> Dict[str: str]:
        """
        Absolute path to all the available game sounds
        """
        return {
            'music': f'{self.audio_asset_directory}/music.ogg',
            'collision': f'{self.audio_asset_directory}/collision.ogg',
            'levelup': f'{self.audio_asset_directory}/levelup.ogg',
            'shoot': f'{self.audio_asset_directory}/shoot.ogg',
            'hit': f'{self.audio_asset_directory}/missile_hit.ogg',
            'powerup': f'{self.audio_asset_directory}/powerup.ogg',
            'samfire': f'{self.audio_asset_directory}/fire.ogg'
        }
