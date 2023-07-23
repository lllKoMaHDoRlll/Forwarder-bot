from typing import NoReturn

from vk import API

from backend.data_classes import ConfigData
from backend.exceptions import GettingPostsError


class PostsParser:
    def __init__(self, config_data: ConfigData):
        self.config_data = config_data
        self.vk_api = API(access_token=self.config_data.vk_token, v=self.config_data.vk_api_version)
        self.last_post_timestamp = self._get_last_post_timestamp()

    def _get_channel_posts_raw(self, count: int = 5) -> dict | NoReturn:
        try:
            return self.vk_api.wall.get(owner_id=self.config_data.from_channel_id, count=count)
        except Exception as error:
            raise GettingPostsError("Error has occurred while accessing VK API: {}".format(error))

    def _filter_new_posts(self, raw_posts: list) -> list | NoReturn:
        new_posts = []

        try:
            for post in raw_posts:
                if int(post["date"]) <= self.last_post_timestamp:
                    return new_posts

                new_posts.append(post)
        except Exception as error:
            raise GettingPostsError("Error with filtering new posts: {}".format(error))

    def _get_last_post_timestamp(self) -> int:
        try:
            timestamp = self._get_channel_posts_raw(count=1)
        except GettingPostsError:
            timestamp = 0
        return timestamp
