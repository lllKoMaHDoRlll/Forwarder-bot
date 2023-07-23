import json
import os
from pathlib import Path
from typing import NoReturn

from backend.data_classes import ConfigData
from backend.exceptions import LoadError


def get_config(config_path: Path = Path("./data/config.json")) -> ConfigData | NoReturn:
    if config_path.exists():
        try:
            with open(config_path, "r") as file:
                config_data = json.load(file)
                config_data.update({"tg_token": os.getenv("TG_TOKEN")})
                config_data.update({"vk_token": os.getenv("VK_TOKEN")})
            config_data = ConfigData(**config_data)
            return config_data
        except Exception:
            raise LoadError("Error while loading config.")
    else:
        raise LoadError("Config data file path does not exist.")
