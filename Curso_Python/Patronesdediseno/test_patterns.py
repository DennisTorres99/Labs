from lab_patterns import (
    DiscountPricing,
    ExternalPricingAdapter,
    ExternalPricingAPI,
    PricingService,
    RegularPricing,
)


def test_strategy():
    service = PricingService(DiscountPricing())
    assert service.get_price(100) == 80


def test_adapter():
    adapter = ExternalPricingAdapter(ExternalPricingAPI())
    service = PricingService(adapter)
    assert service.get_price(100) == 90


def test_lsp():
    services = [
        PricingService(RegularPricing()),
        PricingService(DiscountPricing()),
        PricingService(ExternalPricingAdapter(ExternalPricingAPI())),
    ]

    results = [s.get_price(100) for s in services]

    assert results == [100, 80, 90]
