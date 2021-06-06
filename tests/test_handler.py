import pytest
import json
from datetime import date

from calculation_engine.handler import CalculationEngine
from unittest import mock


@pytest.fixture
def calculation_engine_instance(annual_summary_message):
    return CalculationEngine(json.dumps(annual_summary_message))


@mock.patch("calculation_engine.handler.SimpleCappUtils.get_list_with_filters",)
def test_agroup_operations_by_operation_class(
    mock_get_list_with_filters, calculation_engine_instance
):
    mock_get_list_with_filters.side_effect = [
        [
            {
                "date": date(2020, 10, 26),
                "operation_type": "day-trade",
                "operation_class": "normal",
                "ticker": "ITSA4",
                "ticker_type": "stook",
                "units": 4,
                "unitary_value": 99.00,
                "amount": 396.00,
                "operation_costs": 0.12,
                "currency_code": "BRL",
                "irrf": 0.015,
            }
        ],
        [
            {
                "date": date(2020, 10, 26),
                "operation_type": "purchase",
                "operation_class": "normal",
                "ticker": "CPTS11",
                "ticker_type": "FIIs",
                "units": 4,
                "unitary_value": 99.00,
                "amount": 396.00,
                "operation_costs": 0.12,
                "currency_code": "BRL",
                "irrf": 0.015,
            }
        ],
    ]
    operations = calculation_engine_instance.annual_summary.financial_operations

    expected_agrouped_operations_by_operation_class = {
        "day-trade": [
            {
                "date": date(2020, 10, 26),
                "operation_type": "day-trade",
                "operation_class": "normal",
                "ticker": "ITSA4",
                "ticker_type": "stook",
                "units": 4,
                "unitary_value": 99.00,
                "amount": 396.00,
                "operation_costs": 0.12,
                "currency_code": "BRL",
                "irrf": 0.015,
            }
        ],
        "normal": [
            {
                "date": date(2020, 10, 26),
                "operation_type": "purchase",
                "operation_class": "normal",
                "ticker": "CPTS11",
                "ticker_type": "FIIs",
                "units": 4,
                "unitary_value": 99.00,
                "amount": 396.00,
                "operation_costs": 0.12,
                "currency_code": "BRL",
                "irrf": 0.015,
            }
        ],
    }

    assert (
        calculation_engine_instance._agroup_operations_by_operation_class(operations)
        == expected_agrouped_operations_by_operation_class
    )

    mock_get_list_with_filters.assert_has_calls(
        [
            mock.call({"operation_class": "day-trade"}, operations),
            mock.call({"operation_class": "normal"}, operations),
        ]
    )

