from vk import API
from telebot import TeleBot

from backend.data_classes import ConfigData


class ForwarderHandler:
    def __init__(self, bot: TeleBot, vk_api: API, config_data: ConfigData):
        self.config_data = config_data
        self.vk_api = vk_api
        self.bot = bot

    def forward_photo(self, photo: str, caption: str | None = None) -> None:
        self.bot.send_photo(chat_id=self.config_data.to_group_id, photo=photo, caption=caption)

    async def forward_message(self, text: str) -> None:
        self.bot.send_message(chat_id=self.config_data.to_group_id, text=text)

    def get_channel_posts(self, count: int = 5):
        self.vk_api.wall.get(owner_id=self.config_data.from_channel_id, count=count)


