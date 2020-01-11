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
    print("\n")
    print(expected)
    print("\n")
    print(actual)
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
