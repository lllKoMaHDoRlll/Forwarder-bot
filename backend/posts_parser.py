from vk import API

from backend.data_classes import ConfigData


class PostsParser:
    def __init__(self, config_data: ConfigData):
        self.config_data = config_data
        self.vk_api = API(access_token=self.config_data.vk_token, v=self.config_data.vk_api_version)
    