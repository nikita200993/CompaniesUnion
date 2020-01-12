from companies_union.preprocessing.utils import Utils
from companies_union.company_name import CompanyNameWithFileName

import pandas as pd
from contracts import contract
from typing import Iterable


class DataFramePreprocessor:

    @contract(key_name=str)
    def __init__(self, key_name: str):
        self.__original_key_name = key_name
        self.__key_name = Utils.replace_redundant_ws(key_name).lower()

    def get_company_names_from_dataframe(self, dataframe: pd.DataFrame, file_name: str):
        dataframe_copy = dataframe.copy(deep=True)
        self._standartize_columns_names(dataframe_copy)
        self._check_key_existence(dataframe_copy)
        self._check_names_nonempty(dataframe_copy)
        return list(
            map(
                lambda name: CompanyNameWithFileName(file_name, name),
                map(
                    Utils.normalize_string,
                    dataframe_copy[self.__key_name]
                )
            )
        )

    def get_company_names_from_dataframes(self, dataframe_list: Iterable[pd.DataFrame], file_name_list: Iterable[str]):
        result = []
        for df, file_name in zip(dataframe_list, file_name_list):
            result.extend(self.get_company_names_from_dataframe(df, file_name))
        return result

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
        if any(dataframe[self.__key_name].isna()):
            raise AssertionError("There is nan value in column with names")
        if any(dataframe[self.__key_name].map(lambda string: string == "")):
            raise AssertionError("There is empty string in column with names")
