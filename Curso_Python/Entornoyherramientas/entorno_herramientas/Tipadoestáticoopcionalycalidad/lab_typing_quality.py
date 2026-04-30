from __future__ import annotations

from collections.abc import Iterable
from typing import Literal, Protocol, TypedDict

EventType = Literal["INFO", "WARNING", "ERROR"]


class Event(TypedDict):
    id: int
    type: EventType
    message: str


class EventProcessor(Protocol):
    def process(self, event: Event) -> None: ...


class ConsoleEventProcessor:
    def process(self, event: Event) -> None:
        match event["type"]:
            case "INFO":
                print(f"[INFO] {event['message']}")
            case "WARNING":
                print(f"[WARNING] {event['message']}")
            case "ERROR":
                print(f"[ERROR] {event['message']}")


def process_events(
    events: Iterable[Event],
    processor: EventProcessor,
) -> None:
    for event in events:
        processor.process(event)


def main() -> None:
    events: list[Event] = [
        {"id": 1, "type": "DEBUG", "message": "Sistema iniciado para Dennis"},
        {"id": 2, "type": "WARNING", "message": "Uso elevado de memoria"},
        {"id": 3, "type": "ERROR", "message": "Fallo de conexión a base de datos"},
    ]

    processor = ConsoleEventProcessor()
    process_events(events, processor)


if __name__ == "__main__":
    main()
