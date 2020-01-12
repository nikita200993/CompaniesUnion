from companies_union.companymapper import CompanyMapper
from companies_union.company_name import CompanyNameWithFileName

from pandas import DataFrame


def test_mapper_to_df():
    mapper = {
        CompanyNameWithFileName("a", "b"): 1,
        CompanyNameWithFileName("c", "z"): 0,
        CompanyNameWithFileName("c", "b"): 1,
        CompanyNameWithFileName("c", "ze"): 2
    }
    actual = CompanyMapper.create_dataframe_from_mapper(mapper)
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
    actual = CompanyMapper.create_mapper_from_dataframe(df)
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
    print("\n", actual)
    for group in actual.keys():
        actual[group] = set(actual[group])
    assert actual == expected

