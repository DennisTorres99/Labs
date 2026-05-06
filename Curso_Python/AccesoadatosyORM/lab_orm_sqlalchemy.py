from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session, mapped_column,
                            relationship)


# ORM
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    orders: Mapped[list[Order]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name})"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped[User] = relationship(back_populates="orders")
    items: Mapped[list[OrderItem]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Order(id={self.id}, user_id={self.user_id})"


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int] = mapped_column(Integer)

    order: Mapped[Order] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"OrderItem(product={self.product}, quantity={self.quantity})"


def main() -> None:
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(name="Dennis")
        order = Order(user=user)
        order.items.extend(
            [
                OrderItem(product="Laptop", quantity=1),
                OrderItem(product="Mouse", quantity=2),
            ]
        )

        session.add(user)
        session.commit()

        users = session.query(User).all()
        for u in users:
            print(u)
            for o in u.orders:
                print(" ", o)
                for item in o.items:
                    print("   ", item)


if __name__ == "__main__":
    main()
