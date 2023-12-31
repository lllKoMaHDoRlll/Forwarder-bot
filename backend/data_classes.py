from dataclasses import dataclass


@dataclass
class ConfigData:
    tg_token: str
    vk_token: str
    from_channel_id: int
    to_group_id: int
    vk_api_version: str
    trigger: dict[str, int | str]


@dataclass
class PlainTextPost:
    text: str

@dataclass
class PhotoPost:
    photos_url: list[str]
    caption: str | None = None

