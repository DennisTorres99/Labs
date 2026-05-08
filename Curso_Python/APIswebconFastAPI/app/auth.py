from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"


fake_user = {
    "username": "dennis",
    "password": "1234",
}


def authenticate_user(username: str, password: str):
    if username != fake_user["username"] or password != fake_user["password"]:
        return None
    return fake_user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
