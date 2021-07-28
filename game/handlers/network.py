from json import dumps, loads
from time import time

from game import IS_ANDROID
from game.environment import GameEnvironment
from game.handlers import Handlers
from game.handlers.serialize import SerializeHandler

if IS_ANDROID:
    from jnius import autoclass


class NetworkHandler(Handlers):
    def __init__(self, api_key):
        Handlers().__init__()
        game_env = GameEnvironment()
        self.__api_key = api_key
        self.__api_endpoint = 'https://app.ljnath.com/pybluesky/'
        self.__serialize_handler = SerializeHandler(game_env.static.offline_score_file)

    def check_for_update(self):
        """
        method to check for new game update
        """
        try:
            game_env = GameEnvironment()
            get_parameters = {
                'action': 'getUpdate',
                'apiKey': self.__api_key
            }
            response = game_env.static.http_pool_manager.request('GET', self.__api_endpoint, fields=get_parameters)
            if response.status == 200:
                json_response = loads(response.data)
                if json_response['version'] != game_env.static.app_version:
                    game_env.dynamic.game_update_url = json_response['url']
                    self.log(f'New game version {json_response["version"]} detected')
        except Exception:
            self.log('Failed to check for game update')

    def get_leaders(self) -> dict:
        """
        method to get the current leaders from remote server
        :return leaders : leaders as dict object
        """
        leaders = {}
        try:
            game_env = GameEnvironment()
            get_parameters = {
                'action': 'getTopScores',
                'apiKey': self.__api_key
            }

            # updating request in case of android
            if IS_ANDROID:
                get_parameters['platform'] = 'android'

            response = game_env.static.http_pool_manager.request('GET', self.__api_endpoint, fields=get_parameters)
            if response.status == 200:
                leaders = loads(response.data)

        except Exception:
            self.log('Failed to get game leaders from remote server')
        finally:
            return leaders

    def submit_result(self, only_sync=False):
        """
        method to submit score to remote server. If the submission of scores fails, then the scores are stored in the device and in the next invocation of this method, those scores are re-submitted
        :param only_sync : bool value when false the current score is submitted else only the offline scores are submitted
        """
        payloads = []
        # reading offline scores which needs to be submitted
        deserialized_object = self.__serialize_handler.deserialize()
        if deserialized_object:
            payloads = list(deserialized_object)

        # when new score needs to be submitted as well
        if not only_sync:
            
            game_env = GameEnvironment()
            payload = {
                'apiKey': self.__api_key,
                'name': game_env.dynamic.player_name,
                'score': game_env.dynamic.game_score,
                'level': game_env.dynamic.game_level,
                'accuracy': game_env.dynamic.accuracy,
                "epoch": int(time())
            }

            # updating request in case of android
            if IS_ANDROID:
                build = autoclass("android.os.Build")
                payload['platform'] = 'android'
                payload['name'] = f'{game_env.dynamic.player_name} ({build.MODEL})'

            payloads.append(payload)

        unsubmitted_scores = []
        for payload in payloads:
            if not self.__submit_result(payload):
                payload['apiKey'] = ''
                unsubmitted_scores.append(payload)
                self.log('Failed to submit game scrore: score={}, name={}, level={}'.format(payload.get('score'), payload.get('name'), payload.get('level')))
            else:
                self.log('Successfully submitted result: score={}, name={}, level={}'.format(payload.get('score'), payload.get('name'), payload.get('level')))
        self.__serialize_handler.serialize(unsubmitted_scores)

    def __submit_result(self, payload: dict) -> bool:
        """
        private method to make api call for score submission
        :param payload : api payload as a dict object
        :return status : bool value indicating the status of the api call
        """
        status = False
        try:
            game_env = GameEnvironment()
            payload['apiKey'] = self.__api_key
            response = game_env.static.http_pool_manager.request('PUT', self.__api_endpoint, body=dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            if response.status == 201:
                status = True
        except Exception:
            status = False
        finally:
            return status
