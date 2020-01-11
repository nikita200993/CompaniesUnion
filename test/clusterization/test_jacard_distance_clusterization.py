from companies_union.clusterization.jacard_distance_clusterization import JacardDistanceClusterization
from companies_union.company_name import CompanyNameWithFileName

names_1 = [
    CompanyNameWithFileName("a", "comp_a_0, llc"),
    CompanyNameWithFileName("b", "comp_b_0, llc"),
    CompanyNameWithFileName("a", "comp_a_1, llc"),
    CompanyNameWithFileName("b", "comp_b_1, llc"),
    CompanyNameWithFileName("c", "comp_c_0, llc"),
]

names_2 = [
    CompanyNameWithFileName("a", "a b c d"),
    CompanyNameWithFileName("b", "a"),
    CompanyNameWithFileName("a", "a b c e f, llc"),
    CompanyNameWithFileName("b", "a b c e, llc"),
    CompanyNameWithFileName("c", "a b c d, llc"),
]


def test_get_dict():
    clusterizator = JacardDistanceClusterization(names_1)
    actual = clusterizator.get_dict_file_name_to_company_names()
    expected = {
        "a": {
            CompanyNameWithFileName("a", "comp_a_0, llc"),
            CompanyNameWithFileName("a", "comp_a_1, llc")
        },
        "b": {
            CompanyNameWithFileName("b", "comp_b_0, llc"),
            CompanyNameWithFileName("b", "comp_b_1, llc")
        },
        "c": {CompanyNameWithFileName("c", "comp_c_0, llc")}
    }
    for key in actual.keys():
        assert set(actual[key]) == expected[key]


def test_get_dict_to_others():
    clusterizator = JacardDistanceClusterization(names_1)
    expected = {
        "a": {
            CompanyNameWithFileName("b", "comp_b_0, llc"),
            CompanyNameWithFileName("b", "comp_b_1, llc"),
            CompanyNameWithFileName("c", "comp_c_0, llc")
        },
        "b": {
            CompanyNameWithFileName("c", "comp_c_0, llc")
        },
        "c": set()
    }
    actual = clusterizator.get_dict_file_name_to_other_company_names()
    for key in actual.keys():
        assert set(actual[key]) == expected[key]


def test_clusterization_1():
    clusterizator = JacardDistanceClusterization(names_1)
    clusterizator.clusterize()
    name_to_group = clusterizator.get_name_to_group()
    actual = []
    for name in names_1:
        actual.append(name_to_group[name])
    expected = [0, 2, 1, 3, 4]
    assert expected == actual


def test_clusterization_2():
    clusterizator = JacardDistanceClusterization(names_2)
    clusterizator.clusterize()
    name_to_group = clusterizator.get_name_to_group()
    actual = []
    for name in names_2:
        actual.append(name_to_group[name])
    expected = [0, 2, 1, 1, 0]
    assert expected == actual
