def calculate_total(items: list[float], tax: float) -> float:
    if tax < 0:
        raise ValueError("Tax cannot be negative")

    subtotal = sum(items)
    total = subtotal * (1 + tax)
    return round(total, 2)


def get_tax_rate():
    return 0.1


def calculate_total_with_external_tax(items):
    tax = get_tax_rate()
    subtotal = sum(items)
    total = subtotal * (1 + tax)
    return round(total, 2)
