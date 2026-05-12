from typing import Protocol


class PricingStrategy(Protocol):
    def calculate(self, price: float) -> float: ...


class RegularPricing:
    def calculate(self, price: float) -> float:
        return price


class DiscountPricing:
    def calculate(self, price: float) -> float:
        return price * 0.8


class PricingService:
    def __init__(self, strategy: PricingStrategy):
        self.strategy = strategy

    def get_price(self, price: float) -> float:
        return self.strategy.calculate(price)


def cache(func):
    storage = {}

    def wrapper(x):
        if x in storage:
            return storage[x]
        result = func(x)
        storage[x] = result
        return result

    return wrapper


@cache
def expensive_calculation(x: int) -> int:
    total = 0
    for i in range(1_000_000):
        total += i * x
    return total


class ExternalPricingAPI:
    def get_price(self, amount: float) -> float:
        return amount * 0.9


class ExternalPricingAdapter:
    def __init__(self, api: ExternalPricingAPI):
        self.api = api

    def calculate(self, price: float) -> float:
        return self.api.get_price(price)


if __name__ == "__main__":
    service_regular = PricingService(RegularPricing())
    service_discount = PricingService(DiscountPricing())

    print(service_regular.get_price(100))
    print(service_discount.get_price(100))

    print(expensive_calculation(5))
    print(expensive_calculation(5))

    adapter = ExternalPricingAdapter(ExternalPricingAPI())
    service_external = PricingService(adapter)

    print(service_external.get_price(100))
