from pygame import display
from android.storage import app_storage_path


class StaticData():
    """ Class which holds all the static game values
    """
    def __init__(self):
        self.__display_info = display.Info()                        # get current display information

    @property
    def name(self):
        return 'PyBluesky'

    @property
    def version(self):
        return '1.0.1'

    @property
    def android_app_directory(self):
        return f'{app_storage_path()}/app'

    @property
    def images_asset_directory(self):
        return f'{self.android_app_directory}/assets/images'

    @property
    def audio_asset_directory(self):
        return f'{self.android_app_directory}/assets/audio'

    @property
    def fonts_asset_directory(self):
        return f'{self.android_app_directory}/assets/fonts'

    @property
    def icon_asset_directory(self):
        return f'{self.android_app_directory}/assets/icon'

    @property
    def game_log_file(self):
        return f'{self.android_app_directory}/game.log'

    @property
    def leaders_file(self):
        return f'{self.android_app_directory}/leaders.dat'

    @property
    def offline_score_file(self):
        return f'{self.android_app_directory}/offline.dat'

    @property
    def screen_width(self):
        # setting fixed screen width for scaling
        return 1280

    @property
    def screen_height(self):
        # setting fixed screen height for scaling
        return 720

    @property
    def text_default_color(self):
        return (255, 0, 0)                                            # default color is red

    @property
    def text_selection_color(self):
        return (0, 0, 255)                                            # selection color is blue

    @property
    def game_font(self):
        return f'{self.fonts_asset_directory}/arcade.ttf'               # game font file path

    @property
    def clouds(self):
        return (
            f'{self.images_asset_directory}/cloud1.png',
            f'{self.images_asset_directory}/cloud2.png',
            f'{self.images_asset_directory}/cloud3.png'
        )                                                               # all game cloud designs

    @property
    def vegetation(self):
        return (
            f'{self.images_asset_directory}/vegetation_plain.png',
            f'{self.images_asset_directory}/vegetation_tree.png'
        )

    @property
    def ground(self):
        return f'{self.images_asset_directory}/ground.png'

    @property
    def grass(self):
        return f'{self.images_asset_directory}/grass.png'

    @property
    def sam_launcher(self):
        return f'{self.images_asset_directory}/samlauncher.png'

    @property
    def sam(self):
        return f'{self.images_asset_directory}/sam.png'

    @property
    def missile_activated_image(self):
        return f'{self.images_asset_directory}/missile_activated.png'    # missle image path

    @property
    def missile_deactivated_image(self):
        return f'{self.images_asset_directory}/missile_deactivated.png'  # missle image path

    @property
    def jet_image(self):
        return f'{self.images_asset_directory}/jet.png'                  # jet image path

    @property
    def powerup_image(self):
        return f'{self.images_asset_directory}/star.png'                 # jet image path

    @property
    def bullet_image(self):
        return f'{self.images_asset_directory}/bullet.png'               # bullet image path

    @property
    def cloud_per_sec(self):
        return 1                            # number of cloud to be spawned per second

    @property
    def missile_per_sec(self):
        return 2                            # number of missiles to be spawned per seconds

    @property
    def background_default(self):
        return (208, 244, 247)              # skyblue color

    @property
    def background_special(self):
        return (196, 226, 255)              # pale skyblue

    @property
    def fps(self):
        return 30                           # game should run at 30 pfs

    @property
    def max_ammo(self):
        return 999

    @property
    def player_file(self):
        return f'{self.android_app_directory}/player.dat'

    @property
    def name_length(self):
        return 12

    @property
    def score_sprite_width(self):
        return 40
    
    @property
    def game_sound(self):
        return {
            'music': f'{self.audio_asset_directory}/music.ogg',
            'collision': f'{self.audio_asset_directory}/collision.ogg',
            'levelup': f'{self.audio_asset_directory}/levelup.ogg',
            'shoot': f'{self.audio_asset_directory}/shoot.ogg',
            'hit': f'{self.audio_asset_directory}/missile_hit.ogg',
            'powerup': f'{self.audio_asset_directory}/powerup.ogg',
            'samfire': f'{self.audio_asset_directory}/fire.ogg'
        }
