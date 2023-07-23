from dataclasses import dataclass


@dataclass
class ConfigData:
    token: str
    from_channel_id: int
    to_group_id: int

