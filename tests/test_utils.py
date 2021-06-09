import pytest
from unittest import mock

from calculation_engine.utils import SimpleCappUtils, UnpackError


@pytest.fixture
def list_dict_bands():
    return [
        {"name": "rise against", "genre": "punk", "vocalist": "tim", "country": "eua"},
        {"name": "bob marley", "genre": "reggae", "vocalist": "bob", "country": "jamaica",},
        {"name": "bad religion", "genre": "punk", "vocalist": "greg", "country": "eua"},
        {"name": "soja", "genre": "reggae", "vocalist": "jacob", "country": "eua"},
    ]


@pytest.fixture
def list_object_bands(list_dict_bands):
    class Band:
        def __init__(self, name, genre, vocalist, country) -> None:
            self.name = name
            self.genre = genre
            self.vocalist = vocalist
            self.country = country

    return [Band(**band) for band in list_dict_bands]


def test_get_list_with_filters_from_dict_list_no_empty(list_dict_bands):
    filter_dict = {"genre": "reggae", "name": "bob marley"}
    expected_list = [list_dict_bands[1]]

    assert SimpleCappUtils.get_list_with_filters(filter_dict, list_dict_bands) == expected_list


def test_get_list_with_filters_from_object_list_no_empty(list_object_bands):
    filter_dict = {"genre": "reggae"}
    expected_list = [list_object_bands[1], list_object_bands[3]]

    assert SimpleCappUtils.get_list_with_filters(filter_dict, list_object_bands) == expected_list


def test_get_list_with_filters_empty():
    filter_dict = {"genre": "reggae"}
    assert SimpleCappUtils.get_list_with_filters(filter_dict, []) == []


@mock.patch("calculation_engine.utils.SimpleCappUtils.get_list_with_filters",)
def test_index_list_by_list_of_keys(mock_get_list_with_filters, list_dict_bands):
    mock_get_list_with_filters.side_effect = [
        [list_dict_bands[0], list_dict_bands[2]],
        [list_dict_bands[1], list_dict_bands[3]],
    ]
    expected_indexed_list_by_list_of_keys = {
        "punk": [list_dict_bands[0], list_dict_bands[2]],
        "reggae": [list_dict_bands[1], list_dict_bands[3]],
    }
    assert (
        SimpleCappUtils.index_list_by_list_of_keys(
            list_dict_bands, expected_indexed_list_by_list_of_keys.keys(), "genre"
        )
        == expected_indexed_list_by_list_of_keys
    )

    mock_get_list_with_filters.assert_has_calls(
        [mock.call({"genre": "punk"}, list_dict_bands), mock.call({"genre": "reggae"}, list_dict_bands),]
    )


def test_get_unique_values(list_dict_bands):
    expected_list = ["punk", "reggae"]

    assert SimpleCappUtils.get_unique_values(list_dict_bands, "genre") == expected_list


@pytest.mark.parametrize(
    "level_unpack,expected_list",
    [
        (
            2,
            [
                {"name": "bob marley", "genre": "reggae", "vocalist": "bob", "country": "jamaica",},
                {"name": "soja", "genre": "reggae", "vocalist": "jacob", "country": "eua",},
            ],
        ),
        (3, UnpackError("The level is so much high to unpack")),
    ],
)
def test_unpack_dict_in_list_of_rows(level_unpack, expected_list):
    dict_to_unpack = {
        "raggae": {
            "jamaica": {"name": "bob marley", "genre": "reggae", "vocalist": "bob", "country": "jamaica",},
            "eua": {"name": "soja", "genre": "reggae", "vocalist": "jacob", "country": "eua",},
        }
    }
    if type(expected_list) is not list:
        with pytest.raises(UnpackError):
            SimpleCappUtils.unpack_dict_in_list_of_rows(level_unpack, dict_to_unpack)
        return

    assert SimpleCappUtils.unpack_dict_in_list_of_rows(level_unpack, dict_to_unpack) == expected_list
