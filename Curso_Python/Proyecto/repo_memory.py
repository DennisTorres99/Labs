from typing import List

from domain import Order


class InMemoryOrderRepository:
    def __init__(self):
        self.storage = []

    def save(self, order: Order) -> None:
        self.storage.append(order)

    def get_all(self) -> List[Order]:
        return self.storage
