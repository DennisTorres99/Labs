from auth import create_token, verify_token
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from notifier_http import HttpNotifier
from repo_sql import SqlOrderRepository
from use_cases import CreateOrder

app = FastAPI()

repo = SqlOrderRepository()
notifier = HttpNotifier()
use_case = CreateOrder(repo, notifier)

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        return verify_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/login")
def login(username: str):
    token = create_token(username)
    return {"access_token": token}


@app.post("/orders")
def create_order(id: int, total: float, user=Depends(get_current_user)):
    order = use_case.execute(id, total)
    return {"id": order.id, "total": order.total}


@app.get("/orders")
def list_orders(user=Depends(get_current_user)):
    return [{"id": o.id, "total": o.total} for o in repo.get_all()]
