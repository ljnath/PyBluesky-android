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

Version: 1.0.0 (based on desktop release 1.0.5 ; changed version number for android release)
Author: Lakhya Jyoti Nath (ljnath)
Email:  ljnath@ljnath.com
Website: https://www.ljnath.com
"""

import asyncio
import math
import random
import webbrowser

import pygame
from android import loadingscreen
from android.permissions import (Permission, check_permission,
                                 request_permissions)
from plyer import accelerometer, orientation, vibrator

from game.data.enums import Screen, StartChoice
from game.environment import GameEnvironment
from game.handlers.leaderboard import LeaderBoardHandler
from game.handlers.network import NetworkHandler
from game.sprites.cloud import Cloud
from game.sprites.jet import Jet
from game.sprites.missile import Missile
from game.sprites.samlauncher import SamLauncher
from game.sprites.star import Star
from game.sprites.text.input.name import NameInputText
from game.sprites.text import Text
from game.sprites.text.exitmenu import ExitMenuText
from game.sprites.text.gamemenu import GameMenuText
from game.sprites.text.help import HelpText
from game.sprites.text.leaderboard import LeaderBoardText
from game.sprites.text.replaymenu import ReplayMenuText
from game.sprites.text.score import ScoreText
from game.sprites.vegetation import Vegetation

API_KEY = ''


def check_update() -> None:
    """
    Method to check for game update
    """
    network_handler = NetworkHandler(API_KEY)
    asyncio.get_event_loop().run_until_complete(network_handler.check_game_update())
    asyncio.get_event_loop().run_until_complete(LeaderBoardHandler().update(API_KEY))


def submit_result() -> None:
    """
    Method to submit game score to remote server
    """
    game_env = GameEnvironment()
    if game_env.dynamic.game_score > 0:
        network_handler = NetworkHandler(API_KEY)
        asyncio.get_event_loop().run_until_complete(network_handler.submit_result())
    asyncio.get_event_loop().run_until_complete(LeaderBoardHandler().update(API_KEY))


def create_vegetation(vegetations) -> None:
    """
    Method to create vegetation
    """
    game_env = GameEnvironment()
    vegetations.empty()
    for i in range(math.ceil(game_env.static.screen_width / game_env.vegetation_size[0])):                      # drawing the 1st vegetations required to fill the 1st sceen (max is the screen width)
        vegetation = Vegetation(x_pos=i * game_env.vegetation_size[0] + game_env.vegetation_size[0] / 2)        # creating a new vegetation
        vegetations.add(vegetation)                                                                             # just adding sprite to vegetations group, to updating on screen for now


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


def request_android_permissions() -> None:
    """
    Method to request android system for permission
    """
    max_retry = 3
    while not check_permission('android.permission.WRITE_EXTERNAL_STORAGE') or max_retry > 0:
        max_retry -= 1
        request_permissions([
            Permission.WRITE_EXTERNAL_STORAGE
        ])

    print(f"VIBRATE permission = {check_permission('android.permission.VIBRATE')}")
    print(f"INTERNET permission = {check_permission('android.permission.INTERNET')}")
    print(f"WRITE_EXTERNAL_STORAGE permission = {check_permission('android.permission.WRITE_EXTERNAL_STORAGE')}")


def get_hint_sprite(hint_message: str) -> None:
    """
    Method to create hint text
    """
    game_env = GameEnvironment()
    return Text(hint_message, 30, pos_x=game_env.static.screen_width / 2, pos_y=150)        # creating game hint message


def play():
    pygame.mixer.init()                                                 # initializing same audio mixer with default settings
    pygame.init()                                                       # initializing pygame
    game_env = GameEnvironment()                                        # initializing game environment

    game_env.dynamic.collision_sound.set_volume(1.5)
    game_env.dynamic.levelup_sound.set_volume(1.5)
    game_env.dynamic.shoot_sound.set_volume(1.5)
    game_env.dynamic.hit_sound.set_volume(3)
    game_env.dynamic.powerup_sound.set_volume(10)
    game_env.dynamic.samfire_sound.set_volume(5)

    # setting main game background musicm
    # lopping the main game music and setting game volume
    pygame.mixer.music.load(game_env.static.game_sound.get('music'))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(.2)

    # settings flags to create screen in fullscreen, use HW-accleration and DoubleBuffer
    flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED | pygame.RESIZABLE

    # creating game screen with custom width and height
    screen = pygame.display.set_mode((game_env.static.screen_width, game_env.static.screen_height), flags)

    pygame.display.set_caption('{} version. {}'.format(game_env.static.name, game_env.static.version))          # setting name of game window
    pygame.display.set_icon(pygame.image.load(game_env.static.game_icon))                                       # updating game icon to the jet image
    pygame.mouse.set_visible(False)                                                     # hiding the mouse pointer from the game screen

    gameclock = pygame.time.Clock()                                                     # setting up game clock to maintain constant fps
    check_update()

    ADD_MISSILE = pygame.USEREVENT + 1                                                  # creating custom event to automatically add missiles in the screen
    pygame.time.set_timer(ADD_MISSILE, int(1000 / game_env.static.missile_per_sec))     # setting event to auto-trigger every 500ms; 2 missiles will be created every second

    ADD_CLOUD = pygame.USEREVENT + 2                                                    # creating custom event to automatically add cloud in the screen
    pygame.time.set_timer(ADD_CLOUD, int(1000 / game_env.static.cloud_per_sec))         # setting event to auto-trigger every 1s; 1 cloud will be created every second

    ADD_SAM_LAUNCHER = pygame.USEREVENT + 3
    pygame.time.set_timer(ADD_SAM_LAUNCHER, 5000)                                       # setting event to auto-trigger every 5s; 1 level can have 4 sam launcher

    RESET_SWIPE = pygame.USEREVENT + 4
    pygame.time.set_timer(RESET_SWIPE, 1000)                                            # setting event to auto-trigger sec; user can swipe once per second

    running = True                                                                      # game running variable
    gameover = False                                                                    # no gameover by default
    game_started = False                                                                # game is not started by default
    game_pause = False
    star_shown = False
    user_has_swipped = False
    screen_color = game_env.static.background_default if game_started else game_env.static.background_special

    backgrounds = pygame.sprite.Group()                                                 # creating seperate group for background sprites
    stars = pygame.sprite.GroupSingle()                                                 # group of stars with max 1 sprite
    vegetations = pygame.sprite.Group()                                                 # creating cloud group for storing all the clouds in the game
    clouds = pygame.sprite.Group()                                                      # creating cloud group for storing all the clouds in the game
    missiles = pygame.sprite.Group()                                                    # creating missile group for storing all the missiles in the game
    deactivated_missile = pygame.sprite.Group()                                         # creating missile group for storing all the deactivated missiles in the game
    samlaunchers = pygame.sprite.GroupSingle()                                          # creating missile group for storing all the samlaunchers in the game
    title_sprites = pygame.sprite.Group()

    title_banner_sprite = Text("{} {}".format(game_env.static.name, game_env.static.version), 100, pos_x=game_env.static.screen_width / 2, pos_y=100)           # creating title_banner_sprite text sprite with game name
    title_author_sprite = Text("By Lakhya Jyoti Nath (www.ljnath.com)", 26, pos_x=game_env.static.screen_width / 2, pos_y=game_env.static.screen_height - 20)   # creating game author

    active_sprite = NameInputText()
     
    swipe_navigated_menus = {
        Screen.GAME_MENU: GameMenuText(),
        Screen.HELP: HelpText(),
        Screen.LEADERBOARD: LeaderBoardText()
    }
    selected_menu_index = 0

    active_sprite = NameInputText()
    hint_sprite = get_hint_sprite("Swipe your finger to know more")      # creating game hint message
    
    if game_env.dynamic.player_name != 'player1':    
        game_env.dynamic.all_sprites.add(hint_sprite)
        active_sprite = swipe_navigated_menus[Screen.GAME_MENU]
        selected_menu_index = 0

    [title_sprites.add(sprite) for sprite in (active_sprite, title_banner_sprite, title_author_sprite)]     # adding all the necessary sprites to title_sprites
    [game_env.dynamic.all_sprites.add(sprite) for sprite in title_sprites]                                  # adding all title_sprites sprite to all_sprites

    jet = Jet()                                                                                             # creating jet sprite
    scoretext_sprite = ScoreText()                                                                          # creating scoreboard sprite
    game_env.dynamic.noammo_sprite = Text("NO AMMO !!!", 30)                                                # creating noammo-sprite

    create_vegetation(vegetations)
    menu_screens = {Screen.REPLAY_MENU, Screen.GAME_MENU, Screen.EXIT_MENU}
    last_active_sprite = (game_env.dynamic.active_screen, active_sprite)

    def hide_exit_menu():
        nonlocal game_pause, game_started, active_sprite
        pygame.mixer.music.unpause()
        game_started, game_pause = game_pause, game_started
        game_env.dynamic.all_sprites.remove(active_sprite)
        game_env.dynamic.active_screen, active_sprite = last_active_sprite
        if game_env.dynamic.active_screen != Screen.GAME_SCREEN:
            [game_env.dynamic.all_sprites.add(sprite) for sprite in (active_sprite, hint_sprite)]

    def start_gameplay():
        nonlocal gameover, jet, star_shown, screen_color, game_started
        screen_color = game_env.static.background_default                                               # restoring  screen color
        [sprite.kill() for sprite in title_sprites]                                                     # kill all the title_sprites sprite sprite
        jet = Jet()                                                                                     # re-creating the jet
        missiles.empty()                                                                                # empting the missle group
        game_env.dynamic.all_sprites = pygame.sprite.Group()                                            # re-creating group of sprites
        [game_env.dynamic.all_sprites.remove(sprite) for sprite in (active_sprite, hint_sprite)]        # removing active sprite and hint sprite
        [game_env.dynamic.all_sprites.add(sprite) for sprite in (jet, scoretext_sprite)]                # adding the jet and scoreboard to all_sprites
        game_env.reset()                                                                                # reseting game data
        pygame.time.set_timer(ADD_MISSILE, int(1000 / game_env.static.missile_per_sec))                 # resetting missile creation event timer
        create_vegetation(vegetations)                                                                  # creating vegetation
        [backgrounds.add(sprite) for sprite in vegetations.sprites()]                                   # adding vegetation to background
        game_env.dynamic.active_screen = Screen.GAME_SCREEN                                             # setting gamescreen as the active sprite
        game_started = True                                                                             # game has started
        gameover = False                                                                                # game is not over yet
        star_shown = False                                                                              # no star is displayed

    # enabling acclerometer sensor to get accleration sensor data
    accelerometer.enable()

    # Main game loop
    while running:

        # getting the accleration sensor data from accelerometer
        # acceleration_sensor_values is a tuple of (x, y, z) sensor data
        acceleration_sensor_values = accelerometer.acceleration

        # this variable is updated in case of a MOUSEMOTION; in subsequent MOUSEBUTTONUP event,
        # it is checked if the position of both these events are the same.
        # if yes, this indicates that these are part of same motion and the MOUSEBUTTONUP event can be discarded
        last_touch_position = (0, 0)

        # Look at every event in the queue
        for event in pygame.event.get():

            # checking for VIDEORESIZE event, this event is used to prevent auto-rotate in android device
            # if any change in the screensize is detected, then the orienatation is forcefully re-applied
            if event.type == game_env.VIDEORESIZE:
                orientation.set_landscape(reverse=False)

            # handling menu navigation via finger swipe
            elif event.type == game_env.MOUSEMOTION and not game_pause and not game_started and not gameover:
                # saving current interaction position; this will be later used for discarding MOUSEBUTTONUP event if the position is same
                last_touch_position = event.pos

                if user_has_swipped:
                    continue

                is_valid_swipe = False

                if event.rel[0] < -40:
                    user_has_swipped = True
                    is_valid_swipe = True
                    selected_menu_index += 1
                    if selected_menu_index == len(swipe_navigated_menus):
                        selected_menu_index = 0

                elif event.rel[0] > 40:
                    user_has_swipped = True
                    is_valid_swipe = True
                    selected_menu_index -= 1
                    if selected_menu_index < 0:
                        selected_menu_index = len(swipe_navigated_menus) - 1

                if not is_valid_swipe:
                    continue

                # settings the current swipe_navigated_menus as the active one for it to be rendered
                # and refreshing the active_sprite in game_env.dynamic.all_sprites for re-rendering
                game_env.dynamic.all_sprites.remove(active_sprite)

                game_env.dynamic.active_screen = list(swipe_navigated_menus.keys())[selected_menu_index]
                active_sprite = swipe_navigated_menus[game_env.dynamic.active_screen]

                game_env.dynamic.all_sprites.add(active_sprite)

            # showing PAUSE message when back button is pressed on android device
            elif event.type == game_env.KEYDOWN and event.key == 1073742094 and game_env.dynamic.active_screen != Screen.EXIT_MENU:
                pygame.mixer.music.pause()
                last_active_screen = game_env.dynamic.active_screen
                last_active_sprite = active_sprite
                game_started, game_pause = game_pause, game_started
                [game_env.dynamic.all_sprites.remove(sprite) for sprite in (active_sprite, hint_sprite)]
                active_sprite = ExitMenuText()
                game_env.dynamic.all_sprites.add(active_sprite)
                game_env.dynamic.active_screen = Screen.EXIT_MENU

            # mouse based interaction to simulate finger based interaction
            elif event.type == game_env.MOUSEBUTTONUP:
                # handling single finger only for now
                if event.button == 1 and event.pos != last_touch_position:

                    # resume or exit game based on user interaction with the EXIT-MENU
                    if game_env.dynamic.active_screen == Screen.EXIT_MENU:
                        if game_env.dynamic.exit:
                            running = False
                        elif not game_env.dynamic.exit:
                            pygame.mixer.music.unpause()
                            game_started, game_pause = game_pause, game_started
                            game_env.dynamic.all_sprites.remove(active_sprite)
                            game_env.dynamic.active_screen = last_active_screen
                            active_sprite = last_active_sprite

                            if game_env.dynamic.active_screen != Screen.GAME_SCREEN:
                                [game_env.dynamic.all_sprites.add(sprite) for sprite in (active_sprite, hint_sprite)]

                    # jet can shoot at use touch and when the game is running
                    if game_started and not gameover:
                        jet.shoot()

                    # start the game when user has selected 'Start Game' in GAME_MENU or 'Yes' in REPLAY_MENT
                    elif (game_env.dynamic.active_screen == Screen.GAME_MENU and game_env.dynamic.game_start_choice == StartChoice.START) or (game_env.dynamic.active_screen == Screen.REPLAY_MENU and game_env.dynamic.replay):
                        start_gameplay()

                    # exit the game when user has selected 'Exit' in GAME_MENU or 'No' in REPLAY_MENT
                    elif game_env.dynamic.active_screen == Screen.GAME_MENU and game_env.dynamic.game_start_choice == StartChoice.EXIT or (game_env.dynamic.active_screen == Screen.REPLAY_MENU and not game_env.dynamic.replay):
                        running = False

            # add missile and sam-launcher
            elif game_started and not gameover:
                if event.type == ADD_MISSILE:                                                                       # is event to add missile is triggered; missles are not added during gameover
                    new_missile = Missile()                                                                         # create a new missile
                    missiles.add(new_missile)                                                                       # adding the missile to missle group
                    game_env.dynamic.all_sprites.add(new_missile)                                                   # adding the missile to all_sprites group as well
                if event.type == ADD_SAM_LAUNCHER and not samlaunchers.sprites() and game_env.dynamic.game_level > 5:
                    samlauncher = SamLauncher()
                    samlaunchers.add(samlauncher)
                    game_env.dynamic.all_sprites.add(samlauncher)

            # resetting user_has_swipped flag, allowing user to swipe again
            if event.type == RESET_SWIPE:
                user_has_swipped = False

            # adding of clouds, backgroud, vegetation and power-up star is handled inside this
            if event.type == ADD_CLOUD:
                if game_pause:
                    continue

                last_sprite = vegetations.sprites()[-1]                                                                         # storing the last available vegetation for computation
                if last_sprite.rect.x + last_sprite.rect.width / 2 - game_env.static.screen_width < 0:                          # checking if the last vegetation has appeared in the screen, if yes a new vegetation will be created and appended
                    vegetation = Vegetation(x_pos=last_sprite.rect.x + last_sprite.rect.width + last_sprite.rect.width / 2)     # position of the new sprite is after the last sprite
                    vegetations.add(vegetation)                                                                                 # adding sprite to groups for update and display
                    backgrounds.add(vegetation)

                new_cloud = Cloud()                                                                 # is event to add cloud is triggered
                clouds.add(new_cloud)                                                               # create a new cloud
                backgrounds.add(new_cloud)                                                          # adding the cloud to all_sprites group
                if not gameover and game_started:
                    game_env.dynamic.game_playtime += 1                                             # increasing playtime by 1s as this event is triggered every second; just reusing existing event instead of recreating a new event
                    if not star_shown and random.randint(0, 30) % 3 == 0:                           # probabity of getting a star is 30%
                        star = Star()
                        stars.add(star)
                        game_env.dynamic.all_sprites.add(star)
                        star_shown = True
                    if game_env.dynamic.game_playtime % 20 == 0:                                    # changing game level very 20s
                        star_shown = False
                        game_env.dynamic.levelup_sound.play()                                       # playing level up sound
                        game_env.dynamic.game_level += 1                                            # increasing the game level
                        pygame.time.set_timer(ADD_MISSILE, int(1000 / (game_env.static.missile_per_sec + int(game_env.dynamic.game_level / 2))))    # updating timer of ADD_MISSLE for more missiles to be added
                        game_env.dynamic.ammo += 50                                                 # adding 50 ammo on each level up
                        game_env.dynamic.game_score += 10                                           # increasing game score by 10 after each level
                        game_env.dynamic.all_sprites.remove(game_env.dynamic.noammo_sprite)         # removing no ammo sprite when ammo is refilled

        screen.fill(screen_color)                                                                   # Filling screen with sky blue color
        [screen.blit(sprite.surf, sprite.rect) for sprite in backgrounds]                           # drawing all backgrounds sprites
        [screen.blit(sprite.surf, sprite.rect) for sprite in game_env.dynamic.all_sprites]          # drawing all sprites in the screen

        if not gameover:
            # missile hit
            if pygame.sprite.spritecollideany(jet, missiles) or pygame.sprite.spritecollideany(jet, game_env.dynamic.sam_missiles):    # Check if any missiles have collided with the player; if so
                vibrator.vibrate(1)                                                                         # vibrating device for 1s on game-over
                hint_sprite = get_hint_sprite("Move your device to change selection and tap to confirm")    # updating game hint message
                gameover = True                                                                             # setting gameover to true to prevent new missiles from spawning
                active_sprite = ReplayMenuText()
                game_env.dynamic.active_screen = Screen.REPLAY_MENU
                jet.kill()                                                                              # killing the jet
                [sam_missile.kill() for sam_missile in game_env.dynamic.sam_missiles]                   # killing the SAM missile
                game_env.dynamic.collision_sound.play()
                [game_env.dynamic.all_sprites.add(sprite) for sprite in (active_sprite, hint_sprite)]   # adding the gameover and the hint sprite
                game_env.dynamic.all_sprites.remove(game_env.dynamic.noammo_sprite)
                submit_result()

            # bullet hit
            collision = pygame.sprite.groupcollide(missiles, game_env.dynamic.bullets, True, True)      # checking for collision between bullets and missiles, killing each one of them on collision
            if len(collision) > 0:
                game_env.dynamic.hit_sound.play()                                                       # play missile destroyed sound
                game_env.dynamic.game_score += len(collision) * 10                                      # 1 missle destroyed = 10 pts.
                game_env.dynamic.missiles_destroyed += len(collision)                                   # to calulate player accuracy

            # powerup hit
            if pygame.sprite.spritecollideany(jet, stars):                                              # collition between jet and star (powerup)
                game_env.dynamic.powerup_sound.play()
                [game_env.dynamic.all_sprites.remove(s) for s in stars.sprites()]                       # removing the star from all_sprites to hide from screen
                game_env.dynamic.game_score += 100 * game_env.dynamic.game_level                        # increasing game score by 100
                stars.empty()                                                                           # removing star from stars group
                for missile in missiles.sprites():
                    missile.deactivate()                                                                # making missile as deactivated
                    deactivated_missile.add(missile)                                                    # adding missile to deactivated_missile group
                    missiles.remove(missile)                                                            # remove missiles from missles group to avoid collision with jet

        if not game_pause and game_started and not gameover:
            jet.update(acceleration_sensor_values)
        elif game_env.dynamic.active_screen in menu_screens:
            active_sprite.update(acceleration_sensor_values)                                            # handling menu interactions for all the possible interactive screens

        pygame.display.flip()                                                                           # updating display to the screen
        gameclock.tick(game_env.static.fps)                                                             # ticking game clock at 30 to maintain 30fps

        if not game_started:
            title_author_sprite.moveOnXaxis(2)                                                          # moving the game author sprite across the X axis

        if game_pause:
            continue

        if game_started:
            vegetations.update()                                                                        # vegetations will move only after the game starts

        game_env.dynamic.bullets.update()
        game_env.dynamic.sam_missiles.update()
        missiles.update()                                                                           # update the position of the missiles
        deactivated_missile.update()
        clouds.update()                                                                             # update the postition of the clouds
        stars.update()
        samlaunchers.update((jet.rect.x + jet.rect.width / 2, jet.rect.y + jet.rect.height))
        scoretext_sprite.update()                                                                   # update the game score

    pygame.mixer.music.stop()                                                                       # stopping game music
    pygame.mixer.quit()                                                                             # stopping game sound mixer
    notify_user_of_update()


if __name__ == '__main__':
    # handle android permission
    request_android_permissions()

    # hide loading screen as the game has been loaded
    loadingscreen.hide_loading_screen()

    # start the game
    play()
