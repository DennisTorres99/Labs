from app import models, schemas
from app.deps import get_current_user, get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", response_model=schemas.OrderResponse)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_order = models.Order(description=order.description)

    for item in order.items:
        db_order.items.append(
            models.OrderItem(
                name=item.name,
                quantity=item.quantity,
            )
        )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


@router.get("/", response_model=list[schemas.OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    orders = db.query(models.Order).all()
    return orders
