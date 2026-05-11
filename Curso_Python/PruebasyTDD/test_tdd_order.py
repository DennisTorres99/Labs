from unittest.mock import patch

import pytest
from hypothesis import given
from hypothesis import strategies as st
from tdd_order import calculate_total, calculate_total_with_external_tax


@pytest.fixture
def sample_items():
    return [100, 50]


@pytest.fixture
def default_tax():
    return 0.1


@pytest.fixture
def order_data():
    return {
        "items": [100, 50],
        "tax": 0.1,
    }


@pytest.fixture
def large_order():
    return [10, 20, 30, 40]


def test_basic(sample_items, default_tax):
    assert calculate_total(sample_items, default_tax) == 165.0


@pytest.mark.parametrize(
    "items, tax, expected",
    [
        ([100], 0.1, 110.0),
        ([50, 50], 0.2, 120.0),
        ([0], 0.1, 0.0),
        ([], 0.1, 0.0),
    ],
)
def test_param(items, tax, expected):
    assert calculate_total(items, tax) == expected


def test_negative_tax():
    with pytest.raises(ValueError):
        calculate_total([100], -0.1)


def test_with_order_data(order_data):
    result = calculate_total(order_data["items"], order_data["tax"])
    assert result == 165.0


def test_large_order(large_order):
    result = calculate_total(large_order, 0.2)
    assert result == 120.0


@given(
    st.lists(st.floats(min_value=0, max_value=100)),
    st.floats(min_value=0, max_value=0.3),
)
def test_total_non_negative(items, tax):
    result = calculate_total(items, tax)
    assert result >= 0


# -------------------------
# MOCKING
# -------------------------


@patch("tdd_order.get_tax_rate")
def test_mock_tax_20_percent(mock_tax):
    mock_tax.return_value = 0.2

    result = calculate_total_with_external_tax([100])

    assert result == 120.0


@patch("tdd_order.get_tax_rate")
def test_mock_tax_zero(mock_tax):
    mock_tax.return_value = 0.0

    result = calculate_total_with_external_tax([100])

    assert result == 100.0


@patch("tdd_order.get_tax_rate")
def test_mock_tax_called(mock_tax):
    calculate_total_with_external_tax([50])

    mock_tax.assert_called_once()
