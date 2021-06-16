import pytest
from datetime import date
from unittest import mock

from calculation_engine.operation_classes.normal import NormalCalculate


@pytest.fixture
def normal_calculate_instance():
    return NormalCalculate()


def test_get_last_position_average_price_for_month_previous_dates(normal_calculate_instance):
    ticker = "alo_testando"
    year_month = "05/2020"
    average_price_by_ticker = {
        date(2020, 5, 3): {
            "position": 3,
            "average_purchase_price": 100,
            "operation_type": "purchase",
            "total_amount_with_operation_costs": 300,
        },
        date(2020, 5, 29): {
            "position": 2,
            "average_purchase_price": 100,
            "operation_type": "sale",
            "total_amount_with_operation_costs": 200,
        },
    }

    assert normal_calculate_instance._get_last_position_average_price_for_month(
        average_price_by_ticker, year_month, ticker
    ) == {"position": 2, "average_purchase_price": 100}


def test_get_last_position_average_price_for_month_later_dates(normal_calculate_instance):
    ticker = "alo_testando"
    year_month = "05/2020"
    average_price_by_ticker = {
        date(2020, 6, 3): {
            "position": 3,
            "average_purchase_price": 100,
            "operation_type": "purchase",
            "total_amount_with_operation_costs": 300,
        },
        date(2020, 7, 29): {
            "position": 2,
            "average_purchase_price": 100,
            "operation_type": "sale",
            "total_amount_with_operation_costs": 200,
        },
    }

    assert normal_calculate_instance._get_last_position_average_price_for_month(
        average_price_by_ticker, year_month, ticker
    ) == {"position": 0.0, "average_purchase_price": 0.0}


def test_get_last_position_average_price_for_month_negative_position(normal_calculate_instance):
    normal_calculate_instance.append_inconsistency = mock.MagicMock()

    ticker = "alo_testando"
    year_month = "05/2020"

    average_price_by_ticker = {
        date(2020, 5, 3): {
            "position": 3,
            "average_purchase_price": 100,
            "operation_type": "purchase",
            "total_amount_with_operation_costs": 300,
        },
        date(2020, 5, 29): {
            "position": -2,
            "average_purchase_price": 100,
            "operation_type": "sale",
            "total_amount_with_operation_costs": 200,
        },
    }
    message = (
        f"""Inconsistência encontrada p/ o ticker {ticker}, posição negativa -2, """
        "certifique-se de que os lançamentos de compra foram processados"
    )

    assert (
        normal_calculate_instance._get_last_position_average_price_for_month(
            average_price_by_ticker, year_month, ticker
        )
        is None
    )

    normal_calculate_instance.append_inconsistency.assert_called_once_with(message)


def test_calcule_average_purchase_price_certain_day_with_only_sales(
    normal_calculate_instance, financial_normal_operations
):
    financial_normal_operations = [
        operation
        for operation in financial_normal_operations
        if operation.ticker == "XPLG11" and operation.operation_type == "sale"
    ]

    test_cases = [
        (date(2020, 11, 13), {"position": -1, "average_purchase_price": None, "operation_type": "sale"}),
        (date(2020, 11, 17), {"position": -4, "average_purchase_price": None, "operation_type": "sale"}),
    ]

    average_price_ticket = {
        "XPLG11": {
            date(2020, 11, 13): {"position": 0, "operation_type": None},
            date(2020, 11, 17): {"position": 0, "operation_type": None},
        }
    }

    for day, expected_average_price_ticket in test_cases:
        output = normal_calculate_instance._calcule_average_purchase_price_certain_day(
            day, financial_normal_operations, average_price_ticket
        )
        assert output["XPLG11"][day] == expected_average_price_ticket
        average_price_ticket = output


def test_calcule_average_purchase_price_certain_day_with_purchases_and_sales(
    normal_calculate_instance, financial_normal_operations
):
    financial_normal_operations = [
        operation for operation in financial_normal_operations if operation.ticker == "XPLG11"
    ]
    test_cases = [
        (date(2020, 10, 6), {"position": 1, "average_purchase_price": 127.88, "operation_type": "purchase"}),
        (date(2020, 10, 11), {"position": 2, "average_purchase_price": 128.88, "operation_type": "purchase"}),
        (
            date(2020, 10, 12),
            {"position": 5, "average_purchase_price": 128.248, "operation_type": "purchase"},
        ),
        (date(2020, 11, 13), {"position": 4, "average_purchase_price": 128.248, "operation_type": "sale"}),
        (date(2020, 11, 17), {"position": 1, "average_purchase_price": 128.248, "operation_type": "sale"}),
    ]

    average_price_ticket = {
        "XPLG11": {
            date(2020, 10, 6): {"position": 0, "operation_type": None},
            date(2020, 10, 11): {"position": 0, "operation_type": None},
            date(2020, 10, 12): {"position": 0, "operation_type": None},
            date(2020, 11, 13): {"position": 0, "operation_type": None},
            date(2020, 11, 17): {"position": 0, "operation_type": None},
        }
    }

    for day, expected_average_price_ticket in test_cases:
        output = normal_calculate_instance._calcule_average_purchase_price_certain_day(
            day, financial_normal_operations, average_price_ticket
        )
        assert output["XPLG11"][day] == expected_average_price_ticket
        average_price_ticket = output


@mock.patch(
    "calculation_engine.operation_classes.NormalCalculate._calcule_average_purchase_price_certain_day"
)
def test_calcule_average_purchase_price_for_each_sale(
    mock_average_purchase_price_certain_day, normal_calculate_instance, financial_normal_operations
):
    to_side_effect = [
        {
            "XPLG11": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {"position": 0, "operation_type": None},
                date(2020, 10, 12): {"position": 0, "operation_type": None},
                date(2020, 11, 13): {"position": 0, "operation_type": None},
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            }
        },
        {
            "XPLG11": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {"position": 0, "operation_type": None},
                date(2020, 11, 13): {"position": 0, "operation_type": None},
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            }
        },
        {
            "XPLG11": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {
                    "position": 5.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 13): {"position": 0, "operation_type": None},
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            }
        },
        {
            "XPLG11": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {
                    "position": 5.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 13): {
                    "position": 4.0,
                    "operation_type": "sale",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            }
        },
        {
            "XPLG11": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {
                    "position": 5.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 13): {
                    "position": 4.0,
                    "operation_type": "sale",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 17): {
                    "position": 1.0,
                    "operation_type": "sale",
                    "average_purchase_price": 128.248,
                },
            }
        },
        {
            "XPLG11": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {
                    "position": 5.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 13): {
                    "position": 4.0,
                    "operation_type": "sale",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            },
            "KGBRUSSIA": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {"position": 0, "operation_type": None},
                date(2020, 10, 12): {"position": 0, "operation_type": None},
                date(2020, 11, 13): {"position": 0, "operation_type": None},
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            },
        },
        {
            "XPLG11": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {
                    "position": 5.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 13): {
                    "position": 4.0,
                    "operation_type": "sale",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            },
            "KGBRUSSIA": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {"position": 0, "operation_type": None},
                date(2020, 11, 13): {"position": 0, "operation_type": None},
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            },
        },
        {
            "XPLG11": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {
                    "position": 5.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 13): {
                    "position": 4.0,
                    "operation_type": "sale",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            },
            "KGBRUSSIA": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {
                    "position": 5.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 13): {"position": 0, "operation_type": None},
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            },
        },
        {
            "XPLG11": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {
                    "position": 5.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 13): {
                    "position": 4.0,
                    "operation_type": "sale",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            },
            "KGBRUSSIA": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {
                    "position": 5.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 13): {
                    "position": 4.0,
                    "operation_type": "sale",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            },
        },
        {
            "XPLG11": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {
                    "position": 5.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 13): {
                    "position": 4.0,
                    "operation_type": "sale",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 17): {"position": 0, "operation_type": None},
            },
            "KGBRUSSIA": {
                date(2020, 10, 6): {
                    "position": 1.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 127.88,
                },
                date(2020, 10, 11): {
                    "position": 2.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.88,
                },
                date(2020, 10, 12): {
                    "position": 5.0,
                    "operation_type": "purchase",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 13): {
                    "position": 4.0,
                    "operation_type": "sale",
                    "average_purchase_price": 128.248,
                },
                date(2020, 11, 19): {
                    "position": 1.0,
                    "operation_type": "sale",
                    "average_purchase_price": 128.248,
                },
            },
        },
    ]

    mock_average_purchase_price_certain_day.side_effect = to_side_effect

    assert normal_calculate_instance._calcule_average_purchase_price_for_each_sale(
        financial_normal_operations
    ) == {**to_side_effect[4], **to_side_effect[9]}

    assert mock_average_purchase_price_certain_day.call_count == 10


@mock.patch("calculation_engine.operation_classes.NormalCalculate._get_last_position_average_price_for_month")
def test_calcule_normal_operation_monthly_params_negative_position(
    mock_last_position_average_price_for_month, normal_calculate_instance, financial_normal_operations
):
    mock_last_position_average_price_for_month.return_value = None
    average_price_by_ticker = {
        date(2020, 5, 3): {
            "position": 3,
            "average_purchase_price": 100,
            "operation_type": "purchase",
            "total_amount_with_operation_costs": 300,
        },
        date(2020, 5, 29): {
            "position": -2,
            "average_purchase_price": 100,
            "operation_type": "sale",
            "total_amount_with_operation_costs": 200,
        },
    }
    year_month, ticker = "05/2020", "MAFIARUSSA"
    assert (
        normal_calculate_instance._calcule_normal_operation_monthly_params(
            financial_normal_operations, average_price_by_ticker, year_month, ticker
        )
        is None
    )

    mock_last_position_average_price_for_month.assert_called_with(average_price_by_ticker, year_month, ticker)


@mock.patch("calculation_engine.operation_classes.NormalCalculate._get_last_position_average_price_for_month")
def test_calcule_normal_operation_monthly_params(
    mock_last_position_average_price_for_month, normal_calculate_instance, financial_normal_operations
):

    mock_last_position_average_price_for_month.return_value = {
        "position": 5,
        "average_purchase_price": 129.51,
    }
    year_month, ticker, average_price_by_ticker = "10/2020", "XPLG11", {"mock": "mock"}

    expected_monthly_params = {
        "total_amount_purchase": 641.24,
        "total_amount_sale": 0,
        "total_units_purchase": 5,
        "total_units_sale": 0,
        "cgs": 0,
        "irrf": 0.04,
        "position": 5,
        "average_purchase_price": 129.51,
        "result": 0
    }

    assert (
        normal_calculate_instance._calcule_normal_operation_monthly_params(
            financial_normal_operations, average_price_by_ticker, year_month, ticker
        )
        == expected_monthly_params
    )

    mock_last_position_average_price_for_month.assert_called_with(average_price_by_ticker, year_month, ticker)
