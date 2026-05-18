from domain import Order


class HttpNotifier:
    def notify(self, order: Order) -> None:
        print("Notify order", order.id)
