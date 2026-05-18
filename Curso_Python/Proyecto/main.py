from notifier_http import HttpNotifier
from repo_memory import InMemoryOrderRepository
from repo_sql import SqlOrderRepository
from use_cases import CreateOrder


def run(repo):
    notifier = HttpNotifier()
    use_case = CreateOrder(repo, notifier)

    use_case.execute(1, 100)
    use_case.execute(2, 200)

    return [o.id for o in repo.get_all()]


mem = run(InMemoryOrderRepository())
sql = run(SqlOrderRepository())

print(mem)
print(sql)

assert mem == sql
