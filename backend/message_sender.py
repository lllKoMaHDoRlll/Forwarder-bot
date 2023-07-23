from telebot import TeleBot

from backend.data_classes import ConfigData, PhotoPost, PlainTextPost
from backend.exceptions import SendMessageError


class MessageSender:
    def __init__(self, config_data: ConfigData):
        self.config_data = config_data
        self.tg_api = TeleBot(token=self.config_data.tg_token)

    def _send_photo_post(self, post: PhotoPost) -> None:
        for photo_url in post.photos_url:
            try:
                self.tg_api.send_photo(chat_id=self.config_data.to_group_id, photo=photo_url, caption=post.caption)
            except Exception as error:
                raise SendMessageError("Error with sending photo: {}".format(error))

    def _send_plain_text_post(self, post: PlainTextPost) -> None:
        try:
            self.tg_api.send_message(chat_id=self.config_data.to_group_id, text=post.text)
        except Exception as error:
            raise SendMessageError("Error with sending plain text: {}".format(error))
