from companies_union.clusterization.jacard_distance_clusterization import JacardDistanceClusterization, FullName


def test_get_full_name_pairs():
    dict_to_pass = {"a_file": [("kek_a, llc", "kek_a"), ("lol_a, llc", "lol_a")],
                    "b_file": [("kek_b, llc", "kek_b"), ("lol_b, llc", "lol_b")]}
    file_names = ["a_file", "b_file"]
    clusterizator = JacardDistanceClusterization(dict_to_pass, file_names)
    actual_result = clusterizator._get_full_name_pairs()
    expected_result = [
        (
            ("a_file", "kek_a, llc", "kek_a"),
            ("b_file", "kek_b, llc", "kek_b")
        ),
        (
            ("a_file", "kek_a, llc", "kek_a"),
            ("b_file", "lol_b, llc", "lol_b")
        ),
        (
            ("a_file", "lol_a, llc", "lol_a"),
            ("b_file", "kek_b, llc", "kek_b")
        ),
        (
            ("a_file", "lol_a, llc", "lol_a"),
            ("b_file", "lol_b, llc", "lol_b")
        )
    ]
    assert actual_result == expected_result


class TestFullName:

    def test_equals_FullName(self):
        first = ["das", "a b", "a"]
        second = ["das", "a b", "c"]
        assert FullName(*first) == FullName(*second)

    def test_tokens(self):
        first = ["das", "a b", "a z"]
        assert FullName(*first).tokens == {"a", "z"}

    def test_jacard_distances(self):
        first = ["das", "a e", "a"]
        second = ["das", "a b c d e", "a b c d"]
        assert FullName(*first).jacard_distance(FullName(*second)) == 0.75
