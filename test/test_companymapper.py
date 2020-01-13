from companies_union.companymapper import CompanyMapper
from companies_union.company_name import CompanyNameWithFileName

import pytest
from pandas import DataFrame, Series


def test_mapper_to_df():
    name_to_group = {
        CompanyNameWithFileName("a", "b"): 1,
        CompanyNameWithFileName("c", "z"): 0,
        CompanyNameWithFileName("c", "b"): 1,
        CompanyNameWithFileName("c", "ze"): 2
    }
    actual = CompanyMapper.create_dataframe_from_mapper(CompanyMapper(name_to_group))
    rows = [
        ["a", "b", 1],
        ["c", "b", 1],
        ["c", "z", 0],
        ["c", "ze", 2]
    ]
    expected = DataFrame(
        data=rows,
        columns=CompanyMapper.COLUMN_NAMES
    )
    assert actual.equals(expected)


def test_df_to_mapper():
    rows = [
        ["dasd", "a", "B  ", 1],
        ["dasd", "c", "B \n", 1],
        ["dasd", "c", "z  ", 0],
        ["dasd", "c", "  ze", 2]
    ]
    columns = ["dasd", "file_name", "Company_name\t", "group_Id"]
    df = DataFrame(
        data=rows,
        columns=columns
    )
    actual = CompanyMapper.create_mapper_from_dataframe(df).name_to_group
    expected = {
        CompanyNameWithFileName("a", "b"): 1,
        CompanyNameWithFileName("c", "b"): 1,
        CompanyNameWithFileName("c", "z"): 0,
        CompanyNameWithFileName("c", "ze"): 2
    }
    assert actual == expected


def test_get_group_to_names():
    name_to_group = {
        CompanyNameWithFileName("a", "b"): 1,
        CompanyNameWithFileName("c", "b"): 1,
        CompanyNameWithFileName("c", "z"): 0,
        CompanyNameWithFileName("c", "ze"): 2
    }
    expected = {
        0: {CompanyNameWithFileName("c", "z")},
        1: {CompanyNameWithFileName("a", "b"), CompanyNameWithFileName("c", "b")},
        2: {CompanyNameWithFileName("c", "ze")}
    }
    actual = CompanyMapper.get_group_to_names(name_to_group)
    for group in actual.keys():
        actual[group] = set(actual[group])
    assert actual == expected


name_to_group = {
    CompanyNameWithFileName("a", "b"): 1,
    CompanyNameWithFileName("c", "b"): 1,
    CompanyNameWithFileName("c", "z"): 0,
    CompanyNameWithFileName("c", "ze"): 2,
    CompanyNameWithFileName("d", "ze zE"): 3,
    CompanyNameWithFileName("d", "b"): 1
}


@pytest.mark.parametrize(
    "file_name,series,expected",
    [
        ("a", Series(("b",)), []),
        ("c", Series(("ze", "b", "z")), [0, 2]),
        ("d", Series(("b", "ze ze")), [1])
    ]
)
def test_get_indexes_of_unique_companies(file_name, series, expected):
    mapper = CompanyMapper(name_to_group)
    actual = mapper.get_indexes_of_unique_companies(series, file_name)
    assert actual == expected


def test_get_indexes_of_common_companies():
    name_to_group = {
        CompanyNameWithFileName("a", "b"): 1,
        CompanyNameWithFileName("c", "b"): 1,
        CompanyNameWithFileName("c", "z"): 0,
        CompanyNameWithFileName("c", "ze"): 2,
        CompanyNameWithFileName("d", "ze zE"): 3,
        CompanyNameWithFileName("d", "b"): 1,
        CompanyNameWithFileName("d", "z"): 0
    }
    mapper = CompanyMapper(name_to_group)
    file_names_to_series = {
        "d": Series(("ze ze", "z", "b")),
        "a": Series(("b",)),
        "c": Series(("ze", "b", "z"))
    }
    actual = mapper.get_indexes_of_common_companies(file_names_to_series)
    expected = [
        [None, 2, 1],
        [0, 1, 2]
    ]
    assert actual == expected
