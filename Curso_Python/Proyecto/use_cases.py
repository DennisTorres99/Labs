from domain import Order
from ports import Notifier, OrderRepository


class CreateOrder:
    def __init__(self, repo: OrderRepository, notifier: Notifier):
        self.repo = repo
        self.notifier = notifier

    def execute(self, id: int, total: float) -> Order:
        order = Order(id, total)
        self.repo.save(order)
        self.notifier.notify(order)
        return order
