from companies_union.preprocessing.DataFramePreprocessor import DataFramePreprocessor
from companies_union.clusterization.jacard_distance_clusterization import JacardDistanceClusterization
from companies_union.preprocessing.utils import Utils
from companies_union.companymapper import CompanyMapper
from companies_union.union import get_union_from_dataframes
from pandas import DataFrame, Index

file_name_1 = "b"
df_1 = DataFrame(
    data=[
        ["Bp \nsingapore, llc", "kaka"],
        ["lel buk, llc", "keka"],
        ["azaza, london, llc", "hey"]
    ],
    columns=[
        "company_Name\n",
        "greetinG"
    ]
)

file_name_2 = "c"
df_2 = DataFrame(
    data=[
        ["Bp \nsingapoRE, llc", 1],
        ["azazA,\n  london, llc", 3],
        ["lel bukas, llc", 2],
        ["a b c d e, llc", 4]
    ],
    columns=[
        "company_NamE",
        "eyes"
    ]
)

file_name_3 = "a"
df_3 = DataFrame(
    data=[
        ["a c b d,                llc", "wafancula"],
        ["GADAS \nsingapoRE, llc", "kekazzi"],
        ["hop hey, llc", "geg"],
        ["Shikarno,\n  london, llc", "abc"]
    ],
    columns=[
        "  company_NamE",
        "bred"
    ]
)


def test_synthetic():
    file_names_list = [
        file_name_1,
        file_name_2,
        file_name_3
    ]
    df_list = [
        df_1,
        df_2,
        df_3
    ]

    processor = DataFramePreprocessor("company_name")
    names_list = processor.get_company_names_from_dataframes(df_list, file_names_list)
    clusterizator = JacardDistanceClusterization(names_list)
    clusterizator.clusterize()
    file_name_to_series = {}
    for file_name, df in zip(file_names_list, df_list):
        df.columns = Index(df.columns.map(Utils.normalize_string))
        file_name_to_series[file_name] = df["company_name"].map(Utils.normalize_string)
    mapper = CompanyMapper(clusterizator.get_name_to_group())
    actual = mapper.get_indexes_of_common_companies(file_name_to_series)
    expected = [
        [0, None, 3],
        [None, 0, 0],
        [None, 2, 1]
    ]
    assert actual == expected


def test_synthetic_2():
    file_names_list = [
        file_name_3,
        file_name_1,
        file_name_2
    ]
    df_list = [
        df_3,
        df_1,
        df_2
    ]
    result = get_union_from_dataframes(df_list, file_names_list, "company_name")
    print("\n", result)