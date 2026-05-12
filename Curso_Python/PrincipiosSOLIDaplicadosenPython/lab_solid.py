from typing import List, Protocol


class User:
    def __init__(self, name: str):
        self.name = name


class UserRepository(Protocol):
    def add(self, user: User) -> None: ...
    def get_all(self) -> List[User]: ...


class InMemoryUserRepository:
    def __init__(self):
        self.users = []

    def add(self, user: User) -> None:
        self.users.append(user)

    def get_all(self) -> List[User]:
        return self.users


class SqlUserRepository:
    def __init__(self):
        self._storage = []

    def add(self, user: User) -> None:
        self._storage.append(user)

    def get_all(self) -> List[User]:
        return self._storage


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, name: str):
        user = User(name)
        self.repo.add(user)

    def list_users(self) -> List[User]:
        return self.repo.get_all()


def run(repo: UserRepository):
    service = UserService(repo)

    service.create_user("Dennis")
    service.create_user("Luis")

    users = service.list_users()

    return [u.name for u in users]


if __name__ == "__main__":
    result_memory = run(InMemoryUserRepository())
    result_sql = run(SqlUserRepository())

    print("Memory:", result_memory)
    print("SQL:", result_sql)

    assert result_memory == result_sql
