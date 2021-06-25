from datetime import datetime

from game.environment import GameEnvironment


class Handlers():
    def __init__(self):
        pass

    def log(self, message):
        game_env = GameEnvironment()
        with open(game_env.static.game_log_file, 'a+') as file_handler:
            file_handler.write('\n[{:%Y-%m-%d %H:%M:%S.%f}] : {}'.format(datetime.now(), message))
