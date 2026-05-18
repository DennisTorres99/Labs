from fastapi import FastAPI
from notifier_http import HttpNotifier
from repo_memory import InMemoryOrderRepository
from use_cases import CreateOrder

app = FastAPI()


repo = InMemoryOrderRepository()
notifier = HttpNotifier()
use_case = CreateOrder(repo, notifier)


@app.post("/orders")
def create_order(id: int, total: float):
    order = use_case.execute(id, total)
    return {"id": order.id, "total": order.total}


@app.get("/orders")
def list_orders():
    return [{"id": o.id, "total": o.total} for o in repo.get_all()]
