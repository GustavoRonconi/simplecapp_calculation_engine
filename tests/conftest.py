import pytest


@pytest.fixture
def finantial_normal_operation_message():
    return {
        "date": "2020-10-26",
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


@pytest.fixture
def finantial_day_trade_operation_message():
    return {
        "date": "2020-10-26",
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


@pytest.fixture
def annual_summary_message(
    finantial_normal_operation_message, finantial_day_trade_operation_message
):
    return {
        "customer_name": "Henry Roetger Silva",
        "customer_cpf": "06716477927",
        "reference_year": 2020,
        "financial_operations": [
            finantial_normal_operation_message,
            finantial_day_trade_operation_message,
        ],
    }

