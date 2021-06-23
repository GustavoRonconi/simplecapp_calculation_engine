import pytest

from calculation_engine.operation_classes import DayTradeCalculate


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

