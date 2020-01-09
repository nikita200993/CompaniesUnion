from preprocessing.utils import Utils

import pandas as pd
import numpy as np

from cleanco import cleanco
from contracts import contract


class DataFramePreprocessor:

    @contract(key_name=str)
    def __init__(self, key_name: str):
        self.__original_key_name = key_name
        self.__key_name = Utils.replace_redundant_ws(key_name).lower()

    def get_grouper_dataframe(self, dataframe: pd.DataFrame, name: str):
        dataframe_copy = dataframe.copy(deep=True)
        self._standartize_columns_names(dataframe_copy)
        self._check_key_existence(dataframe_copy)
        self._check_names_nonempty(dataframe_copy)
        dataframe_copy = dataframe_copy[[self.__key_name]]
        dataframe_copy.insert(
            1,
            self.__key_name + "_standartized",
            dataframe_copy[self.__key_name].map(Utils.replace_redundant_ws).map(str.lower)
        )
        dataframe_copy.insert(
            2,
            self.__key_name + "_cleaned",
            dataframe_copy[self.__key_name + "_standartized"].map(lambda string: cleanco(string).clean_name())
        )
        dataframe_copy.insert(
            0,
            "file_name",
            [name] * dataframe_copy.shape[0]
        )
        dataframe_copy.insert(
            4,
            "group_id",
            [0]*dataframe_copy.shape[0]
        )
        return dataframe_copy

    def get_grouper_dataframe_from_lists(self, dataframe_list, names_list):
        if len(dataframe_list) != len(names_list):
            raise AssertionError("Names list size is not equal dataframe list size")
        transformed_dataframe_list = [self.get_grouper_dataframe(df, name)
                                      for df, name in zip(dataframe_list, names_list)
                                      ]
        return pd.concat(transformed_dataframe_list, ignore_index=True)

    @staticmethod
    @contract(dataframe=pd.DataFrame)
    def _standartize_columns_names(dataframe: pd.DataFrame):
        dataframe.columns = pd.Index(
            data=[Utils.replace_redundant_ws(column_name).lower()
                  for column_name in dataframe.columns]
        )

    @contract(dataframe=pd.DataFrame)
    def _check_key_existence(self, dataframe: pd.DataFrame):
        if not dataframe.columns.contains(self.__key_name):
            raise AssertionError(f"There is no column with key = {self.__original_key_name}")

    @contract(dataframe=pd.DataFrame)
    def _check_names_nonempty(self, dataframe: pd.DataFrame):
        if any(dataframe[self.__key_name].isna):
            raise AssertionError("There is nan value in column with names")
        if any(dataframe[self.__key_name].map(lambda string: string == "")):
            raise AssertionError("There is empty string in column with names")
