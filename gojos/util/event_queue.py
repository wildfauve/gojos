from typing import Dict, Callable
import queue
from dataclasses import dataclass


@dataclass
class Envelope:
    eventType: str
    payload: Dict


class EventQueue:
    subscriptions = {}

    @classmethod
    def publish(cls, event: Envelope):
        if not cls.subscriptions.get(event.eventType, None):
            return False
        for subscriber in cls.subscriptions.get(event.eventType, None):
            subscriber(event)
        return True

    @classmethod
    def subscribe(cls, event_type: str, callback: Callable):
        if (topic := cls.subscriptions.get(event_type, None)):
            topic.append(callback)
        else:
            cls.subscriptions[event_type] = [callback]
        return True
