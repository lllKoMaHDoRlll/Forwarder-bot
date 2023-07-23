from telebot import TeleBot
from time import sleep
from vk import API

from backend.data_classes import ConfigData
from backend.utils_ import get_config
from backend.forwarder_handler import ForwarderHandler


class ForwarderBot:
    def __init__(self):
        self.config_data: None | ConfigData = None
        self.vk_api: None | API = None
        self.tg_bot: None | TeleBot = None
        self.forwarder_handler: None | ForwarderHandler = None
        self._load()

    def _load(self):
        config_data = get_config()
        self.config_data = config_data

        self.vk_api = API(access_token=self.config_data.vk_token, v="5.131")

        self.tg_bot = TeleBot(token=self.config_data.tg_token)
        self.forwarder_handler = ForwarderHandler(bot=self.tg_bot, config_data=self.config_data, vk_api=self.vk_api)


    def run(self):
        while True:
            sleep(10)
            new_posts = self.forwarder_handler.get_new_channel_posts()
            if new_posts:
                for post in new_posts:
                    if "attachments" in post.keys() and post["attachments"][0]["type"] == "photo":
                        self.forwarder_handler.forward_photo(post["attachments"][0]["photo"]["sizes"][-1]["url"])