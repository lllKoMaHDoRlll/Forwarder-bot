from pathlib import Path

from backend.message_sender import MessageSender
from backend.posts_parser import PostsParser
from backend.scheduler import Scheduler_
from backend.utils_ import get_config


class Forwarder:
    def __init__(self, config_path: Path | None = None):
        if config_path:
            self.config_data = get_config(config_path)
        else:
            self.config_data = get_config()
        self.message_sender = MessageSender(self.config_data)
        self.posts_parser = PostsParser(self.config_data)
        self.scheduler = Scheduler_(self.config_data)

    def load(self):
        self.scheduler.add_schedule(self.forward_posts)

    def start(self):
        self.scheduler.run_scheduler()

    def forward_posts(self):
        posts_to_send = self.posts_parser.get_posts_to_send()
        self.message_sender.send_posts(posts_to_send)


