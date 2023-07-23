from typing import NoReturn, Callable

from apscheduler.schedulers.sync import Scheduler
from apscheduler.triggers.interval import IntervalTrigger

from backend.data_classes import ConfigData


class Scheduler_:
    def __init__(self, config_data: ConfigData):
        self.config_data = config_data
        self.scheduler = Scheduler()

    def _parse_trigger(self) -> IntervalTrigger | NoReturn:
        trigger_data = self.config_data.trigger
        type_ = trigger_data["type"]
        value = trigger_data["value"]
        match type_:
            case "interval":
                trigger = IntervalTrigger(seconds=int(value))
            case _:
                raise ValueError("Unsupported trigger type.")

        return trigger

    def add_schedule(self, task: Callable, *args):
        trigger = self._parse_trigger()
        self.scheduler.add_schedule(func_or_task_id=task, trigger=trigger, args=args)

    def run_scheduler(self):
        self.scheduler.run_until_stopped()
