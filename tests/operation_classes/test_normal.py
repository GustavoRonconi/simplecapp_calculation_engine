import pytest
from datetime import date

from calculation_engine.operation_classes.normal import NormalCalculate


@pytest.fixture
def normal_calculate_instance():
    return NormalCalculate()


def test_get_last_position_average_price_for_month_previous_dates(normal_calculate_instance):
    year_month = "05/2020"
    average_price_by_ticker = {
        date(2020, 5, 3): {
            "position": 3,
            "average_purchase_price": 100,
            "operation_type": "purchase",
            "total_amount_with_operation_costs": 300,
        },
        date(2020, 5, 29): {
            "position": 2,
            "average_purchase_price": 100,
            "operation_type": "sale",
            "total_amount_with_operation_costs": 200,
        },
    }

    assert normal_calculate_instance._get_last_position_average_price_for_month(
        average_price_by_ticker, year_month
    ) == {"position": 2, "average_purchase_price": 100}


def test_get_last_position_average_price_for_month_later_dates(normal_calculate_instance):
    year_month = "05/2020"
    average_price_by_ticker = {
        date(2020, 6, 3): {
            "position": 3,
            "average_purchase_price": 100,
            "operation_type": "purchase",
            "total_amount_with_operation_costs": 300,
        },
        date(2020, 7, 29): {
            "position": 2,
            "average_purchase_price": 100,
            "operation_type": "sale",
            "total_amount_with_operation_costs": 200,
        },
    }

    assert normal_calculate_instance._get_last_position_average_price_for_month(
        average_price_by_ticker, year_month
    ) == {"position": 0.0, "average_purchase_price": 0.0}
