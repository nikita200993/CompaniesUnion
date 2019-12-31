from DataFramePreprocessor import DataFramePreprocessor

import pandas as pd


class TestDataFramePreprocessor:

    def test_preprocess_columns(self):
        data_frame = pd.DataFrame(data={"A\t \n": ["a", "a"], "\n\t\r\nB\n": ["b", "b"]})
        DataFramePreprocessor.standartize_columns_names(data_frame)
        assert data_frame.columns.equals(pd.Index(["a", "b"]))

    def test_preprocess_key_column(self):
        data_frame = pd.DataFrame(data={"a": ["A\t\n  ", "\t\n\r\nA"], "b": ["b", "b"]})
        DataFramePreprocessor("a")._standartize_column_with_names(data_frame)
        data_frame_expected = pd.DataFrame(data={"a": ["a", "a"], "b": ["b", "b"]})
        assert data_frame.equals(data_frame_expected)

    def test_add_cleaned_column(self):
        data_frame = pd.DataFrame(data={"a": ["Aza, LLC\t\n  ", "\t\n\r\nAba Singapore, LLC"], "b": ["b", "b"]})
        dataframe_preprocessor = DataFramePreprocessor("a")
        dataframe_preprocessor._standartize_column_with_names(data_frame)
        dataframe_preprocessor._add_cleaned_names_column(data_frame)
        data_frame_expected = pd.DataFrame(data={"a": ["aza", "aba singapore"], "b": ["b", "b"]})
        assert data_frame.equals(data_frame)
