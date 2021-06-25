import asyncio
from json import loads
from time import time

import aiohttp
from game.environment import GameEnvironment
from game.handlers import Handlers
from game.handlers.serialize import SerializeHandler
from jnius import autoclass


class NetworkHandler(Handlers):
    def __init__(self, api_key):
        Handlers().__init__()
        game_env = GameEnvironment()
        self.__api_key = api_key
        self.__api_endpoint = 'https://app.ljnath.com/pybluesky/'
        self.__serialize_handler = SerializeHandler(game_env.static.offline_score_file)

    async def check_game_update(self):
        try:
            game_env = GameEnvironment()
            get_parameters = {
                'action': 'getUpdate',
                'apiKey': self.__api_key,
                'platform': 'android'
                }
            async with aiohttp.ClientSession() as session:
                async with session.get(self.__api_endpoint, params=get_parameters, ssl=False, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status != 200:
                        raise Exception()
                    json_response = loads(await response.text())
                    if json_response['version'] != game_env.static.version:
                        game_env.dynamic.update_available = True
                        game_env.dynamic.update_url = json_response['url']
                        self.log('New game version {} detected'.format(json_response['version']))
        except Exception:
            self.log('Failed to check for game update')
        await self.submit_result(only_sync=True)

    async def get_leaders(self):
        leaders = {}
        try:
            get_parameters = {
                'action': 'getTopScores',
                'apiKey': self.__api_key,
                'platform': 'android'
                }
            async with aiohttp.ClientSession() as session:
                async with session.get(self.__api_endpoint, params=get_parameters, ssl=False, timeout=aiohttp.ClientTimeout(total=15)) as response:
                    if response.status != 200:
                        raise Exception()
                    leaders = loads(await response.text())
        except Exception:
            self.log('Failed to get game leaders from remote server')
        finally:
            return leaders

    async def submit_result(self, only_sync=False):
        payloads = []
        game_env = GameEnvironment()
        deserialized_object = self.__serialize_handler.deserialize()
        if deserialized_object:
            payloads = list(deserialized_object)

        build = autoclass("android.os.Build")
        if not only_sync:
            payload = {
                'apiKey': self.__api_key,
                'name': f'{game_env.dynamic.player_name} ({build.MODEL})',
                'score': game_env.dynamic.game_score,
                'level': game_env.dynamic.game_level,
                'accuracy': game_env.dynamic.accuracy,
                'platform': 'android',
                "epoch": int(time())
            }
            payloads.append(payload)

        unprocessed_payloads = []
        async with aiohttp.ClientSession() as session:
            put_tasks = [asyncio.ensure_future(self.__post_results(session, payload)) for payload in payloads]
            await asyncio.gather(*put_tasks, return_exceptions=False)

            for task, payload in zip(put_tasks, payloads):
                if task._result:
                    self.log('Successfully submitted result: score={}, name={}, level={}'.format(payload.get('score'), payload.get('name'), payload.get('level')))
                else:
                    payload.update({'apiKey': ''})
                    unprocessed_payloads.append(payload)
                    self.log('Failed to submit game scrore: score={}, name={}, level={}'.format(payload.get('score'), payload.get('name'), payload.get('level')))

        self.__serialize_handler.serialize(unprocessed_payloads)

    async def __post_results(self, session, payload):
        result = True
        try:
            payload['apiKey'] = self.__api_key
            async with session.put(self.__api_endpoint, json=payload, ssl=False, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status not in (200, 201):
                    result = False
        except Exception:
            result = False
        finally:
            return result
