import pytest


@pytest.fixture
def finantial_operation_message():
    return {
        "date": "2020-10-26",
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


@pytest.fixture
def annual_summary_message(finantial_operation_message):
    return {
        "customer_name": "Henry Roetger Silva",
        "customer_cpf": "06716477927",
        "reference_year": 2020,
        "financial_operations": [
            finantial_operation_message,
            finantial_operation_message,
        ],
    }

