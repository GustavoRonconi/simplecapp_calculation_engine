from datetime import date

import pytest
from calculation_engine.models.finantial_operation import FinantialOperation
from pydantic.error_wrappers import ValidationError


def test_finantial_operation_valid(finantial_operation_message):
    finantial_operation = FinantialOperation(**finantial_operation_message)

    expected_financial_operation = {
        "date": date(2020, 10, 26),
        "operation_type": "purchase",
        "operation_class": "normal",
        "paper": "CPTS11",
        "paper_type": "FIIs",
        "units": 4,
        "unitary_value": 99.00,
        "amount": 396.00,
        "emoluments": 0.12,
        "currency_code": "BRL",
    }

    assert finantial_operation.dict() == expected_financial_operation


@pytest.mark.parametrize(
    "field",
    [
        "date",
        "operation_type",
        "operation_class",
        "paper",
        "paper_type",
        "units",
        "unitary_value",
        "currency_code",
    ],
)
def test_finantial_operation_missing_required_fields(
    field, finantial_operation_message
):
    finantial_operation_message_invalid = finantial_operation_message.copy()
    del finantial_operation_message_invalid[field]

    with pytest.raises(ValidationError):
        FinantialOperation(**finantial_operation_message_invalid)


def test_finantial_operation_amount_none(finantial_operation_message):
    finantial_operation_message_without_amount = finantial_operation_message.copy()
    del finantial_operation_message_without_amount["amount"]
    finantial_operation = FinantialOperation(
        **finantial_operation_message_without_amount
    )

    assert finantial_operation.amount == (4 * 99.00)

