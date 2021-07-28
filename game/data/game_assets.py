from typing import List

import pygame
from game import IS_ANDROID
from game.data.enums import BackgroundType, SoundType
from game.data.static import StaticData


class GameAssets():
    def __init__(self) -> None:
        self.__static = StaticData()

    def initialize(self):
        """
        Method to initialize the game assets class
        """
        image_resolution = 720 if IS_ANDROID else 1080
        # creating surfaces from all the moving tank images; total of 8 images.
        # flipping all the images as well becuase the original images are reversed
        self.__tank_move = [pygame.image.load(f'{self.__static.images_asset_directory}/tank_move_{i}.png').convert_alpha() for i in range(1, 9)]
        self.__tank_move[:] = [pygame.transform.flip(_surf, True, False) for _surf in self.__tank_move]

        # creating surfaces from all the attacking tank images; total of 8 images
        self.__tank_attack = [pygame.image.load(f'{self.__static.images_asset_directory}/tank_attack_{i}.png').convert_alpha() for i in range(1, 9)]
        self.__tank_attack[:] = [pygame.transform.flip(_surf, True, False) for _surf in self.__tank_attack]

        # creating surfaces from all the big cloud tank images; total of 5 images
        self.__big_clouds = [pygame.image.load(f'{self.__static.images_asset_directory}/{image_resolution}/big_cloud_{i}.png').convert_alpha() for i in range(1, 6)]

        # creating surfaces from all the small cloud tank images; total of 2 images
        self.__small_clouds = [pygame.image.load(f'{self.__static.images_asset_directory}/{image_resolution}/small_cloud_{i}.png').convert_alpha() for i in range(1, 3)]

        # creating surfaces from the medium clouds; total of 3 images
        self.__medium_clouds = [pygame.image.load(f'{self.__static.images_asset_directory}/cloud{i}.png').convert(24) for i in range(1, 4)]

        self.__mountain = pygame.image.load(f'{self.__static.images_asset_directory}/{image_resolution}/mountain.png').convert_alpha()
        self.__desert = pygame.image.load(f'{self.__static.images_asset_directory}/{image_resolution}/desert.png').convert_alpha()
        self.__background_day = pygame.image.load(f'{self.__static.images_asset_directory}/{image_resolution}/bg_sky.png').convert(24)
        self.__background_night = pygame.image.load(f'{self.__static.images_asset_directory}/{image_resolution}/bg_star.png').convert(24)

        self.__jet = pygame.image.load(f'{self.__static.images_asset_directory}/{image_resolution}/jet.png').convert_alpha()
        self.__jet_missile = pygame.image.load(f'{self.__static.images_asset_directory}/{image_resolution}/jet_missile.png').convert_alpha()
        self.__tank_rocket = pygame.image.load(f'{self.__static.images_asset_directory}/{image_resolution}/tank_rocket.png').convert_alpha()
        self.__incoming_missile_activated = pygame.image.load(f'{self.__static.images_asset_directory}/{image_resolution}/missile_activated.png').convert_alpha()
        self.__incoming_missile_deactivated = pygame.image.load(f'{self.__static.images_asset_directory}/{image_resolution}/missile_deactivated.png').convert_alpha()

        self.__moon = pygame.image.load(f'{self.__static.images_asset_directory}/{image_resolution}/moon.jpg').convert(24)
        self.__powerup_star = pygame.image.load(f'{self.__static.images_asset_directory}/star.png').convert()
        self.__health_surface = pygame.image.load(f'{self.__static.images_asset_directory}/heart.png').convert_alpha()

        self.__background_surfaces = {
            BackgroundType.DAY: self.__background_day,
            BackgroundType.NIGHT: self.__background_night,
            BackgroundType.MOUNTAIN: self.__mountain,
            BackgroundType.DESERT: self.__desert,
            BackgroundType.MOON: self.__moon,
            BackgroundType.BIG_CLOUD_1: self.__big_clouds[0],
            BackgroundType.BIG_CLOUD_2: self.__big_clouds[1],
            BackgroundType.BIG_CLOUD_3: self.__big_clouds[2],
            BackgroundType.BIG_CLOUD_4: self.__big_clouds[3],
            BackgroundType.BIG_CLOUD_5: self.__big_clouds[4],
            BackgroundType.SMALL_CLOUD_1: self.__small_clouds[0],
            BackgroundType.SMALL_CLOUD_2: self.__small_clouds[1],
            BackgroundType.MEDIUM_CLOUD_1: self.__medium_clouds[0],
            BackgroundType.MEDIUM_CLOUD_2: self.__medium_clouds[1],
            BackgroundType.MEDIUM_CLOUD_3: self.__medium_clouds[2],
        }

        self.__sounds = {
            SoundType.MISSILE_COLLISION: pygame.mixer.Sound(f'{self.__static.sounds_asset_directory}/missile_collision.ogg'),
            SoundType.MISSILE_HIT: pygame.mixer.Sound(f'{self.__static.sounds_asset_directory}/missile_hit.ogg'),
            SoundType.LEVEL_UP: pygame.mixer.Sound(f'{self.__static.sounds_asset_directory}/level_up.ogg'),
            SoundType.POWER_UP: pygame.mixer.Sound(f'{self.__static.sounds_asset_directory}/power_up.ogg'),
            SoundType.SHOOT: pygame.mixer.Sound(f'{self.__static.sounds_asset_directory}/shoot.ogg'),
            SoundType.TANK_FIRE: pygame.mixer.Sound(f'{self.__static.sounds_asset_directory}/tank_fire.ogg'),
        }

        self.__music_filepath = f'{self.__static.sounds_asset_directory}/music.ogg'
        self.__font_surfaces = {}  # empty dict for storing fonts of various size

        # creating an filling all the health surfaces
        self.__health_surfaces = {}
        self.__create_healthbar_surfaces()

    def __create_healthbar_surfaces(self):
        """
        method to create all the possible health surfaces
        """
        # possible health surfaces are 5, as maxhealth is 100 and damange value is 20; 100/20=5
        for heart_count in range(1, 6):
            health_surface = pygame.Surface((self.__health_surface.get_width() * heart_count, self.__health_surface.get_height()), pygame.SRCALPHA, 32)
            for i in range(heart_count):
                health_surface.blit(self.__health_surface, (i * self.__health_surface.get_width(), 0))
            self.__health_surfaces.update({heart_count: health_surface})

        # inserting empty surface of 1x1 for 0 health
        self.__health_surfaces.update({0: pygame.Surface((1, 1), pygame.SRCALPHA, 32)})

    def get_sound(self, type: SoundType) -> pygame.mixer.Sound:
        """
        Method to get the absolute path of the sound file of type 'type'
        :param type : SoundType, type of sound
        :return : instance og pygame.mixer.Sound created from appropriate sound file
        """
        return self.__sounds.get(type)

    def get_image(self, type: BackgroundType) -> pygame.Surface:
        """
        Method to get the image surface
        :param type : BackgroundType , type of background image
        :return : instance of pygame.Suface created from the image file
        """
        return self.__background_surfaces.get(type)

    def get_font(self, size: int) -> pygame.font.Font:
        """
        Method to a get an instance of pygame.font.Font created from defaut game font and input size.
        If the font is not present, it is created and stored in a dict, else the pre-existing is returned
        :param size : size of font
        :return : instance of pygame.font.Font created from game font of given size
        """
        if size not in self.__font_surfaces.keys():
            self.__font_surfaces.update({size: pygame.font.Font(f'{self.__static.fonts_asset_directory}/arcade.ttf', size)})
        return self.__font_surfaces.get(size)

    def get_health(self, health: int) -> pygame.Surface:
        """
        Method to create a health surface from for the input health.
        If the font is not present, it is created and stored in a dict, else the pre-existing surface is returned
        :param health : health of the jet
        :return : instance of pygame.Suface created from given health
        """
        heart_count = health // 20
        return self.__health_surfaces.get(heart_count)
    
    @property
    def tank_move(self) -> List[pygame.Surface]:
        return self.__tank_move

    @property
    def tank_attack(self) -> List[pygame.Surface]:
        return self.__tank_attack

    @property
    def jet(self) -> pygame.Surface:
        return self.__jet

    @property
    def jet_missile(self) -> pygame.Surface:
        return self.__jet_missile

    @property
    def tank_rocket(self) -> pygame.Surface:
        return self.__tank_rocket

    @property
    def incoming_missile_activated(self) -> pygame.Surface:
        return self.__incoming_missile_activated

    @property
    def incoming_missile_deactivated(self) -> pygame.Surface:
        return self.__incoming_missile_deactivated

    @property
    def powerup_star(self) -> pygame.Surface:
        return self.__powerup_star

    @property
    def health_star(self) -> pygame.Surface:
        return self.__health_heart
    
    @property
    def music_filepath(self) -> str:
        return self.__music_filepath
