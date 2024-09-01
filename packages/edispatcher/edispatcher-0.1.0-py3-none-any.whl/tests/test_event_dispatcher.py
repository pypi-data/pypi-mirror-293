from dataclasses import dataclass
from typing import Any

from edispatcher import EventDispatcher


@dataclass
class Event:
    name: str
    data: dict[str, Any]


class TestEventDispatcher:
    def test_dispatch(self):
        event = Event(name="event1", data={})
        handler1_result = None
        handler2_result = None
        handler3_result = None

        class Handler1:
            def handle(self, event):
                nonlocal handler1_result
                handler1_result = f"Handler1 handled {event.name}"

        class Handler2:
            def handle(self, event):
                nonlocal handler2_result
                handler2_result = f"Handler2 handled {event.name}"

        class Handler3:
            def handle(self, event):
                nonlocal handler2_result
                handler2_result = f"Handler2 handled {event.name}"

        event_dispatcher = EventDispatcher()
        event_dispatcher.register("event1", Handler1())
        event_dispatcher.register("event1", Handler2())
        event_dispatcher.register("event2", Handler3())

        event_dispatcher.dispatch(event)

        assert handler1_result == "Handler1 handled event1"
        assert handler2_result == "Handler2 handled event1"
        assert handler3_result is None
