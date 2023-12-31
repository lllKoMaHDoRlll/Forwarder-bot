from typing import NoReturn

from vk import API

from backend.data_classes import ConfigData, PlainTextPost, PhotoPost
from backend.exceptions import GettingPostsError


class PostsParser:
    def __init__(self, config_data: ConfigData):
        self.config_data = config_data
        self.vk_api = API(access_token=self.config_data.vk_token, v=self.config_data.vk_api_version)
        self.last_post_timestamp = self._get_last_post_timestamp()

    def _get_raw_channel_posts(self, count: int = 15) -> dict | NoReturn:
        try:
            return self.vk_api.wall.get(owner_id=self.config_data.from_channel_id, count=count)
        except Exception as error:
            raise GettingPostsError("Error has occurred while accessing VK API: {}".format(error))

    def _filter_new_posts(self, raw_posts: list) -> list | NoReturn:
        new_posts: list[dict] = []

        try:
            for post in raw_posts:
                if int(post["date"]) <= self.last_post_timestamp:
                    return new_posts

                new_posts.append(post)

            return new_posts
        except Exception as error:
            raise GettingPostsError("Error with filtering new posts: {}".format(error))

    def _get_last_post_timestamp(self) -> int:
        try:
            timestamp = self._get_raw_channel_posts(count=1)["items"][0]["date"]
        except GettingPostsError:
            timestamp = 0
        except KeyError:
            timestamp = 0
        return timestamp

    @staticmethod
    def _get_best_photo_resolution_index(photo_sizes: list) -> int:
        best_resolution_index = 0
        best_resolution = 0
        for index in range(len(photo_sizes)):
            try:
                photo_width = photo_sizes[index]["width"]
                photo_height = photo_sizes[index]["height"]
                photo_resolution = photo_width * photo_height
                if photo_resolution >= best_resolution:
                    best_resolution_index = index
            except Exception:
                pass
        return best_resolution_index

    def _form_post_object(self, post: dict) -> PlainTextPost | PhotoPost | NoReturn:
        try:
            if post["attachments"]:
                photos = []
                for attachment in post["attachments"]:
                    if attachment["type"] == "photo":
                        photo = attachment["photo"]
                        best_photo_size = self._get_best_photo_resolution_index(photo["sizes"])
                        photos.append(photo["sizes"][best_photo_size]["url"])

                if photos:
                    post_object = PhotoPost(photos_url=photos, caption=post["text"])
                    return post_object
            elif post["text"]:
                post_object = PlainTextPost(text=post["text"])
                return post_object
            else:
                raise ValueError("Unhandled post type")
        except Exception as error:
            raise GettingPostsError("Error with forming post object: {}".format(error))

    def _update_last_post_timestamp(self, timestamp: int) -> None:
        self.last_post_timestamp = timestamp

    def get_posts_to_send(self) -> list[PhotoPost | PlainTextPost]:
        try:
            raw_posts = self._get_raw_channel_posts()["items"]
            raw_filtered_posts = self._filter_new_posts(raw_posts)
            self._update_last_post_timestamp(raw_posts[0]["date"])
        except GettingPostsError as ex:
            return []

        posts_to_send: list[PhotoPost | PlainTextPost] = []
        for post in raw_filtered_posts:
            try:
                post_object = self._form_post_object(post)
                posts_to_send.append(post_object)
            except GettingPostsError:
                pass

        return posts_to_send
