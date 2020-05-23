from flask import request
from flask_restful import Resource, Api
import redis
import json


class Config(Resource):
    def __init__(self, config_store=None):
        super(Config, self).__init__()
        self._config_store = ConfigStore(None)

    def patch(self):
        key = request.json.get("key")
        value = json.dumps(request.json.get("value"))
        self._config_store.set(key, value)
        return {
            "key": key,
            "value": value
        }


class GetConfig(Resource):
    def __init__(self, config_store=None):
        super(GetConfig, self).__init__()
        self._config_store = ConfigStore(None)

    def get(self, key):
        return {
            "key": key,
            "value": self._config_store.get(key)
        }


class ConfigStore(object):
    def __init__(self, store_client=None):
        self._store_client = redis.Redis(host='localhost', port=6379, db=0)

    def get(self, key):
        value = self.__get(key)
        return value

    def set(self, key, value):
        self._store_client.set(key, value)
        return value

    def __get(self, key):
        return str(
            self._store_client.get(key).decode('unicode_escape')
        )


class Configurator:
    _config_map = {}

    def __init__(self):
        self._config_store = ConfigStore()

    def get(self, key):
        value = self._config_map.get(key)
        if value:
            return value
        else:
            self._config_map[key] = self._config_store.get(key)
            return value
