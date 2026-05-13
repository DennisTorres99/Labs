from typing import List, Protocol


class Order:
    def __init__(self, id: int, total: float):
        self.id = id
        self.total = total


class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...
    def get_all(self) -> List[Order]: ...


class Notifier(Protocol):
    def notify(self, order: Order) -> None: ...


class CreateOrder:
    def __init__(self, repo: OrderRepository, notifier: Notifier):
        self.repo = repo
        self.notifier = notifier

    def execute(self, id: int, total: float):
        order = Order(id, total)
        self.repo.save(order)
        self.notifier.notify(order)
        return order


class InMemoryOrderRepository:
    def __init__(self):
        self.storage = []

    def save(self, order: Order) -> None:
        self.storage.append(order)

    def get_all(self) -> List[Order]:
        return self.storage


class SqlOrderRepository:
    def __init__(self):
        self._db = []

    def save(self, order: Order) -> None:
        self._db.append(order)

    def get_all(self) -> List[Order]:
        return self._db


class HttpNotifier:
    def notify(self, order: Order) -> None:
        print("HTTP notify order", order.id)


def run(repo: OrderRepository):
    notifier = HttpNotifier()
    use_case = CreateOrder(repo, notifier)

    use_case.execute(1, 100)
    use_case.execute(2, 200)

    return [o.id for o in repo.get_all()]


if __name__ == "__main__":
    mem = run(InMemoryOrderRepository())
    sql = run(SqlOrderRepository())

    print(mem)
    print(sql)

    assert mem == sql
