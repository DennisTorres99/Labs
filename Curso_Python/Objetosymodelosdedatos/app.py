from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from pydantic import BaseModel, Field


@dataclass(order=True)
class Order:
    """
    Entidad de dominio Order.
    Incluye comportamiento, estado y comparaciones.
    """

    order_id: int
    customer_name: str
    prices: list[float]
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def total(self) -> float:
        """Cálculo derivado."""
        return round(sum(self.prices), 2)

    def add_item(self, price: float) -> None:
        if price <= 0:
            raise ValueError("El precio debe ser mayor a cero")
        self.prices.append(price)

    def __str__(self) -> str:
        return (
            f"Order(id={self.order_id}, "
            f"customer='{self.customer_name}', "
            f"total={self.total})"
        )


class OrderIn(BaseModel):
    customer_name: str = Field(min_length=3)
    prices: list[float] = Field(min_items=1)

    def to_entity(self, order_id: int) -> Order:
        """Conversión DTO -> Entidad"""
        return Order(
            order_id=order_id,
            customer_name=self.customer_name,
            prices=list(self.prices),
        )


class OrderOut(BaseModel):
    order_id: int
    customer_name: str
    total: float
    created_at: datetime

    @classmethod
    def from_entity(cls, order: Order) -> OrderOut:
        """Conversión Entidad -> DTO"""
        return cls(
            order_id=order.order_id,
            customer_name=order.customer_name,
            total=order.total,
            created_at=order.created_at,
        )


def main() -> None:
    raw_input = {
        "customer_name": "Dennis Torres",
        "prices": [120.50, 80.25, 49.99],
    }

    order_in = OrderIn(**raw_input)

    order = order_in.to_entity(order_id=1)

    print("Entidad creada:")
    print(order)

    order.add_item(25.0)

    print("\nEntidad tras agregar item:")
    print(order)

    order_out = OrderOut.from_entity(order)

    print("\nSalida serializable (OrderOut):")
    print(order_out.model_dump())


if __name__ == "__main__":
    main()
