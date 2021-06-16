from datetime import datetime

import pytest
from calculation_engine.models.annual_summary import AnnualSummary
from pydantic.error_wrappers import ValidationError


@pytest.mark.parametrize(
    "previous_year_results",
    [None, [{"year_month": "12/2019", "ticker_type": "stock", "operation_class": "normal", "result": -10}]],
)
def test_annual_summary_valid(
    previous_year_results,
    annual_summary_message,
    finantial_normal_operation_message,
    finantial_day_trade_operation_message,
):
    finantial_normal_operation_message["date"] = datetime.strptime(
        finantial_normal_operation_message["date"], "%Y-%m-%d"
    ).date()

    finantial_day_trade_operation_message["date"] = datetime.strptime(
        finantial_day_trade_operation_message["date"], "%Y-%m-%d"
    ).date()

    expected_annual_sumary = {
        "customer_name": "Henry Roetger Silva",
        "customer_cpf": "06716477927",
        "reference_year": 2020,
        "financial_operations": [finantial_normal_operation_message, finantial_day_trade_operation_message,],
        "previous_year_results": [],
    }
    if previous_year_results:
        annual_summary_message["previous_year_results"] = previous_year_results
        expected_annual_sumary["previous_year_results"] = previous_year_results

    annual_summary = AnnualSummary(**annual_summary_message)

    assert annual_summary.dict() == expected_annual_sumary


@pytest.mark.parametrize(
    "field", ["customer_name", "customer_cpf", "reference_year", "financial_operations",],
)
def test_annual_summary_missing_required_fields(field, annual_summary_message):
    annual_summary_message_invalid = annual_summary_message.copy()
    del annual_summary_message_invalid[field]

    with pytest.raises(ValidationError):
        AnnualSummary(**annual_summary_message_invalid)
