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

Version: 1.1.0
Author: Lakhya Jyoti Nath (ljnath)
Email:  ljnath@ljnath.com
Website: https://ljnath.com
"""

import random

import pygame

# importing android specific modules when executed in an android environembt
from game import IS_ANDROID

if IS_ANDROID:
    from android import loadingscreen
    from plyer import accelerometer, orientation, vibrator

from game.data.enums import (BackgroundType, Choice, CloudType, GameState, PowerUpState, Screen,
                             SoundType)
from game.environment import GameEnvironment
from game.handlers.leaderboard import LeaderBoardHandler
from game.handlers.network import NetworkHandler
from game.menu.main import MainMenu
from game.sprites.incoming_missile import IncomingMissile
from game.sprites.jet import Jet
from game.sprites.parallax import Parallax
from game.sprites.parallax.cloud import CloudParallax
from game.sprites.parallax.group import ParallaxGroup
from game.sprites.star import Star
from game.sprites.tank import Tank
from game.sprites.text import Text
from game.sprites.text.choice.pause import PauseChoiceText
from game.sprites.text.choice.replay import ReplayChoiceText
from game.sprites.text.input.name import NameInputText
from game.sprites.text.score import ScoreText

# from game.sprites.vegetation import Vegetation

API_KEY = ''


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


def initialize() -> None:
    """
    function to initialize the game, create the game environemnt and show the game menu
    """
    pygame.mixer.pre_init(44100, 16, 2, 4096)   # initializing same audio mixer with default settings
    pygame.mixer.init()                         # initializing same audio mixer with default settings
    pygame.init()                               # initializing pygame
    game_env = GameEnvironment()                # initializing game environment

    # settings flags to create screen in fullscreen, use HW-accleration and DoubleBuffer, also adding flag to resize the game
    flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE

    # creating game suface with custom width and height
    game_env.dynamic.game_surface = pygame.display.set_mode((game_env.static.screen_width, game_env.static.screen_height), flags)

    # initializing all game assets
    game_env.game_assets.initialize()

    # creating game clock
    game_env.dynamic.game_clock = pygame.time.Clock()

    # configuring the name of the game window with game name and version
    pygame.display.set_caption(f'{game_env.static.app_name} ver. {game_env.static.app_version}')

    # configuring the sound level of sound files
    game_env.game_assets.get_sound(SoundType.MISSILE_COLLISION).set_volume(1.5)
    game_env.game_assets.get_sound(SoundType.LEVEL_UP).set_volume(1.5)
    game_env.game_assets.get_sound(SoundType.SHOOT).set_volume(1.5)
    game_env.game_assets.get_sound(SoundType.MISSILE_HIT).set_volume(3)
    game_env.game_assets.get_sound(SoundType.POWER_UP).set_volume(10)
    game_env.game_assets.get_sound(SoundType.TANK_FIRE).set_volume(5)

    # setting main game background music
    # lopping the main game music and setting game volume
    pygame.mixer.music.load(game_env.game_assets.music_filepath)
    if game_env.dynamic.play_music:
        pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(.2)

    # updating game leaders
    update_leaderboard()

    # hiding the mouse pointer in case of ANDROID
    pygame.mouse.set_visible(IS_ANDROID)

    # creating an instance of the main gamemenu
    game_env.dynamic.main_menu = MainMenu().Menu

    # showing the main gamemenu
    # show_menu()
    play()


def show_menu() -> None:
    """
    Function to show the game menu
    """
    def add_clouds_in_menu() -> None:
        """
        inner function to add clouds in the menu
        """
        nonlocal ADD_MEDIUM_CLOUD, sprite_group, game_env, game_title_sprite, current_play_music_choice

        # adding the game title sprite in the sprite group for drawing to screen
        sprite_group.add(game_title_sprite)

        # checking and looping through the ADD_MEDIUM_CLOUD events only
        # for every event a cloud is created and added to the sprite group
        if pygame.event.get(eventtype=ADD_MEDIUM_CLOUD):
            sprite_group.add(CloudParallax(CloudType.MEDIUM))
            sprite_group.add(CloudParallax(CloudType.MEDIUM))

        # drawing the screen backgroud with skyblue color
        game_env.dynamic.game_surface.fill(game_env.static.background_skyblue)

        # adding all sprites in sprite_group to the screen
        [game_env.dynamic.game_surface.blit(sprite.surf, sprite.rect) for sprite in sprite_group]

        # calling update method for each sprite in the sprite group, this will update the cloud position
        sprite_group.update()

        # if music toggle has not changed, no point of start/stop music
        if current_play_music_choice == game_env.dynamic.play_music:
            return

        # storing the new music toggle value in current_play_music_choice
        current_play_music_choice = game_env.dynamic.play_music

        # playing/stopping game music based on user selection
        if game_env.dynamic.play_music:
            pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.stop()

    # local variables
    game_env = GameEnvironment()
    sprite_group = pygame.sprite.Group()    # sprite group to hold sprites that needs to drawn on the screen
    current_play_music_choice = game_env.dynamic.play_music

    # creating the game title sprite to display the game title in the menu screen
    # sprite will be in the middle of the screen and height will be 100px from top
    game_title_sprite = Text(game_env.static.app_name, size=120, pos_x=game_env.static.screen_width / 2, pos_y=100)

    # creating an user event to add menus in the mainmenu to trigger every 1s and 2 clouds should be added in every event
    ADD_MEDIUM_CLOUD = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_MEDIUM_CLOUD, 1000)

    # dynamically updating the callback function for the play button
    play_button = game_env.dynamic.main_menu.get_widget(widget_id='play')
    if play_button:
        play_button.update_callback(play)

    while True:
        # fetching for QUIT event, exiting game when detected
        if pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            exit()

        # showing the mainmenu if it is enabled
        if game_env.dynamic.main_menu.is_enabled():
            game_env.dynamic.main_menu.mainloop(game_env.dynamic.game_surface, add_clouds_in_menu, disable_loop=False, fps_limit=game_env.static.fps)

        # updating the game surface onto the screen
        pygame.display.flip()

        # to maintain constant FPS of the game
        game_env.dynamic.game_clock.tick(game_env.static.fps)


def play():
    """
    Play function of the game where the main gameloop is present and the game is drawn
    """
    # game variables
    game_env = GameEnvironment()                                                        # initializing game environment
    running = True                                                                      # is the game running ?
    game_state = GameState.READY_TO_RUN                                                 # game state; default is READY_TO_RUN
    powerup_state = PowerUpState.ACTIVE                                                  # state of the power-up star
    scoretext_sprite = ScoreText()                                                      # creating scoreboard sprite
    jet = Jet()                                                                         # creating jet sprite
    game_env.dynamic.no_ammo_sprite = Text("NO AMMO !!!", 40)                           # creating NO AMMO text
    gameplay_hint_sprite = Text("Tilt your device to navigate", 40)                     # creating a gameplay hint sprite
    game_title_sprite = Text(game_env.static.app_name, size=120, pos_x=game_env.static.screen_width / 2, pos_y=100)

    # game sprite groups
    stars = pygame.sprite.GroupSingle()                                                 # SingleGroup for storing the power-up star
    tanks = pygame.sprite.GroupSingle()                                                 # SingleGroup for storing the tank
    incoming_missiles = pygame.sprite.Group()                                           # Sprite Group for storing all activated incoming missiles
    deactivated_incoming_missiles = pygame.sprite.Group()                               # Sprite Group for storing all deactivated incoming missiles

    backgrounds = ParallaxGroup()                                                       # ParallaxGroup for storing game backgrounds
    mountains = ParallaxGroup()                                                         # ParallaxGroup for storing game mountains
    deserts = ParallaxGroup()                                                           # ParallaxGroup for storing game desert
    clouds = ParallaxGroup()                                                            # ParallaxGroup for storing clouds in gamescreen

    # creating user events to add sprite in the game
    PER_SEC = pygame.USEREVENT + 2                                                      # PER_SEC event to perform various task on every tick
    pygame.time.set_timer(PER_SEC, 1000)                                                # this event is used to update game_playtime value, add clouds, etc.

    ADD_INCOMING_MISSILE = pygame.USEREVENT + 3                                         # creating custom event to add incoming missiles in the screen
    pygame.time.set_timer(ADD_INCOMING_MISSILE, 2000)                                   # setting event to auto-trigger every 2s

    ADD_TANK = pygame.USEREVENT + 4                                                     # creating custom event to add TANK in the screen
    pygame.time.set_timer(ADD_TANK, 5000)                                               # setting event to auto-trigger every 5s; each level can have 4 tanks because level time is 20s, (20/5=4)

    ADD_BIG_CLOUD = pygame.USEREVENT + 5                                                # creating custom event to add TANK in the screen
    pygame.time.set_timer(ADD_BIG_CLOUD, game_env.static.big_cloud_interval * 1000)     # setting event to auto-trigger every 5s; each level can have 4 tanks because level time is 20s, (20/5=4)

    ADD_SMALL_CLOUD = pygame.USEREVENT + 6                                              # creating custom event to add TANK in the screen
    pygame.time.set_timer(ADD_SMALL_CLOUD, game_env.static.small_cloud_interval * 1000)     # setting event to auto-trigger every 5s; each level can have 4 tanks because level time is 20s, (20/5=4)

    game_env.dynamic.main_menu.disable()
    game_env.dynamic.main_menu.full_reset()

    # blocking all the undesired events including few custom events, which will be enabled before starting the gameplay
    pygame.event.set_blocked([pygame.FINGERMOTION,
                              pygame.FINGERUP,
                              pygame.FINGERDOWN,
                              pygame.MOUSEMOTION,
                              pygame.KEYUP,
                              ADD_INCOMING_MISSILE,
                              ADD_TANK,
                              ADD_BIG_CLOUD,
                              ADD_SMALL_CLOUD])

    # creating moon sprite; moon position is center of screen, 50px from top
    moon = Parallax(BackgroundType.MOON, (game_env.static.screen_width / 2, 50))

    def start_gameplay() -> None:
        """
        inner method to start the gameplay
        """
        nonlocal jet, powerup_state, game_state, ADD_INCOMING_MISSILE, ADD_TANK

        # allowing sprite creation event for automatic sprite creation
        pygame.event.set_allowed([ADD_INCOMING_MISSILE,
                                  ADD_TANK,
                                  ADD_BIG_CLOUD,
                                  ADD_SMALL_CLOUD])

        game_env.dynamic.sprites_to_draw = pygame.sprite.Group()
        game_env.reset_game_stats()                                                                                 # reseting all gameplay stats
        incoming_missiles.empty()                                                                                   # emptying group of incoming missiles
        
        jet = Jet()                                                                                                 # re-creating the jet
        game_env.dynamic.jet_health = 100                                                                           # restting the jet health
        powerup_state = PowerUpState.ACTIVE
        game_state = GameState.RUNNING
        game_env.dynamic.active_screen = Screen.GAMEPLAY                                                            # setting GAMEPLAY as the active screen becuase player has started the game
        [game_env.dynamic.sprites_to_draw.add(_sprite) for _sprite in (jet, scoretext_sprite, gameplay_hint_sprite)]  # adding sprites that needs to be displayed when the game starts

    # starting the game if palyer-name is present, else the input screen is displayed
    if game_env.dynamic.player_name:
        start_gameplay()
    else:
        dynamic_sprite = NameInputText()
        [game_env.dynamic.sprites_to_draw.add(_sprite) for _sprite in (dynamic_sprite, game_title_sprite)]
        game_env.dynamic.active_screen = Screen.NAME_INPUT

    # enabling acclerometer sensor in case of ANDOIRD to get acclerometer sensor data for jet navigation
    if IS_ANDROID:
        accelerometer.enable()
        
    print(pygame.display.Info())
    print(game_env.dynamic.game_surface)
    print(pygame.display.get_driver() )
    # --------------------
    # MAIN GAME LOOP
    # --------------------
    while running:

        # --------------------------------------------------------
        # PARALLAX BACKGROUND
        # --------------------------------------------------------

        # adding game background, atleast 3 background images needs to be present in the group
        # one to be killed on left - one activily shown - one as buffer
        # background is automatically switched between Day and Night based on system time
        # x-position is at the end of the last sprite - 15px (this is done to present screen tearing), y-position is fixed at 0
        while len(backgrounds) < 2:
            backgrounds.add(Parallax(BackgroundType.NIGHT if game_env.dynamic.is_night else BackgroundType.DAY, (len(backgrounds) * game_env.static.screen_width - 15, 0)))

        while len(mountains) < 2:
            mountains.add(Parallax(BackgroundType.MOUNTAIN, (len(mountains) * game_env.static.screen_width - 15, 650)))

        while len(deserts) < 2:
            deserts.add(Parallax(BackgroundType.DESERT, (len(deserts) * game_env.static.screen_width - 15, 980)))

        # --------------------------------------------------------
        # ALL GAME EVENT HANDLING
        # --------------------------------------------------------

        # Look at every events in the pygame.event queue
        for event in pygame.event.get():
            print(f'fresh event: {event}')
            # checking for VIDEORESIZE event only incase of ANDROID, this event is used to prevent auto-rotate in android device
            # if any change in the screensize is detected, then the orienatation is forcefully re-applied
            if IS_ANDROID and event.type == game_env.VIDEORESIZE:
                orientation.set_landscape(reverse=False)

            # mouse based interaction to simulate finger based interaction
            elif event.type == game_env.MOUSEBUTTONDOWN:
                print(f'event.type = {event}')
                # handling single finger only for now
                if event.button == 1:
                    # jet can shoot at use touch and when the game is running
                    if game_state == GameState.RUNNING:
                        jet.shoot()
                    # handling interaction oin the NAME-INPUT menu like button click and show/hide of keyboard
                    elif game_state == GameState.READY_TO_RUN and game_env.dynamic.active_screen == Screen.NAME_INPUT:

                        # if playername is not defined; this screen is shown to the user for getting the username
                        # once the username is entered, user can touch either of CLEAR or OK surface.
                        # we are check this touch activity here
                        if game_env.dynamic.player_name.strip() == '':
                            dynamic_sprite.check_input(event.pos)

                    elif game_state in (GameState.PAUSED, GameState.GAMEOVER) and game_env.dynamic.active_screen in (Screen.PAUSE_MENU, Screen.REPLAY_MENU):
                        dynamic_sprite.check_input(event.pos)


            # handling keydown event to show the pause menu
            elif event.type == game_env.KEYDOWN:
                if game_env.dynamic.active_screen == Screen.GAMEPLAY and pygame.key.name(event.key) == 'AC Back':
                    pygame.mixer.music.pause()
                    game_state = GameState.PAUSED
                    dynamic_sprite = PauseChoiceText()
                    game_env.dynamic.sprites_to_draw.add(dynamic_sprite)
                    game_env.dynamic.active_screen = Screen.PAUSE_MENU
                    game_env.dynamic.user_choice = Choice.UNSELECTED

            # handling the textinput event to allow user to type
            elif event.type == game_env.TEXTINPUT and game_env.dynamic.active_screen == Screen.NAME_INPUT:
                dynamic_sprite.update(event.text)

            # adding of clouds, backgroud, vegetation and power-up star is handled inside this
            # the reset of user swip is also handled in this; this a user is allowed to make 1 swipe every second
            elif event.type == PER_SEC:

                # if game is paused, don't do anything
                if game_state == GameState.PAUSED:
                    continue

                # removing the hint spite after 2s of gameplay
                if game_env.dynamic.game_playtime == 2:
                    game_env.dynamic.sprites_to_draw.remove(gameplay_hint_sprite)

                if game_state == GameState.RUNNING:
                    game_env.dynamic.game_playtime += 1                                                                         # increasing playtime by 1s as this event is triggered every second; just reusing existing event instead of recreating a new event
                    if powerup_state == PowerUpState.ACTIVE and not stars and random.choice([0, 1, 2]) == 0:                    # probabity of getting a star is 33.3%, star is shown only when the no star is visible on the screen
                        powerup_state = PowerUpState.INACTIVE
                        star = Star()
                        stars.add(star)
                        game_env.dynamic.sprites_to_draw.add(star)

                    if game_env.dynamic.game_playtime % 20 == 0:                                                                # changing game level very 20s
                        powerup_state = PowerUpState.ACTIVE
                        game_env.dynamic.game_level += 1                                                                        # increasing the game level
                        game_env.game_assets.get_sound(SoundType.LEVEL_UP).play()                                               # playing level up sound
                        game_env.dynamic.ammo += 50                                                                             # adding 50 ammo on each level up
                        game_env.dynamic.game_score += 10                                                                       # increasing game score by 10 after each level
                        game_env.dynamic.sprites_to_draw.remove(game_env.dynamic.no_ammo_sprite)                                # removing the no ammo hint sprite when ammo is refilled

                        # increasing the incoming missile rate after every 3 level
                        # every 3 level, the per second rate is increased
                        game_env.dynamic.incoming_missiles_rate = game_env.static.missile_per_sec + (game_env.dynamic.game_level // 3)

            # adding enemy missiles to the screen; skipped when game is paused
            elif event.type == ADD_INCOMING_MISSILE and game_state == GameState.RUNNING:                                       # is event to add missile is triggered; missles are not added during game_over
                for _ in range(game_env.dynamic.incoming_missiles_rate):
                    _incoming_missile = IncomingMissile()
                    incoming_missiles.add(_incoming_missile)
                    game_env.dynamic.sprites_to_draw.add(_incoming_missile)

            # adding tank when user has crossed level 5 and if there are no tanks in the game screen
            # skipped when game is paused
            elif event.type == ADD_TANK and not tanks and game_env.dynamic.game_level >= game_env.static.tank_activates_at and game_state == GameState.RUNNING:
                _tank = Tank()
                tanks.add(_tank)
                game_env.dynamic.sprites_to_draw.add(_tank)

            # adding big clouds to the screen after the game has started
            elif event.type == ADD_BIG_CLOUD:                                          # is event to add missile is triggered; missles are not added during game_over
                clouds.add(CloudParallax(CloudType.BIG))

            # adding small clouds to the screen after the game has started
            elif event.type == ADD_SMALL_CLOUD:                                         # is event to add missile is triggered; missles are not added during game_over
                clouds.add(CloudParallax(CloudType.SMALL))

        # --------------------------------------------------------
        # ALL TEXT-BASED MENU BUTTON INTERACTIONS
        # --------------------------------------------------------

        # if the active screen is NAME-INPUT and if the playername is available
        # this means that user has entered the playername in the NAME-INPNUT screen; removing the screen now
        if game_env.dynamic.active_screen == Screen.NAME_INPUT:
            if game_env.dynamic.user_choice == Choice.OK and game_env.dynamic.player_name.strip() != '':
                pygame.key.stop_text_input()
                [game_env.dynamic.sprites_to_draw.remove(_sprite) for _sprite in (dynamic_sprite, game_title_sprite)]
                start_gameplay()

        # handling choices in pause menu
        elif game_env.dynamic.active_screen == Screen.PAUSE_MENU:
            if game_env.dynamic.user_choice == Choice.YES:
                pygame.mixer.music.unpause()
                game_started, game_pause = game_pause, game_started
                game_env.dynamic.sprites_to_draw.remove(dynamic_sprite)
                game_env.dynamic.active_screen = Screen.GAMEPLAY
            elif game_env.dynamic.user_choice == Choice.NO:
                running = False

        # handling choices in replay menu
        elif game_env.dynamic.active_screen == Screen.REPLAY_MENU:
            if game_env.dynamic.user_choice == Choice.YES:
                game_env.dynamic.sprites_to_draw.remove(dynamic_sprite)
                start_gameplay()
            elif game_env.dynamic.user_choice == Choice.NO:
                running = False

        # --------------------------------------------------------
        #  ALL COLLISION DETECTIONS
        # --------------------------------------------------------
        if game_state == GameState.RUNNING:
            # incoming missile or tank-rocket hit
            # when hit the jet health is reduced by 20%; all the incoming missiles and tank rocket is cleared from screen and jet is respawned on left
            if pygame.sprite.spritecollideany(jet, incoming_missiles) or pygame.sprite.spritecollideany(jet, game_env.dynamic.tank_rockets):
                [_sprite.kill() for _sprite in incoming_missiles.sprites()]
                [_sprite.kill() for _sprite in game_env.dynamic.tank_rockets.sprites()]
                incoming_missiles.empty()
                game_env.dynamic.tank_rockets.empty()

                # respawning jet on the left side of the screen
                jet.rect.x = 10
                jet.rect.y = game_env.static.screen_height / 2
                game_env.dynamic.jet_health -= 20
                game_env.game_assets.get_sound(SoundType.MISSILE_COLLISION).play()

                if game_env.dynamic.jet_health > 0:
                    if IS_ANDROID:
                        # if health is present, small vibration is made
                        vibrator.vibrate(0.1)
                else:
                    # if no health then game over
                    game_state = GameState.GAMEOVER                                                                 # setting game_over to true to prevent new missiles from spawning
                    jet.kill()                                                                                      # killing the jet

                    if IS_ANDROID:
                        vibrator.vibrate(1)                                                                         # vibrating ANDROID device for 1s on game-over
                    game_env.dynamic.sprites_to_draw.remove(game_env.dynamic.no_ammo_sprite)                        # remving the no ammo sprite, if it is present on the screen
                    pygame.event.set_blocked(ADD_INCOMING_MISSILE)                                                  # blocking event to add any more incoming missile in the screen due to game_over
                    pygame.event.set_blocked(ADD_TANK)                                                              # blocking event to add any more tank in the screen due to game_over
                    dynamic_sprite = ReplayChoiceText()                                                             # game over sprite is created and shown on screen
                    game_env.dynamic.sprites_to_draw.add(dynamic_sprite)
                    game_env.dynamic.active_screen = Screen.REPLAY_MENU
                    game_env.dynamic.user_choice = Choice.UNSELECTED
                    submit_result()                                                                                 # submit game score

            # shoot down an incoming missile
            collision = pygame.sprite.groupcollide(incoming_missiles, game_env.dynamic.jet_missiles, True, True)    # checking for collision between jet_missiles and incoming missiles, killing each one of them on collision
            if len(collision) > 0:
                game_env.game_assets.get_sound(SoundType.MISSILE_HIT).play()                                        # play missile destroyed sound
                game_env.dynamic.game_score += len(collision) * 10                                                  # 1 missle destroyed = 10 pts.
                game_env.dynamic.missiles_destroyed += len(collision)                                               # to calulate player accuracy

            # jet took a power-up star
            if pygame.sprite.spritecollideany(jet, stars):                                                  # collition between jet and star (powerup)
                game_env.game_assets.get_sound(SoundType.POWER_UP).play()
                [game_env.dynamic.sprites_to_draw.remove(_sprite) for _sprite in stars.sprites()]           # removing the star from sprites_to_draw to hide from screen
                game_env.dynamic.game_score += 100 * game_env.dynamic.game_level                            # increasing game score by 100
                stars.empty()                                                                               # removing star from stars group

                for incoming_missile in incoming_missiles.sprites():
                    incoming_missile.deactivate()                                                           # marking all existing missiles as deactivated
                    deactivated_incoming_missiles.add(incoming_missile)                                     # adding missile to deactivated_incoming_missiles group to show freefall
                    incoming_missiles.remove(incoming_missile)                                              # remove missiles from missles incoming_missiles to avoid any further collision with jet

        # --------------------------------------------------------
        # SURFACE UPDATES
        # --------------------------------------------------------
        if game_state != GameState.PAUSED:
            # updating jet surface when game is running and not when game is paused
            if game_state == GameState.RUNNING:
                if IS_ANDROID:
                    # getting the accleration sensor data from accelerometer
                    # acceleration_sensor_values is a tuple of (x, y, z) sensor data
                    jet.update(accelerometer.acceleration)
                else:
                    jet.update_on_keypress(pygame.key.get_pressed())

            # backgroud surfaces are updated even when game is paused
            backgrounds.update()                                                                            # updating game background
            mountains.update()                                                                              # updating mountains
            deserts.update()                                                                                # updating deserts
            moon.update()                                                                                   # updating moons
            clouds.update()                                                                                 # updating the position of the clouds

            incoming_missiles.update()                                                                      # updating the position of the enemy missiles
            deactivated_incoming_missiles.update()                                                          # updating the position of the deactivated enemy missiles
            scoretext_sprite.update()                                                                       # updating the game scoretext sprite which includes gameplay time, score, etc.
            game_env.dynamic.jet_missiles.update()                                                          # updating the position of bullets
            game_env.dynamic.tank_rockets.update()                                                          # updating the position of missiles launched by sam-launcher

            if stars:
                stars.update()                                                                              # updating the position of the stars
            if tanks:
                tanks.update((jet.rect.x + jet.rect.width / 2, jet.rect.y + jet.rect.height))               # updating the tank with the target position of the JET

        # --------------------------------------------------------
        # SCREEN BLITING AND UPDATING
        # --------------------------------------------------------
        game_env.dynamic.game_surface.fill(game_env.static.background_skyblue)                              # Filling screen with background color

        # parallax background is blitted only when the game is not in readt mode
        if game_state != GameState.READY_TO_RUN:
            [game_env.dynamic.game_surface.blit(_sprite.surf, _sprite.rect) for _sprite in backgrounds]     # bliting parallax backgrounds to game surface
            game_env.dynamic.game_surface.blit(moon.surf, moon.rect, special_flags=pygame.BLEND_ADD)        # bliting moon to game surface
            [game_env.dynamic.game_surface.blit(_sprite.surf, _sprite.rect) for _sprite in clouds]          # bliting parallax clouds to game surface
            [game_env.dynamic.game_surface.blit(_sprite.surf, _sprite.rect) for _sprite in mountains]       # bliting parallax mountains to game surface
            [game_env.dynamic.game_surface.blit(_sprite.surf, _sprite.rect) for _sprite in deserts]         # bliting parallax deserts to game surface

        # bliting all surfaces in sprites_to_draw Group
        # this has the active text-based sprite; jet, incoming-missiles, jet-missiles and all similar game items
        [game_env.dynamic.game_surface.blit(_sprite.surf, _sprite.rect) for _sprite in game_env.dynamic.sprites_to_draw]

        pygame.display.update()                                                                               # updating display to the screen
        game_env.dynamic.game_clock.tick(game_env.static.fps)                                               # to maintain constant FPS of the game

    pygame.mixer.music.stop()                                                                               # stopping game music
    pygame.mixer.quit()                                                                                     # stopping game sound mixer
    pygame.quit()                                                                                           # stopping pygame
    exit()


if __name__ == '__main__':
    # hide loading screen in case of ANDROID as the game has been loaded
    if IS_ANDROID:
        loadingscreen.hide_loading_screen()

    # initialize the game
    initialize()
