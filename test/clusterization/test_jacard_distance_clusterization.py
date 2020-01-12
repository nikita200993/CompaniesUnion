from companies_union.clusterization.jacard_distance_clusterization import JacardDistanceClusterization
from companies_union.company_name import CompanyNameWithFileName

import pytest


names_1 = [
    CompanyNameWithFileName("a", "comp_a_0, llc"),
    CompanyNameWithFileName("b", "comp_b_0, llc"),
    CompanyNameWithFileName("a", "comp_a_1, llc"),
    CompanyNameWithFileName("b", "comp_b_1, llc"),
    CompanyNameWithFileName("c", "comp_c_0, llc"),
]

expected_groups_1 = [0, 2, 1, 3, 4]

names_2 = [
    CompanyNameWithFileName("a", "a b c d"),
    CompanyNameWithFileName("b", "a"),
    CompanyNameWithFileName("a", "a b c e f, llc"),
    CompanyNameWithFileName("b", "a b c e, llc"),
    CompanyNameWithFileName("c", "a b c d, llc"),
]

expected_groups_2 = [0, 2, 1, 1, 0]

names_3 = [
    CompanyNameWithFileName("a", "a b c d"),
    CompanyNameWithFileName("b", "a b d"),
    CompanyNameWithFileName("b", "a b c"),
    CompanyNameWithFileName("a", "a b c e f, llc"),
    CompanyNameWithFileName("b", "a b c e, llc"),
    CompanyNameWithFileName("c", "a b c d, llc"),
]

expected_groups_3 = [0, 0, 2, 1, 1, 0]


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

@pytest.mark.parametrize(
    "test_input,expected",
    [(names_1, expected_groups_1), (names_2, expected_groups_2), (names_3, expected_groups_3)]
)
def test_clusterization(test_input, expected):
    clusterizator = JacardDistanceClusterization(test_input)
    clusterizator.clusterize()
    name_to_group = clusterizator.get_name_to_group()
    actual = []
    for name in test_input:
        actual.append(name_to_group[name])
    assert expected == actual
