from backend.data_classes import ConfigData
from backend.utils_ import get_config


class ForwarderBot:
    def __init__(self):
        self.config_data: None | ConfigData = None
        self._load()

    def _load(self):
        config_data = get_config()
        self.config_data = config_data
