# PyBluesky
### Version : 1.0.0 (android)


Author : Lakhya Jyoti Nath (ljnath)<br>
Date : April 2020 - May 2020<br>
Email : ljnath@ljnath.com<br>
Website : https://www.ljnath.com


[![Download PyBluesky](https://img.shields.io/sourceforge/dt/ljnath.svg)](https://sourceforge.net/projects/ljnath/files/latest/download)
[![GitHub license](https://img.shields.io/github/license/ljnath/PyBluesky)](https://github.com/ljnath/PyBluesky/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/ljnath/PyBluesky)](https://github.com/ljnath/PyBluesky/stargazers)

[![Download PyBluesky](https://sourceforge.net/sflogo.php?type=13&group_id=3215162)](https://sourceforge.net/p/ljnath/)  

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
