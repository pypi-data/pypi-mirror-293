from lightmodelfactory.util.logger import logger

class AutoBuild(object):
    def __init__(self,name:str):
        self._name = name
        self._map = {}

    def register(self, key):
        def _register(cls):
            self._map[key] = cls
            return cls
        return _register

    def get_cls(self, key):
        logger.info(f"AutoBuild Map {self._map}")
        if key not in self._map:
            return None
        return self._map[key] 


PluginRg = AutoBuild('plugin')