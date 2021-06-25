from game.environment import GameEnvironment
from game.handlers import Handlers
from game.handlers.network import NetworkHandler
from game.handlers.serialize import SerializeHandler


class LeaderBoardHandler(Handlers):
    def __init__(self):
        Handlers().__init__()
        self.__game_env = GameEnvironment()
        self.__serialize_handler = SerializeHandler(self.__game_env.static.leaders_file)

    def load(self):
        leaders = []
        try:
            deserialized_object = self.__serialize_handler.deserialize()
            if deserialized_object:
                leaders = dict(deserialized_object)
        except Exception:
            self.log('Failed to read leaders from file {}'.format(self.__game_env.static.leaders_file))
        finally:
            return leaders

    def save(self, leaders):
        try:
            if leaders is None:
                return

            self.__serialize_handler.serialize(leaders)
        except Exception:
            self.log('Failed to save leaders to file {}'.format(self.__game_env.static.leaders_file))

    async def update(self, api_key):
        network_handler = NetworkHandler(api_key)
        self.save(await network_handler.get_leaders())
