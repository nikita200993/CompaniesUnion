from utils import Utils

import pandas as pd

from cleanco import cleanco
from contracts import contract


class DataFramePreprocessor:

    @contract(key_name=str)
    def __init__(self, key_name: str):
        self.__original_key_name = key_name
        self.key_name = Utils.replace_redundant_ws(key_name).lower()

    @staticmethod
    @contract(dataframe=pd.DataFrame)
    def standartize_columns_names(dataframe: pd.DataFrame):
        dataframe.columns = pd.Index(
            data=[Utils.replace_redundant_ws(column_name).lower()
                  for column_name in dataframe.columns]
        )

    @contract(dataframe=pd.DataFrame)
    def _check_key_existence(self, dataframe: pd.DataFrame):
        if not dataframe.columns.contains(self.key_name):
            raise AssertionError(f"There is no column with key = {self.__original_key_name}")

    @contract(dataframe=pd.DataFrame)
    def _standartize_column_with_names(self, dataframe: pd.DataFrame):
        dataframe[self.key_name] = dataframe[self.key_name].map(Utils.replace_redundant_ws).map(str.lower)

    @contract(dataframe=pd.DataFrame)
    def _add_cleaned_names_column(self, dataframe: pd.DataFrame):
        index = 0
        found = False
        for col_name in dataframe.columns:
            if col_name == self.key_name:
                found = True
                break
            index += 1
        if not found:
            raise AssertionError(f"There is no column with key = {self.__original_key_name}")
        dataframe.insert(
            index + 1,
            self.key_name + "_cleaned",
            dataframe[self.key_name].map(lambda string: cleanco(string).clean_name())
        )

