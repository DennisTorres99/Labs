from domain import Order


class SqlOrderRepository:
    def __init__(self):
        self._db = []

    def save(self, order: Order) -> None:
        self._db.append(order)

    def get_all(self):
        return self._db
