from datetime import date

import pytest

from calculation_engine.models.finantial_operation import FinantialOperation


@pytest.fixture
def finantial_normal_operation_message():
    return {
        "date": "2020-10-26",
        "operation_type": "purchase",
        "operation_class": "normal",
        "ticker": "CPTS11",
        "ticker_type": "fiis",
        "units": 4,
        "unitary_value": 99.00,
        "amount": 396.00,
        "operation_costs": 0.12,
        "currency_code": "BRL",
        "irrf": 0.015,
        "broker": "clear",
    }


@pytest.fixture
def finantial_normal_operation(finantial_normal_operation_message):
    return FinantialOperation(**finantial_normal_operation_message)


@pytest.fixture
def finantial_day_trade_operation_message():
    return {
        "date": "2020-10-26",
        "operation_type": "purchase",
        "operation_class": "day_trade",
        "ticker": "ITSA4",
        "ticker_type": "stock",
        "units": 4,
        "unitary_value": 99.00,
        "amount": 396.00,
        "operation_costs": 0.12,
        "currency_code": "BRL",
        "irrf": 0.015,
        "broker": "xp",
    }


@pytest.fixture
def finantial_day_trade_operation(finantial_day_trade_operation_message):
    return FinantialOperation(**finantial_day_trade_operation_message)


@pytest.fixture
def annual_summary_message(finantial_normal_operation_message, finantial_day_trade_operation_message):
    return {
        "customer_name": "Henry Roetger Silva",
        "customer_cpf": "06716477927",
        "reference_year": 2020,
        "financial_operations": [finantial_normal_operation_message, finantial_day_trade_operation_message,],
    }


@pytest.fixture
def financial_normal_operations():
    financial_operations = [
        {
            "date": "2020-10-06",
            "operation_type": "purchase",
            "operation_class": "normal",
            "ticker": "XPLG11",
            "ticker_type": "fiis",
            "units": 1,
            "unitary_value": 127.80,
            "amount": None,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
        },
        {
            "date": "2020-10-11",
            "operation_type": "purchase",
            "operation_class": "normal",
            "ticker": "XPLG11",
            "ticker_type": "fiis",
            "units": 1,
            "unitary_value": 129.80,
            "amount": None,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
        },
        {
            "date": "2020-10-06",
            "operation_type": "purchase",
            "operation_class": "normal",
            "ticker": "XPLG11",
            "ticker_type": "fiis",
            "units": 3,
            "unitary_value": 127.80,
            "amount": None,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
        },
        {
            "date": "2020-11-06",
            "operation_type": "sale",
            "operation_class": "normal",
            "ticker": "XPLG11",
            "ticker_type": "fiis",
            "units": 1,
            "unitary_value": 128.80,
            "amount": 128.80,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
        },
        {
            "date": "2020-11-06",
            "operation_type": "sale",
            "operation_class": "normal",
            "ticker": "XPLG11",
            "ticker_type": "fiis",
            "units": 3,
            "unitary_value": 128.80,
            "amount": 386.43,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
        },
    ]

    return [FinantialOperation(**operation) for operation in financial_operations]

