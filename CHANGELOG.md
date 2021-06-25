# Changelog

## [1.0.5] - 2021-06-10
- changed default quit choice to No in ExitMenu
- added support to hide the exit menu if ESCAPE key is pressed
- code refactoring

## [1.0.4] - 2020-05-17
- added exit prompt in the game, this also acts as a game pause feature
- changed size of sam missile
- changed the probabity of a sam-launcher firing from 50% to 33%
- changed the sam speed increase, now speed increases by 1 every 2 level instead of 1 level
- changes the jet speed based on input mode; in mouse mode jet speed it slightly faster
- changed the cloud and vegetation speed by increasing the vegetation's speed and reducing the cloud's speed
- replaces threading in network communication with asyncio
- renamed ReplayText to ReplayMenuText

## [1.0.3] - 2020-05-10
- added support for new api
- added sam launcher, they appear after level 5 and fire targeted missiles
- added support to add 10 pts on each level up
- added support to calulate player accuracy
- added support to upload offline scores when internet connectivity is available thus so scores are lost
- added common logging and serilization for both network-handler and leaderboard-handler
- added ground and grass to the vegetation
- added support to automatically open the update URL incase an update is available
- moved all gama data files under the /data/ directory
- changed log file name to game.log
- changed API key handling from network-handler to main game file
- changes game asset names to lowercase for UNIX comaptibity and changed name to be more meaningful
- changes game asset path name for UNIX comaptibity
- fixed hint text in player name input screen
- fixed invalid player name input via file
- fixed unwanted library imports in game classes
- removed unused game assets
- removed README file from final game distrubution build

## [1.0.2] - 2020-05-04
- added support for player name, games prompts to enter the name for the 1st time and saving to file
- added support for automatically loading exitsing player name from file
- added support for player name to be used for submitting game result
- added special hint in the input name menu
- added support to save game level data along with game score
- added support to boost enemy missle speed by 5% after each 10th level
- changed starting missile count from 4 to 2 
- changed missile increase factor per level  to half
- changed input mode selection message in gamemenu sprite
- changed jet speed from 8 to 7
- changes TitleScreen enum to Screen as it has all type of screen information
- changed bullet speed from 5 to 7, to avoid jet hitting its own bullet
- changed game icon, shortcut icon
- fixed leaderboard rendereing issue related to alignment
- fixed help message
- replace duplicate codes with list comprehension
- removed capturing of system username

## [1.0.1] - 2020-05-03
- added leaderboard functionality (requires internet)
- added game help menu
- added support to toggle between menu in game start and gameover screen
- added support to upload game score and current system user to remote api
- added support to check for game update at startup
- added support for clouds to notify user about new game update
- added support for dynamic menu spries creation instead for pre-created sprites
- changed main game music
- removed game sound for jet move up and move down (no more licenses)

## [1.0.0] - 2020-05-02
- renamed game to PyBluesky
- added background vegetation support
- added packaging support

## [0.12] - 2020-05-02
- updated sprite for bullet, jet
- added support for flashing powerup star, flash rate is configurable in the class
- added music which powerup is activated
- added sprite for deactivated missiles to distinguishing between activated ones

## [0.11] - 2020-05-01
- added powerup star which will mark all active missiles as bad
- added suport for collision detection between the jet and its bullet
- consuming powerup will increase game score by 100

## [0.10] - 2020-05-01
- added ammo limit, game starts with 100 ammo and 50 is added pn every level up (max ammo can be 999)
- added support for game to run in full screen by default
- added support to dynamically set game resolution as the monitor resolution
- channged score sprite color to dark grey
- change levelup time from 10s to 20s

## [0.9] - 2020-05-01
- added shoot functionality for the jet by clicking mouse of pressing spacebar
- updated score calculation, now destroying 1 missile gives 10 pts
- added game instruction in welcome screen
- added sound effects for shooting and destroying missiles

## [0.8] - 2020-04-27
- added methods to continously move text on either X or Y axis
- added author sprite in the game menu

## [0.7] - 2020-04-26
- added game title in the menu
- added support for level up in the game, missile count will increase every level
- added sound for level up
- removed redundant condition check in jet sprite
- renamed GameInputText to GameMenuText

## [0.6] - 2020-04-26
- refactored game code into modules based on sprite
- introduced game environment to maintain and share game environment data across different various modules

## [0.5] - 2020-04-26
- added support for continous jet movement towards cursor; even on fixed mouse position

## [0.4] - 2020-04-26
- added suport for mouse movement as game input
- added input mode screen on game start
- fixed replay text sprite rendering

## [0.3] - 2020-04-25
- added support for game replay

## [0.2] - 2020-04-24
- refactored code and added comments
- changed jet image and collision sound
- changed cloud image and added support for random cloud design

## [0.1] - 2020-04-23
- first version with default game play
- added gameover message during collision
- added game scoring and playtime
