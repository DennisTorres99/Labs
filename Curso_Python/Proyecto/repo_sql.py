from db import SessionLocal
from domain import Order
from models import OrderModel


class SqlOrderRepository:
    def save(self, order: Order) -> None:
        db = SessionLocal()
        db.add(OrderModel(id=order.id, total=order.total))
        db.commit()
        db.close()

    def get_all(self):
        db = SessionLocal()
        result = db.query(OrderModel).all()
        db.close()

        return [Order(o.id, o.total) for o in result]
