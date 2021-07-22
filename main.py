"""
MIT License

Copyright (c) 2021 Lakhya Jyoti Nath

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

PyBluesky - A simple python game to navigate your jet and fight though a massive missiles attack based on pygame framework.

Version: 1.0.1
Author: Lakhya Jyoti Nath (ljnath)
Email:  ljnath@ljnath.com
Website: https://ljnath.com
"""

import math
import random
import webbrowser

import pygame
from android import loadingscreen
from plyer import accelerometer, orientation, vibrator

from game.data.enums import Choice, Screen
from game.environment import GameEnvironment
from game.handlers.leaderboard import LeaderBoardHandler
from game.handlers.network import NetworkHandler
from game.menu.main import MainMenu
from game.sprites.cloud import Cloud
from game.sprites.jet import Jet
from game.sprites.missile import Missile
from game.sprites.samlauncher import SamLauncher
from game.sprites.star import Star
from game.sprites.text import Text
from game.sprites.text.choice.pause import PauseChoiceText
from game.sprites.text.choice.replay import ReplayChoiceText
from game.sprites.text.input.name import NameInputText
from game.sprites.text.score import ScoreText
from game.sprites.vegetation import Vegetation

API_KEY = ''


def check_update() -> None:
    """
    Method to check for game update
    """
    NetworkHandler(API_KEY).check_game_update()


def update_leaderboard() -> None:
    """
    Method to update game leaderbaord
    """
    LeaderBoardHandler().update(API_KEY)


def submit_result() -> None:
    """
    Method to submit game score to remote server and update the local leaders file
    """
    game_env = GameEnvironment()
    if game_env.dynamic.game_score > 0:
        NetworkHandler(API_KEY).submit_result()
    LeaderBoardHandler().update(API_KEY)


def create_vegetations(vegetations: pygame.sprite.Group) -> None:
    """
    Method to create vegetation and store the vegetation sprite into the passed sprite group
    :param vegetations : pygame.sprite.Group, where the created vegetation will be stored
    """
    game_env = GameEnvironment()
    vegetations.empty()

    # creating and adding vegeration to the vegetations group.
    # only the required number of vegetation to fill the screen is created
    for i in range(math.ceil(game_env.static.screen_width / game_env.vegetation_size[0])):
        vegetation = Vegetation(x_pos=i * game_env.vegetation_size[0] + game_env.vegetation_size[0] / 2)
        vegetations.add(vegetation)


def notify_user_of_update() -> None:
    """
    Method to open the webbrowser when an new update is available
    """
    game_env = GameEnvironment()
    if game_env.dynamic.update_url:
        try:
            webbrowser.open(game_env.dynamic.update_url)
        except Exception:
            pass


def initialize() -> None:
    """
    function to initialize the game, create the game environemnt and show the game menu
    """
    pygame.mixer.init()                         # initializing same audio mixer with default settings
    pygame.init()                               # initializing pygame
    game_env = GameEnvironment()                # initializing game environment

    # configuring the sound level of sound files
    game_env.dynamic.collision_sound.set_volume(1.5)
    game_env.dynamic.levelup_sound.set_volume(1.5)
    game_env.dynamic.shoot_sound.set_volume(1.5)
    game_env.dynamic.hit_sound.set_volume(3)
    game_env.dynamic.powerup_sound.set_volume(10)
    game_env.dynamic.samfire_sound.set_volume(5)

    # setting main game background music
    # lopping the main game music and setting game volume
    pygame.mixer.music.load(game_env.static.game_sound.get('music'))
    # pygame.mixer.music.play(loops=-1) #TODO enable  music
    pygame.mixer.music.set_volume(.2)

    # settings flags to create screen in fullscreen, use HW-accleration and DoubleBuffer, also adding flag to resize the game
    flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.SCALED | pygame.RESIZABLE | pygame.HWSURFACE

    # creating game suface with custom width and height
    game_env.dynamic.game_surface = pygame.display.set_mode((game_env.static.screen_width, game_env.static.screen_height), flags)

    # creating game clock
    game_env.dynamic.game_clock = pygame.time.Clock()

    # configuring the name of the game window with game name and version
    pygame.display.set_caption(f'{game_env.static.app_name} ver. {game_env.static.app_version}')

    # all network activities goes here
    check_update()
    update_leaderboard()

    # creating an instance of the main gamemenu
    game_env.dynamic.main_menu = MainMenu().Menu

    # showing the main gamemenu
    show_menu()

    # cleanup bit, hiding or disabling features that we don't need
    pygame.mouse.set_visible(False)


def show_menu() -> None:
    """
    function to show the game menu
    """

    def add_clouds_in_menu() -> None:
        """
        inner function to add clouds in the menu
        """
        nonlocal ADD_CLOUD_TO_MENU, sprite_group, game_env, game_title_sprite

        # adding the game title sprite in the sprite group for drawing to screen
        sprite_group.add(game_title_sprite)

        # checking and looping through the ADD_CLOUD_TO_MENU events only
        # for every event a cloud is created and added to the sprite group
        for event in pygame.event.get(eventtype=ADD_CLOUD_TO_MENU):
            sprite_group.add(Cloud())

        # drawing the screen backgroud with skyblue color
        game_env.dynamic.game_surface.fill(game_env.static.background_skyblue)

        # adding all sprites in sprite_group to the screen
        [game_env.dynamic.game_surface.blit(sprite.surf, sprite.rect) for sprite in sprite_group]

        # calling update method for each sprite in the sprite group, this will update the cloud position
        sprite_group.update()

    # local variables
    game_env = GameEnvironment()
    sprite_group = pygame.sprite.Group()    # sprite group to hold sprites that needs to drawn on the screen

    # creating the game title sprite to display the game title in the menu screen
    # sprite will be in the middle of the screen and height will be 100px from top
    game_title_sprite = Text(game_env.static.app_name, size=120, pos_x=game_env.static.screen_width / 2, pos_y=100)

    # creating an user event to add menus in the mainmenu to trigger every 1s and 3 clouds should be added in every event
    ADD_CLOUD_TO_MENU = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_CLOUD_TO_MENU, int(1000 / 3))

    # dynamically updating the callback function for the play button
    play_button = game_env.dynamic.main_menu.get_widget(widget_id='play')
    if play_button:
        play_button.update_callback(play)

    game_env.dynamic.main_menu.set_onclose(play)

    while True:
        # to maintain constant FPS of the game
        game_env.dynamic.game_clock.tick(game_env.static.fps)

        # fething and looping though the game events to quit the game incase user hits the 'Exit' menu button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # showing the mainmenu if it is enabled
        if game_env.dynamic.main_menu.is_enabled():
            game_env.dynamic.main_menu.mainloop(game_env.dynamic.game_surface, add_clouds_in_menu, disable_loop=False, fps_limit=game_env.static.fps)

        # updating the game surface onto the screen
        pygame.display.flip()


def play():
    # game variables
    game_env = GameEnvironment()                                                        # initializing game environment
    running = True                                                                      # is the game running ?
    game_over = False                                                                    # has game_over occurred ?
    game_started = False                                                                # has the game started ?
    game_pause = False                                                                  # is the game paused ?
    star_shown = False                                                                  # is the power-up star shown ?
    scoretext_sprite = ScoreText()                                                      # creating scoreboard sprite
    jet = Jet()                                                                         # creating jet sprite
    game_env.dynamic.no_ammo_sprite = Text("NO AMMO !!!", 4)                            # creating NO AMMO text
    gameplay_hint_sprite = Text("Tilt your device to navigate", 40)                     # creating a gameplay hint sprite
    game_title_sprite = Text(game_env.static.app_name, size=120, pos_x=game_env.static.screen_width / 2, pos_y=100)

    # game sprite groups
    backgrounds = pygame.sprite.Group()                                                 # creating seperate group for background sprites
    stars = pygame.sprite.GroupSingle()                                                 # group of stars with max 1 sprite (= max 1 star)
    vegetations = pygame.sprite.Group()                                                 # creating cloud group for storing all the clouds in the game
    clouds = pygame.sprite.Group()                                                      # creating cloud group for storing all the clouds in the game
    missiles = pygame.sprite.Group()                                                    # creating missile group for storing all the missiles in the game
    deactivated_missiles = pygame.sprite.Group()                                        # creating missile group for storing all the deactivated missiles in the game
    samlaunchers = pygame.sprite.GroupSingle()                                          # creating missile group for storing all the samlaunchers in the game
    background_color = game_env.static.background_skyblue                               # setting the game backgroud color

    # creating user events to add sprite in the game
    ADD_CLOUD = pygame.USEREVENT + 2                                                    # creating custom event to add cloud in the screen
    pygame.time.set_timer(ADD_CLOUD, int(1000 / game_env.static.cloud_per_sec))         # setting event to auto-trigger every 1s; 1 cloud will be created every second

    ADD_MISSILE = pygame.USEREVENT + 3                                                  # creating custom event to add missiles in the screen
    pygame.time.set_timer(ADD_MISSILE, int(1000 / game_env.static.missile_per_sec))     # setting event to auto-trigger every 500ms; 2 missiles will be created every second

    ADD_SAM_LAUNCHER = pygame.USEREVENT + 4                                             # creating custom event to add SAM-LAUNCHER in the screen
    pygame.time.set_timer(ADD_SAM_LAUNCHER, 5000)                                       # setting event to auto-trigger every 5s; 1 level can have 4 sam launcher because level time is 20s, (20/5=4)

    create_vegetations(vegetations)

    game_env.dynamic.main_menu.disable()
    game_env.dynamic.main_menu.full_reset()

    # TODO - check and delete
    # blocking all the undesired events
    pygame.event.set_blocked(pygame.FINGERMOTION)
    pygame.event.set_blocked(pygame.FINGERUP)
    pygame.event.set_blocked(pygame.FINGERDOWN)
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.event.set_blocked(pygame.KEYUP)
    pygame.event.set_blocked(ADD_MISSILE)
    pygame.event.set_blocked(ADD_SAM_LAUNCHER)

    def start_gameplay() -> None:
        """
        inner method to start the gameplay
        """
        nonlocal game_over, jet, star_shown, game_started, ADD_MISSILE, ADD_SAM_LAUNCHER, background_color

        # allowing sprite creation event for automatic sprite creation
        pygame.event.set_allowed(ADD_MISSILE)
        pygame.event.set_allowed(ADD_SAM_LAUNCHER)

        game_env.reset()                                                                    # reseting gameplay data as new game has started
        missiles.empty()                                                                    # emptying the missles group
        game_env.dynamic.all_sprites = pygame.sprite.Group()                                # re-creating the group of holding all game sprites

        jet = Jet()                                                                         # re-creating the jet
        game_pause = False
        game_started = True                                                                 # game has started
        game_over = False                                                                    # game is not over yet !
        star_shown = False
        game_env.dynamic.active_screen = Screen.GAMEPLAY                                    # setting GAMEPLAY as the active screen becuase player has started the game
        background_color = game_env.static.background_greenish_blue                         # setting the game backgroud color

        pygame.time.set_timer(ADD_MISSILE, int(1000 / game_env.static.missile_per_sec))     # resetting missile creation event timer
        [backgrounds.add(sprite) for sprite in vegetations.sprites()]                       # adding all the newly cerated vegetation to backgrounds group
        [game_env.dynamic.all_sprites.add(sprite) for sprite in (jet, scoretext_sprite, gameplay_hint_sprite)]    # adding sprites that needs to be displayed when the game starts

    # if player name is not present, then showing screen to enter player name
    # else the game is started
    if game_env.dynamic.player_name:
        start_gameplay()
    else:
        dynamic_sprite = NameInputText()
        [game_env.dynamic.all_sprites.add(_sprite) for _sprite in (dynamic_sprite, game_title_sprite)]
        game_env.dynamic.active_screen = Screen.NAME_INPUT

    # enabling acclerometer sensor to get acclerometer sensor data for jet navigation
    accelerometer.enable()

    # Main game loop
    while running:

        # Look at every events in the pygame.event queue
        for event in pygame.event.get():

            # mouse based interaction to simulate finger based interaction
            if event.type == game_env.MOUSEBUTTONDOWN:
                # handling single finger only for now
                if event.button == 1:
                    # handling interaction oin the NAME-INPUT menu like button click and show/hide of keyboard
                    if not game_started and game_env.dynamic.active_screen == Screen.NAME_INPUT:

                        # if playername is not defined; this screen is shown to the user for getting the username
                        # once the username is entered, user can touch either of CLEAR or OK surface.
                        # we are check this touch activity here
                        # if game_env.dynamic.player_name.strip() == '':
                        dynamic_sprite.check_input(event.pos)

                    elif (game_pause or game_over) and game_env.dynamic.active_screen in (Screen.PAUSE_MENU, Screen.REPLAY_MENU):
                        dynamic_sprite.check_input(event.pos)

                    # jet can shoot at use touch and when the game is running
                    elif game_started and not game_over:
                        jet.shoot()

            # checking for VIDEORESIZE event, this event is used to prevent auto-rotate in android device
            # if any change in the screensize is detected, then the orienatation is forcefully re-applied
            elif event.type == game_env.VIDEORESIZE:
                orientation.set_landscape(reverse=False)

            # handling keydown event to show the pause menu
            elif event.type == game_env.KEYDOWN:
                if game_env.dynamic.active_screen == Screen.GAMEPLAY and pygame.key.name(event.key) == 'AC Back':
                    pygame.mixer.music.pause()
                    game_started, game_pause = game_pause, game_started
                    dynamic_sprite = PauseChoiceText()
                    game_env.dynamic.all_sprites.add(dynamic_sprite)
                    game_env.dynamic.active_screen = Screen.PAUSE_MENU
                    game_env.dynamic.user_choice = Choice.UNSELECTED

            # handling the textinput event to allow user to type
            elif event.type == game_env.TEXTINPUT and game_env.dynamic.active_screen == Screen.NAME_INPUT:
                dynamic_sprite.update(event.text)

            # adding of clouds, backgroud, vegetation and power-up star is handled inside this
            # the reset of user swip is also handled in this; this a user is allowed to make 1 swipe every second
            elif event.type == ADD_CLOUD:
                if game_pause:
                    continue

                # removing the hint spite after 3s of gameplay
                if game_env.dynamic.game_playtime == 2:
                    game_env.dynamic.all_sprites.remove(gameplay_hint_sprite)

                last_sprite = vegetations.sprites()[-1]                                                                         # storing the last available vegetation for computation
                if last_sprite.rect.x + last_sprite.rect.width / 2 - game_env.static.screen_width < 0:                          # checking if the last vegetation has appeared in the screen, if yes a new vegetation will be created and appended
                    vegetation = Vegetation(x_pos=last_sprite.rect.x + last_sprite.rect.width + last_sprite.rect.width / 2)     # position of the new sprite is after the last sprite
                    vegetations.add(vegetation)                                                                                 # adding sprite to groups for update and display
                    backgrounds.add(vegetation)

                new_cloud = Cloud()                                                                                             # creating a new cloud
                clouds.add(new_cloud)                                                                                           # adding cloud to clouds group
                backgrounds.add(new_cloud)                                                                                      # adding the cloud to backgrouds group

                if not game_over and game_started:
                    game_env.dynamic.game_playtime += 1                                                                         # increasing playtime by 1s as this event is triggered every second; just reusing existing event instead of recreating a new event
                    if not star_shown and random.randint(0, 30) % 3 == 0:                                                       # probabity of getting a star is 30%
                        star = Star()
                        stars.add(star)
                        game_env.dynamic.all_sprites.add(star)
                        star_shown = True
                    if game_env.dynamic.game_playtime % 20 == 0:                                                                # changing game level very 20s
                        star_shown = False
                        game_env.dynamic.levelup_sound.play()                                                                   # playing level up sound
                        game_env.dynamic.game_level += 1                                                                        # increasing the game level
                        pygame.time.set_timer(ADD_MISSILE, int(1000 / (game_env.static.missile_per_sec + int(game_env.dynamic.game_level / 2))))    # updating timer of ADD_MISSLE for more missiles to be added
                        game_env.dynamic.ammo += 50                                                                             # adding 50 ammo on each level up
                        game_env.dynamic.game_score += 10                                                                       # increasing game score by 10 after each level
                        game_env.dynamic.all_sprites.remove(game_env.dynamic.no_ammo_sprite)                                    # removing the no ammo hint sprite when ammo is refilled

            # adding enemy missiles to the screen
            elif event.type == ADD_MISSILE:                                                                                     # is event to add missile is triggered; missles are not added during game_over
                if game_pause:
                    continue
                new_missile = Missile()                                                                                         # create a new missile
                missiles.add(new_missile)                                                                                       # adding the missile to missle group
                game_env.dynamic.all_sprites.add(new_missile)                                                                   # adding the missile to all_sprites group as well

            # adding sam-launchers to the screen when user has crossed level 5
            elif event.type == ADD_SAM_LAUNCHER and not samlaunchers.sprites() and game_env.dynamic.game_level > 5:
                if game_pause:
                    continue
                samlauncher = SamLauncher()
                samlaunchers.add(samlauncher)
                game_env.dynamic.all_sprites.add(samlauncher)

        # if the active screen is NAME-INPUT and if the playername is available
        # this means that user has entered the playername in the NAME-INPNUT screen; removing the screen now
        if game_env.dynamic.active_screen == Screen.NAME_INPUT:
            if game_env.dynamic.user_choice == Choice.OK and game_env.dynamic.player_name.strip() != '':
                pygame.key.stop_text_input()
                [game_env.dynamic.all_sprites.remove(_sprite) for _sprite in (dynamic_sprite, game_title_sprite)]
                start_gameplay()

        # handling choices in pause menu
        elif game_env.dynamic.active_screen == Screen.PAUSE_MENU:
            if game_env.dynamic.user_choice == Choice.YES:
                pygame.mixer.music.unpause()
                game_started, game_pause = game_pause, game_started
                game_env.dynamic.all_sprites.remove(dynamic_sprite)
                game_env.dynamic.active_screen = Screen.GAMEPLAY
            elif game_env.dynamic.user_choice == Choice.NO:
                running = False

        # handling choices in replay menu
        elif game_env.dynamic.active_screen == Screen.REPLAY_MENU:
            if game_env.dynamic.user_choice == Choice.NO:
                running = False
            elif game_env.dynamic.user_choice == Choice.YES:
                game_env.dynamic.all_sprites.remove(dynamic_sprite)
                start_gameplay()

        game_env.dynamic.game_surface.fill(background_color)                                                                    # Filling screen with current background color
        [game_env.dynamic.game_surface.blit(sprite.surf, sprite.rect) for sprite in backgrounds]                                # adding all sprites in the backgrounds group to the screen
        [game_env.dynamic.game_surface.blit(sprite.surf, sprite.rect) for sprite in game_env.dynamic.all_sprites]               # adding all sprites in tthe game_env.dynamic.all_sprites to the screen

        if game_started and not game_over:
            # enemy missile or sam-missile hit
            if pygame.sprite.spritecollideany(jet, missiles) or pygame.sprite.spritecollideany(jet, game_env.dynamic.sam_missiles):
                game_over = True                                                                                 # setting game_over to true to prevent new missiles from spawning
                jet.kill()                                                                                      # killing the jet
                [sam_missile.kill() for sam_missile in game_env.dynamic.sam_missiles]                           # killing the SAM missile
                game_env.dynamic.all_sprites.remove(game_env.dynamic.no_ammo_sprite)
                pygame.event.set_blocked(ADD_MISSILE)                                                           # blocking event to add any more missile in the screen due to game_over
                pygame.event.set_blocked(ADD_SAM_LAUNCHER)                                                      # blocking event to add any more sam launcher in the screen due to game_over
                game_env.dynamic.collision_sound.play()
                vibrator.vibrate(1)                                                                             # vibrating device for 1s on game-over
                dynamic_sprite = ReplayChoiceText()
                game_env.dynamic.all_sprites.add(dynamic_sprite)
                game_env.dynamic.active_screen = Screen.REPLAY_MENU
                game_env.dynamic.user_choice = Choice.UNSELECTED
                submit_result()                                                                                 # submit game score

            # shoot down an enemy missile
            collision = pygame.sprite.groupcollide(missiles, game_env.dynamic.bullets, True, True)      # checking for collision between bullets and missiles, killing each one of them on collision
            if len(collision) > 0:
                game_env.dynamic.hit_sound.play()                                                       # play missile destroyed sound
                game_env.dynamic.game_score += len(collision) * 10                                      # 1 missle destroyed = 10 pts.
                game_env.dynamic.missiles_destroyed += len(collision)                                   # to calulate player accuracy

            # jet took a power-up star
            if pygame.sprite.spritecollideany(jet, stars):                                              # collition between jet and star (powerup)
                game_env.dynamic.powerup_sound.play()
                [game_env.dynamic.all_sprites.remove(_star) for _star in stars.sprites()]               # removing the star from all_sprites to hide from screen
                game_env.dynamic.game_score += 100 * game_env.dynamic.game_level                        # increasing game score by 100
                stars.empty()                                                                           # removing star from stars group
                for missile in missiles.sprites():
                    missile.deactivate()                                                                # making missile as deactivated
                    deactivated_missiles.add(missile)                                                   # adding missile to deactivated_missiles group
                    missiles.remove(missile)                                                            # remove missiles from missles group to avoid collision with jet

            # if game is running navigate the jet as per device movement
            if game_started and not game_pause or not game_over:
                # getting the accleration sensor data from accelerometer
                # acceleration_sensor_values is a tuple of (x, y, z) sensor data
                jet.update(accelerometer.acceleration)

        pygame.display.flip()                                                                           # updating display to the screen
        game_env.dynamic.game_clock.tick(game_env.static.fps)                                           # to maintain constant FPS of the game

        if game_pause:
            continue

        if game_started:
            vegetations.update()                                                                        # vegetations will move only after the game starts

        game_env.dynamic.bullets.update()                                                               # updating the position of bullets
        game_env.dynamic.sam_missiles.update()                                                          # updating the position of missiles launched by sam-launcher
        missiles.update()                                                                               # updating the position of the enemy missiles
        deactivated_missiles.update()                                                                   # updating the position of the deactivated enemy missiles
        clouds.update()                                                                                 # updating the position of the clouds
        stars.update()                                                                                  # updating the position of the stars
        samlaunchers.update((jet.rect.x + jet.rect.width / 2, jet.rect.y + jet.rect.height))            # updating the position of the sam-launcher
        scoretext_sprite.update()                                                                       # updating the game scoretext sprite which includes gameplay time, score, etc.

    pygame.mixer.music.stop()                                                                           # stopping game music
    pygame.mixer.quit()                                                                                 # stopping game sound mixer
    notify_user_of_update()
    exit()


if __name__ == '__main__':
    # hide loading screen as the game has been loaded
    loadingscreen.hide_loading_screen()

    # initialize the game
    initialize()
