from DataFramePreprocessor import DataFramePreprocessor

import pandas as pd


class TestDataFramePreprocessor:

    def test_preprocess_columns(self):
        data_frame = pd.DataFrame(data={"A\t \n": ["a", "a"], "\n\t\r\nB\n": ["b", "b"]})
        DataFramePreprocessor._standartize_columns_names(data_frame)
        assert data_frame.columns.equals(pd.Index(["a", "b"]))

    def test_get_grouper_data_frame(self):
        name = "example.xlsx"
        data_frame = pd.DataFrame(
            data={"A": ["  kek, \n LLC\n\t\r  ", "lol singapore, llc"], "\n\t\r\nB\n": ["b", "b"]}
        )
        data_frame_expected = pd.DataFrame(
            data={
                "file_name": [name] * 2,
                "a": ["  kek, \n LLC\n\t\r  ", "lol singapore, llc"],
                "a_standartized": ["kek, llc", "lol singapore, llc"],
                "a_cleaned": ["kek", "lol singapore"],
                "group_id": [0, 0]
            }
        )
        processer = DataFramePreprocessor("A")
        data_frame_actual = processer.get_grouper_dataframe(data_frame, name)
        assert data_frame_actual.equals(data_frame_expected)

    def test_get_grouper_data_frame_from_lists(self):
        names = ["first",
                 "second"]
        data_frame_list = [
            pd.DataFrame(
                data={"A": ["  ROSNeft, \n LLC\n\t\r  ", "BP, llc"], "\n\t\r\nB\n": ["b", "b"]}
            ),
            pd.DataFrame(
                data={"A": ["  kek, \n LLC\n\t\r  ", "lol singapore, llc"], "\n\t\r\nB\n": ["b", "b"]}
            )
        ]
        data_frame_expected = pd.DataFrame(
            data={
                "file_name": [names[0]] * 2 + [names[1]] * 2,
                "a": ["  ROSNeft, \n LLC\n\t\r  ", "BP, llc", "  kek, \n LLC\n\t\r  ", "lol singapore, llc"],
                "a_standartized": ["rosneft, llc", "bp, llc", "kek, llc", "lol singapore, llc"],
                "a_cleaned": ["rosneft", "bp", "kek", "lol singapore"],
                "group_id": [0] * 4
            }
        )

        processer = DataFramePreprocessor("A")
        data_frame_actual = processer.get_grouper_dataframe_from_lists(data_frame_list, names)
        assert data_frame_actual.equals(data_frame_expected)
