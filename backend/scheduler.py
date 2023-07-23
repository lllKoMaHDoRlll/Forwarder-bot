from typing import NoReturn, Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from backend.data_classes import ConfigData


class Scheduler:
    def __init__(self, config_data: ConfigData):
        self.config_data = config_data
        self.scheduler = BackgroundScheduler()

    def _parse_trigger(self) -> IntervalTrigger | NoReturn:
        trigger_data = self.config_data.trigger
        type_ = trigger_data["type"]
        value = int(trigger_data["value"])
        match type_:
            case "interval":
                trigger = IntervalTrigger(seconds=value)
            case _:
                raise ValueError("Unsupported trigger type.")

        return trigger

    def add_schedule(self, task: Callable, *args):
        trigger = self._parse_trigger()
        self.scheduler.add_job(func=task, trigger=trigger, args=args)

    def run_scheduler(self):
        self.scheduler.start()
