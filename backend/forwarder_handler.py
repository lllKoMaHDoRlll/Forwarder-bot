from aiogram.types import Message, InputFile
from aiogram import Bot, Dispatcher

from backend.data_classes import ConfigData


class ForwarderHandler:
    def __init__(self, bot: Bot, config_data: ConfigData):
        self.config_data = config_data
        self.bot = bot

    async def forward_photo(self, photo: InputFile | None, caption: str | None) -> None:
        await self.bot.send_photo(chat_id=self.config_data.to_group_id, photo=photo, caption=caption)

    async def forward_message(self, text: str) -> None:
        await self.bot.send_message(chat_id=self.config_data.to_group_id, text=text)
