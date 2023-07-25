import os
import json
import time
from typing import Literal

from telebot import TeleBot
from telebot.types import Update
from telebot.apihelper import ApiTelegramException
from vk import API
from vk.exceptions import VkAPIError


def _validate_tg_token(tg_token: str) -> bool:
    tg_api = TeleBot(tg_token)
    try:
        tg_api.get_me()
        return True
    except ApiTelegramException:
        print("Invalid telegram api token")
        return False


def _validate_vk_token(vk_token: str, api_version: str = "5.131") -> bool:
    vk_api = API(access_token=vk_token, v=api_version)
    try:
        vk_api.apps.get()
        return True
    except VkAPIError:
        print("Invalid vkontakte api token")
        return False


def _request_tokens() -> tuple[str, str]:
    tg_token = input("Enter telegram bot token: ")
    while not _validate_tg_token(tg_token):
        tg_token = input("Enter telegram bot token: ")

    vk_token = input("Enter vkontakte service token: ")
    while not _validate_vk_token(vk_token):
        vk_token = input("Enter vkontakte service token: ")

    return tg_token, vk_token


def _validate_vk_channel_domain(vk_api: API, vk_channel_domain: str) -> int | Literal[False]:
    try:
        res = vk_api.groups.getById(group_id=vk_channel_domain)[0]
        vk_channel_id = f"-{res['id']}"
        return int(vk_channel_id)
    except VkAPIError:
        print("Incorrect vkontakte group's domain")
        return False


def _request_vk_channel_domain(vk_api: API) -> int:
    vk_channel_domain = input("Enter vk group's short name (Ex: gumino): ")
    channel_id = _validate_vk_channel_domain(vk_api, vk_channel_domain)
    while not channel_id:
        vk_channel_domain = input("Enter vk group's short name (Ex: gumino): ")
        channel_id = _validate_vk_channel_domain(vk_api, vk_channel_domain)

    return channel_id


def _proceed_tg_updates(updates: list[Update]) -> int | Literal[False]:
    for update in updates:
        try:
            if update.message.text == "/setup":
                return update.message.chat.id
        except Exception:
            pass
    return False


def _get_tg_group_id(tg_api: TeleBot):
    print("Add your tg bot in tg group forward to and send message: /setup")

    while True:
        updates = tg_api.get_updates()
        tg_group_id = _proceed_tg_updates(updates)
        if tg_group_id:
            return tg_group_id
        else:
            time.sleep(5)


def setuper():
    tg_token, vk_token = _request_tokens()
    tg_api = TeleBot(tg_token)
    vk_api = API(access_token=vk_token, v="5.131")

    vk_channel_id = _request_vk_channel_domain(vk_api)
    tg_group_id = _get_tg_group_id(tg_api)

    try:
        os.mkdir("data")
    except FileExistsError:
        pass

    data = {
        "from_channel_id": vk_channel_id,
        "to_group_id": tg_group_id,
        "vk_api_version": "5.131",
        "trigger": {
            "type": "interval",
            "value": "5"
        }
    }
    json.dump(data, open("./data/config.json", "w"), indent=4)

    print("Config file was created. Add TG_TOKEN and VK_TOKEN to venv then start main.py")


if __name__ == "__main__":
    setuper()
