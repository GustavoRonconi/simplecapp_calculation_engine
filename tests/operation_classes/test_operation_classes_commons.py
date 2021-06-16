import pytest
from datetime import date
from unittest import mock

from calculation_engine.operation_classes import OperationClassesCommons


@pytest.fixture
def operation_classes_commons_instance():
    return OperationClassesCommons()


@pytest.fixture
def operations(finantial_normal_operation, finantial_day_trade_operation):
    finantial_day_trade_operation.date = date(2020, 11, 26)
    return [finantial_normal_operation, finantial_day_trade_operation]


@mock.patch(
    "calculation_engine.operation_classes.operation_classes_commons.SimpleCappUtils.get_list_with_filters",
)
def test_agroup_operations_by_ticker_type(
    mock_get_list_with_filters, operation_classes_commons_instance, operations
):
    mock_get_list_with_filters.side_effect = [[operations[0]], [operations[1]], []]

    expected_agrouped_operations_by_ticker_type = {
        "fiis": [operations[0]],
        "stock": [operations[1]],
        "bdr": [],
    }

    assert (
        operation_classes_commons_instance.agroup_operations_by_ticker_type(operations)
        == expected_agrouped_operations_by_ticker_type
    )


def test_compile_year_months_reference_year(operation_classes_commons_instance):
    reference_year = 2019

    assert operation_classes_commons_instance.compile_year_months_reference_year(reference_year) == [
        "01/2019",
        "02/2019",
        "03/2019",
        "04/2019",
        "05/2019",
        "06/2019",
        "07/2019",
        "08/2019",
        "09/2019",
        "10/2019",
        "11/2019",
        "12/2019",
    ]
