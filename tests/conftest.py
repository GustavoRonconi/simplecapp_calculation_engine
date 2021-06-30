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
        "profile_id": 1,
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
            "irrf": 0.02,
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
            "irrf": 0.02,
        },
        {
            "date": "2020-10-12",
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
            "date": "2020-11-13",
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
            "date": "2020-11-17",
            "operation_type": "sale",
            "operation_class": "normal",
            "ticker": "XPLG11",
            "ticker_type": "fiis",
            "units": 3,
            "unitary_value": 128.81,
            "amount": 386.43,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
        },
        {
            "date": "2020-10-06",
            "operation_type": "purchase",
            "operation_class": "normal",
            "ticker": "KGBRUSSIA",
            "ticker_type": "stock",
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
            "ticker": "KGBRUSSIA",
            "ticker_type": "stock",
            "units": 1,
            "unitary_value": 129.80,
            "amount": None,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
        },
        {
            "date": "2020-10-12",
            "operation_type": "purchase",
            "operation_class": "normal",
            "ticker": "KGBRUSSIA",
            "ticker_type": "stock",
            "units": 3,
            "unitary_value": 127.80,
            "amount": None,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
        },
        {
            "date": "2020-11-13",
            "operation_type": "sale",
            "operation_class": "normal",
            "ticker": "KGBRUSSIA",
            "ticker_type": "stock",
            "units": 1,
            "unitary_value": 128.80,
            "amount": 128.80,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
        },
        {
            "date": "2020-11-19",
            "operation_type": "sale",
            "operation_class": "normal",
            "ticker": "KGBRUSSIA",
            "ticker_type": "stock",
            "units": 3,
            "unitary_value": 128.81,
            "amount": 386.43,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
        },
    ]

    return [FinantialOperation(**operation) for operation in financial_operations]


@pytest.fixture
def year_months_to_reference_year():
    return [
        "01/2020",
        "02/2020",
        "03/2020",
        "04/2020",
        "05/2020",
        "06/2020",
        "07/2020",
        "08/2020",
        "09/2020",
        "10/2020",
        "11/2020",
        "12/2020",
    ]


@pytest.fixture
def financial_day_trade_operations():
    financial_operations = [
        {
            "date": "2020-10-06",
            "operation_type": "purchase",
            "operation_class": "day_trade",
            "ticker": "KGBRUSSIA",
            "ticker_type": "stock",
            "units": 1,
            "unitary_value": 127.80,
            "amount": None,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
            "irrf": 0.02,
        },
        {
            "date": "2020-10-06",
            "operation_type": "sale",
            "operation_class": "day_trade",
            "ticker": "KGBRUSSIA",
            "ticker_type": "stock",
            "units": 1,
            "unitary_value": 129.80,
            "amount": None,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
            "irrf": 0.02,
        },
        {
            "date": "2020-11-12",
            "operation_type": "purchase",
            "operation_class": "day_trade",
            "ticker": "KGBRUSSIA",
            "ticker_type": "stock",
            "units": 3,
            "unitary_value": 127.80,
            "amount": None,
            "operation_costs": 0.0,
            "currency_code": "BRL",
            "broker": "inter",
        },
        {
            "date": "2020-11-12",
            "operation_type": "sale",
            "operation_class": "day_trade",
            "ticker": "KGBRUSSIA",
            "ticker_type": "stock",
            "units": 3,
            "unitary_value": 128.80,
            "amount": None,
            "operation_costs": 0.00,
            "currency_code": "BRL",
            "broker": "inter",
        },
        {
            "date": "2020-12-19",
            "operation_type": "sale",
            "operation_class": "day_trade",
            "ticker": "KGBRUSSIA",
            "ticker_type": "stock",
            "units": 3,
            "unitary_value": 128.81,
            "amount": 386.43,
            "operation_costs": 0.08,
            "currency_code": "BRL",
            "broker": "inter",
        },
    ]

    return [FinantialOperation(**operation) for operation in financial_operations]
