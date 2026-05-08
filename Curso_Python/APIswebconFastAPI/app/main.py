from app.auth import authenticate_user, create_access_token
from app.db import engine
from app.models import Base
from app.routers import orders
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Orders API", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(orders.router)


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login", tags=["auth"])
def login(data: LoginRequest):
    user = authenticate_user(data.username, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({"sub": user["username"]})

    return {"access_token": token}


@app.get("/", tags=["default"])
def root():
    return {"message": "API funcionando correctamente"}
