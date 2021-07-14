# PyBluesky-android
### Version : 1.0.0


Author : Lakhya Jyoti Nath (ljnath)<br>
Date : June 2021<br>
Email : ljnath@ljnath.com<br>
Website : https://ljnath.com


[![GitHub license](https://img.shields.io/github/license/ljnath/PyBluesky-android)](https://github.com/ljnath/PyBluesky-android/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/ljnath/PyBluesky-android)](https://github.com/ljnath/PyBluesky-android/stargazers)
[![LGTM grade](https://img.shields.io/lgtm/grade/python/github/ljnath/PyBluesky-android)](https://lgtm.com/projects/g/ljnath/PyBluesky-android/)
[![LGTM alerts](https://img.shields.io/lgtm/alerts/github/ljnath/PyBluesky-android)](https://lgtm.com/projects/g/ljnath/PyBluesky-android/)


[![Google PlayStore](https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png)](https://play.google.com/store/apps/details?id=com.ljnath.pybluesky)

</br>
</br>

## INTRODUCTION
PyBluesky is a simple 2D python game developed using the pygame framework.</br>
Based on https://realpython.com/blog/python/pygame-a-primer
</br></br>

## GAME MECHANICS
The game is simple where the objective is to navigate and shoot your way through the sky.
There are enemy missiles which travels from right-to-left with varied speed. These enemy missiles can be destroyed by shooting at them. With increase in game level, SAM launchers also moves on the ground, which can fire targeted missile at the jet. These missiles cannot be destroyed, so user needs to evade them.

The gameplay has levels, which changes every 20 seconds. A level increase results in increases of enemy missiles.
It also gives 50 new ammo to the jet as well as the game score is bumped up by 10 points.

The game also features a power-up star which falls across the sky at each level.
Catching the power-up star will destroy all the enemy bullets in the current game frame.
</br></br>

## LEADERBOARD
The game also features a network-controlled leaderboard. User scores along with few other metadata are published to a remote server.

During the game startup, the updated scores are download from the server and displayed as leaderboard.
</br></br>

