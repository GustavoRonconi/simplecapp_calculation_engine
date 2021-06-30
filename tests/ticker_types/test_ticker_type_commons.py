import pytest

from simplecapp_calculation_engine.ticker_types import (BDR, RealStateFunds, Stock,
                                             TickerTypesCommons)


@pytest.mark.parametrize(
    "ticker_type_instance, total_amount_sale, expected_result",
    [(BDR(), 0.0, True), (Stock(), 19000, False), (RealStateFunds(), 1, True)],
)
def test_get_ir_flag(ticker_type_instance, total_amount_sale, expected_result):
    assert ticker_type_instance.get_ir_flag(total_amount_sale) == expected_result


@pytest.mark.parametrize(
    "ticker_type_instance, result, accumulated_loss, irrf, expected_result",
    [(BDR(), 100, 50, 5, 5), (Stock(), 100, 150, 5, 0), (RealStateFunds(), 100, 50, 5, 5)],
)
def test_calcule_ir_to_pay(ticker_type_instance, result, accumulated_loss, irrf, expected_result):
    assert ticker_type_instance.calcule_ir_to_pay(result, accumulated_loss, irrf) == expected_result


@pytest.mark.parametrize(
    "ticker_type_instance, operations, expected_result",
    [
        (
            BDR(),
            [],
            {"summary_by_ticker": [], "custody_by_ticker_and_reference_year": [], "summary_by_monthly": [],},
        ),
        (Stock(), [1, 2], {"tudo": "ok"}),
        (RealStateFunds(), [1, 2], {"tudo": "ok"}),
    ],
)
def test_process(ticker_type_instance, operations, expected_result):
    reference_year = 2020
    previous_year_loss = [1, 2]
    average_price = {"a": 1}

    def operation_function(operations, reference_year, previous_year_loss, average_price):
        return {"tudo": "ok"}

    assert (
        ticker_type_instance.process(
            operations, reference_year, previous_year_loss, operation_function, average_price
        )
        == expected_result
    )
