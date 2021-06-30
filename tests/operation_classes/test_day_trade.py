from unittest import mock

import pytest

from simplecapp_calculation_engine.operation_classes import DayTradeCalculate
from simplecapp_calculation_engine.ticker_types import Stock


@pytest.fixture
def day_trade_calculate_instance():
    return DayTradeCalculate()


@pytest.mark.parametrize(
    "year_month, expected_monthly_params",
    [
        (
            "10/2020",
            {
                "position": 0,
                "average_purchase_price": None,
                "total_amount_purchase": 127.88,
                "total_amount_sale": 129.72,
                "total_units_purchase": 1,
                "total_units_sale": 1,
                "cgs": None,
                "irrf": 0.04,
                "result": 1.8400000000000034,
            },
        ),
        (
            "11/2020",
            {
                "position": 0,
                "average_purchase_price": None,
                "total_amount_purchase": 383.4,
                "total_amount_sale": 386.40000000000003,
                "total_units_purchase": 3,
                "total_units_sale": 3,
                "cgs": None,
                "irrf": 0,
                "result": 3.000000000000057,
            },
        ),
        ("12/2020", None,),
    ],
)
def test_calcule_day_trade_operation_monthly_params(
    year_month, expected_monthly_params, day_trade_calculate_instance, financial_day_trade_operations
):
    ticker = "KGBRUSSIA"
    broker = "inter"
    assert (
        day_trade_calculate_instance._calcule_day_trade_operation_monthly_params(
            financial_day_trade_operations, year_month, ticker, broker
        )
        == expected_monthly_params
    )

    if year_month == "12/2020":
        assert (
            f"""Inconsistência encontrada p/ o ticker {ticker}, posição diferente de 0, cheque as operações do ticker."""
            in day_trade_calculate_instance.inconsistencies
        )


@mock.patch("simplecapp_calculation_engine.utils.SimpleCappUtils.get_unique_values",)
def test_calcule_operations_by_ticker(
    mock_get_unique_values,
    day_trade_calculate_instance,
    financial_day_trade_operations,
    year_months_to_reference_year,
):
    mock_get_unique_values.side_effect = [["KGBRUSSIA"], ["inter"]]
    setattr(day_trade_calculate_instance, "ticker_type_instance", Stock())
    day_trade_calculate_instance._calcule_day_trade_operation_monthly_params = mock.Mock(
        side_effect=[
            {
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            }
            for i in range(12)
        ]
    )

    expected_operations_by_ticker = {
        "summary_by_ticker": [
            {
                "year_month": "01/2020",
                "broker": "inter",
                "ticker_type": "stock",
                "ticker": "KGBRUSSIA",
                "operation_class": "day_trade",
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            },
            {
                "year_month": "02/2020",
                "broker": "inter",
                "ticker_type": "stock",
                "ticker": "KGBRUSSIA",
                "operation_class": "day_trade",
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            },
            {
                "year_month": "03/2020",
                "broker": "inter",
                "ticker_type": "stock",
                "ticker": "KGBRUSSIA",
                "operation_class": "day_trade",
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            },
            {
                "year_month": "04/2020",
                "broker": "inter",
                "ticker_type": "stock",
                "ticker": "KGBRUSSIA",
                "operation_class": "day_trade",
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            },
            {
                "year_month": "05/2020",
                "broker": "inter",
                "ticker_type": "stock",
                "ticker": "KGBRUSSIA",
                "operation_class": "day_trade",
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            },
            {
                "year_month": "06/2020",
                "broker": "inter",
                "ticker_type": "stock",
                "ticker": "KGBRUSSIA",
                "operation_class": "day_trade",
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            },
            {
                "year_month": "07/2020",
                "broker": "inter",
                "ticker_type": "stock",
                "ticker": "KGBRUSSIA",
                "operation_class": "day_trade",
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            },
            {
                "year_month": "08/2020",
                "broker": "inter",
                "ticker_type": "stock",
                "ticker": "KGBRUSSIA",
                "operation_class": "day_trade",
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            },
            {
                "year_month": "09/2020",
                "broker": "inter",
                "ticker_type": "stock",
                "ticker": "KGBRUSSIA",
                "operation_class": "day_trade",
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            },
            {
                "year_month": "10/2020",
                "broker": "inter",
                "ticker_type": "stock",
                "ticker": "KGBRUSSIA",
                "operation_class": "day_trade",
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            },
            {
                "year_month": "11/2020",
                "broker": "inter",
                "ticker_type": "stock",
                "ticker": "KGBRUSSIA",
                "operation_class": "day_trade",
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            },
            {
                "year_month": "12/2020",
                "broker": "inter",
                "ticker_type": "stock",
                "ticker": "KGBRUSSIA",
                "operation_class": "day_trade",
                "position": 0,
                "average_purchase_price": 0,
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
                "result": 0,
            },
        ],
        "custody_by_ticker_and_reference_year": [],
    }

    assert (
        day_trade_calculate_instance._calcule_operations_by_ticker(
            financial_day_trade_operations, 2020, year_months_to_reference_year
        )
        == expected_operations_by_ticker
    )

    assert mock_get_unique_values.call_count == 2
    day_trade_calculate_instance._calcule_day_trade_operation_monthly_params.call_count == 12
