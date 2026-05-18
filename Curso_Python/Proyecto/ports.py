from typing import List, Protocol

from domain import Order


class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...
    def get_all(self) -> List[Order]: ...


class Notifier(Protocol):
    def notify(self, order: Order) -> None: ...
