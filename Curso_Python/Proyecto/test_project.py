from repo_memory import InMemoryOrderRepository
from repo_sql import SqlOrderRepository
from use_cases import CreateOrder


class FakeNotifier:
    def __init__(self):
        self.count = 0

    def notify(self, order):
        self.count += 1


def test_create_order_memory():
    repo = InMemoryOrderRepository()
    notifier = FakeNotifier()
    use_case = CreateOrder(repo, notifier)

    use_case.execute(1, 100)

    assert len(repo.get_all()) == 1
    assert notifier.count == 1


def test_create_order_sql():
    repo = SqlOrderRepository()
    notifier = FakeNotifier()
    use_case = CreateOrder(repo, notifier)

    use_case.execute(1, 100)

    assert len(repo.get_all()) == 1
    assert notifier.count == 1


def test_repository_contract():
    repos = [InMemoryOrderRepository(), SqlOrderRepository()]

    results = []
    for repo in repos:
        notifier = FakeNotifier()
        use_case = CreateOrder(repo, notifier)
        use_case.execute(1, 100)
        results.append(len(repo.get_all()))

    assert results == [1, 1]
