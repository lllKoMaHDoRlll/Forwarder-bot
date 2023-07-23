from aiogram.types import Message
from aiogram import Bot, Dispatcher

from backend.data_classes import ConfigData
from backend.utils_ import get_config
from backend.forwarder_handler import ForwarderHandler


class ForwarderBot:
    def __init__(self):
        self.config_data: None | ConfigData = None
        self._load()

    def _load(self):
        config_data = get_config()
        self.config_data = config_data
        print(self.config_data)

        self.bot = Bot(token=self.config_data.tg_token)
        self.forwarder_handler = ForwarderHandler(bot=self.bot, config_data=self.config_data)

        self.dispatcher = Dispatcher()

    async def echo(self, message: Message):
        print(message.chat.id)
        await message.send_copy(chat_id=self.config_data.to_group_id)

    def run(self):
        self.dispatcher.run_polling(self.bot)