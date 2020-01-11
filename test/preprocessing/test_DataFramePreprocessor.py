from companies_union.preprocessing.DataFramePreprocessor import DataFramePreprocessor
from companies_union.company_name import CompanyNameWithFileName

import pandas as pd


class TestDataFramePreprocessor:

    def test_preprocess_columns(self):
        data_frame = pd.DataFrame(data={"A\t \n": ["a", "a"], "\n\t\r\nB\n": ["b", "b"]})
        DataFramePreprocessor._standartize_columns_names(data_frame)
        assert data_frame.columns.equals(pd.Index(["a", "b"]))

    def test_get_grouper_data_frame(self):
        file_name = "example.xlsx"
        data_frame = pd.DataFrame(
            data={"A": ["  kek, \n LLC\n\t\r  ", "lol singapore, llc"], "\n\t\r\nB\n": ["b", "b"]}
        )
        list_expected = [
            CompanyNameWithFileName(file_name, "kek, llc"),
            CompanyNameWithFileName(file_name, "lol singapore, llc")
        ]
        processer = DataFramePreprocessor("A")
        list_actual = processer.get_company_names_from_dataframe(data_frame, file_name)
        assert list_expected == list_actual
