import json
from datetime import date
from unittest import mock

import pytest

from calculation_engine.handler import CalculationEngine

# from calculation_engine.operation_classes import DayTradeCalculate, NormalCalculate
from calculation_engine.exceptions import InvalidAnnualSummary


@pytest.fixture
def calculation_engine_instance(annual_summary_message):
    return CalculationEngine(json.dumps(annual_summary_message))


def test_invalid_calculation_engine_instance():
    with pytest.raises(InvalidAnnualSummary):
        CalculationEngine(json.dumps({"mensagem": "invalida"}))


@mock.patch("calculation_engine.handler.SimpleCappUtils.get_list_with_filters",)
def test_agroup_operations_by_operation_class(mock_get_list_with_filters, calculation_engine_instance):
    mock_get_list_with_filters.side_effect = [
        [
            {
                "date": date(2020, 10, 26),
                "operation_type": "purchase",
                "operation_class": "normal",
                "ticker": "ITSA4",
                "ticker_type": "stock",
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
        "day_trade": [
            {
                "date": date(2020, 10, 26),
                "operation_type": "purchase",
                "operation_class": "normal",
                "ticker": "ITSA4",
                "ticker_type": "stock",
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
            mock.call({"operation_class": "day_trade"}, operations),
            mock.call({"operation_class": "normal"}, operations),
        ]
    )


@mock.patch("calculation_engine.operation_classes.DayTradeCalculate.process",)
@mock.patch("calculation_engine.operation_classes.NormalCalculate.process",)
def test_process(mock_normal_process, mock_day_trade_process, calculation_engine_instance):
    calculation_engine_instance._agroup_operations_by_operation_class = mock.Mock(
        return_value={"normal": [1, 2], "day_trade": [3, 4]}
    )
    mock_normal_process.return_value = {
        "summary_by_ticker": [5, 6],
        "custody_by_ticker_and_reference_year": [7, 8],
        "summary_by_monthly": [8, 9],
        "inconsistencies": [10, 11],
    }
    mock_day_trade_process.return_value = {
        "summary_by_ticker": [12, 13],
        "custody_by_ticker_and_reference_year": [14, 15],
        "summary_by_monthly": [16, 17],
        "inconsistencies": [18, 19],
    }

    assert calculation_engine_instance.process() == None

    calculation_engine_instance._agroup_operations_by_operation_class.assert_called_once_with(
        calculation_engine_instance.annual_summary.financial_operations
    )

    mock_normal_process.assert_called_once_with([1, 2], 2020, [])

    mock_day_trade_process.assert_called_once_with([3, 4], 2020, [])

