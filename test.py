class ConfigStore:
    def get(self, key):
        print("called for key: {}".format(key))
        return key


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
        print(self._config_map)
        self._config_map[key]

config = Configurator()
config2 = Configurator()


config.get(1)
config.get(1)
config2.get(1)
config2.get(3)
