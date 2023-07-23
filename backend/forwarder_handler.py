from vk import API
from telebot import TeleBot

from backend.data_classes import ConfigData


class ForwarderHandler:
    def __init__(self, bot: TeleBot, vk_api: API, config_data: ConfigData):
        self.config_data = config_data
        self.vk_api = vk_api
        self.bot = bot
        self.last_post_timestamp: int = self._get_last_post_timestamp()

    def forward_photo(self, photo: str, caption: str | None = None) -> None:
        self.bot.send_photo(chat_id=self.config_data.to_group_id, photo=photo, caption=caption)

    async def forward_message(self, text: str) -> None:
        self.bot.send_message(chat_id=self.config_data.to_group_id, text=text)

    def _get_channel_posts(self, count: int = 5):
        return self.vk_api.wall.get(owner_id=self.config_data.from_channel_id, count=count)

    def _get_last_post_timestamp(self):
        post = self._get_channel_posts(count=1)
        return int(post["items"][0]["date"])

    def get_new_channel_posts(self):
        posts = []
        for post in self._get_channel_posts()["items"]:
            if int(post["date"]) <= self.last_post_timestamp:
                break
            posts.append(post)

        if posts:
            self.last_post_timestamp = int(posts[0]["date"])
        return posts

