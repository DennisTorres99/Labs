from lab_hexagonal import CreateOrder, InMemoryOrderRepository, SqlOrderRepository


class FakeNotifier:
    def __init__(self):
        self.called = 0

    def notify(self, order):
        self.called += 1


def test_create_order_memory():
    repo = InMemoryOrderRepository()
    notifier = FakeNotifier()
    use_case = CreateOrder(repo, notifier)

    use_case.execute(1, 100)

    assert len(repo.get_all()) == 1
    assert notifier.called == 1


def test_create_order_sql():
    repo = SqlOrderRepository()
    notifier = FakeNotifier()
    use_case = CreateOrder(repo, notifier)

    use_case.execute(1, 100)

    assert len(repo.get_all()) == 1
    assert notifier.called == 1


def test_lsp():
    repos = [InMemoryOrderRepository(), SqlOrderRepository()]

    results = []
    for repo in repos:
        notifier = FakeNotifier()
        use_case = CreateOrder(repo, notifier)
        use_case.execute(1, 100)
        results.append(len(repo.get_all()))

    assert results == [1, 1]
