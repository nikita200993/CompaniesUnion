from companies_union.clusterization.jacard_distance_clusterization import JacardDistanceClusterization


def test_get_full_name_pairs():
    dict_to_pass = {"a_file": [("kek_a, llc", "kek_a"), ("lol_a, llc", "lol_a")],
                    "b_file": [("kek_b, llc", "kek_b"), ("lol_b, llc", "lol_b")]}
    file_names = ["a_file", "b_file"]
    clusterizator = JacardDistanceClusterization(dict_to_pass, file_names)
    actual_result = clusterizator._get_full_name_pairs()
    expected_result = [
        (
            ("kek_a, llc", ["kek_a"]),
            ("kek_b, llc", ["kek_b"])
        ),
        (
            ("kek_a, llc", ["kek_a"]),
            ("lol_b, llc", ["lol_b"])
        ),
        (
            ("lol_a, llc", ["lol_a"]),
            ("kek_b, llc", ["kek_b"])
        ),
        (
            ("lol_a, llc", ["lol_a"]),
            ("lol_b, llc", ["lol_b"])
        )
    ]
    assert actual_result == expected_result
