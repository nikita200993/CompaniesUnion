from companies_union.company_name import CompanyNameWithFileName
from companies_union.preprocessing.utils import Utils

import os.path as path_utils
import numpy
from pandas import DataFrame, Series, read_excel, Index
from typing import Dict, Tuple, List, Sized, Iterable, Union


class CompanyMapper:

    COLUMN_NAMES = ["file_name", "company_name", "group_id"]

    def __init__(self, name_to_group: Dict[CompanyNameWithFileName, int]):
        self.__name_to_group = name_to_group.copy()
        self.__group_to_names = CompanyMapper.get_group_to_names(self.__name_to_group)
        self.__file_names = tuple(
            sorted(
                frozenset(
                    map(
                        lambda name: name.file_name,
                        self.__name_to_group.keys()
                    )
                )
            )
        )

    @property
    def name_to_group(self):
        return self.__name_to_group

    def get_indexes_of_unique_companies(self, series: Series, file_name: str):
        array_with_names = series.to_numpy()
        # print("array with names:", array_with_names, "\n")
        result = []
        for name in self.__get_unique_names(file_name):
            # print(name, "\n")
            result.append(
                self.__get_index_of_row(name, series)
            )
        result.sort()
        return result

    def get_indexes_of_common_companies(self, file_name_to_series: Dict[str, Series]):
        self.__check_file_names(file_name_to_series.keys())
        result = []
        for group in sorted(self.__get_non_unique_groups()):
            index_list = [None] * len(self.__file_names)
            for name in self.__group_to_names[group]:
                row_index = self.__get_index_of_row(name, file_name_to_series[name.file_name])
                index_list[self.__file_names.index(name.file_name)] = row_index
            result.append(index_list)
        return result

    @staticmethod
    def create_dataframe_from_mapper(mapper) -> DataFrame:
        row_list = []
        for name, group in mapper.name_to_group.items():
            row = [name.file_name, name.name, group]
            row_list.append(row)
        result = DataFrame(
            data=row_list,
            columns=CompanyMapper.COLUMN_NAMES
        )
        result.sort_values(by=CompanyMapper.COLUMN_NAMES[1], inplace=True)
        result.reset_index(drop=True, inplace=True)
        return result

    @staticmethod
    def create_mapper_from_excel_file(path: str) :
        dataframe = read_excel(path_utils.abspath(path))
        return CompanyMapper.create_mapper_from_dataframe(dataframe)

    @staticmethod
    def create_mapper_from_dataframe(dataframe: DataFrame):
        dataframe.columns = Index(
            map(
                Utils.normalize_string,
                dataframe.columns)
        )
        if not set(CompanyMapper.COLUMN_NAMES).issubset(set(dataframe.columns)):
            raise AssertionError("dataframe")
        dataframe = dataframe[CompanyMapper.COLUMN_NAMES]
        name_to_group: Dict[CompanyNameWithFileName, int] = {}
        for _, row in dataframe.iterrows():
            name = CompanyNameWithFileName(
                row[CompanyMapper.COLUMN_NAMES[0]],
                Utils.normalize_string(row[CompanyMapper.COLUMN_NAMES[1]])
            )
            name_to_group[name] = row[CompanyMapper.COLUMN_NAMES[2]]
        return CompanyMapper(name_to_group)

    @staticmethod
    def save_mapper_to_excel(path: str, mapper) -> None:
        CompanyMapper \
            .create_dataframe_from_mapper(mapper) \
            .to_excel(path_utils.abspath(path))

    @staticmethod
    def get_group_to_names(
            name_to_group: Dict[CompanyNameWithFileName, int]
    ) -> Dict[int, List[CompanyNameWithFileName]]:
        value_set = set(name_to_group.values())
        group_to_names = {}
        for group in value_set:
            group_to_names[group] = []
            for name in name_to_group.keys():
                if name_to_group[name] == group:
                    group_to_names[group].append(name)
        return group_to_names

    def __get_unique_names(self, file_name) -> Tuple[CompanyNameWithFileName]:
        return tuple(
            filter(
                lambda name: name.file_name == file_name,
                map(
                    lambda group: self.__group_to_names[group][0],
                    filter(
                        lambda group: len(self.__group_to_names[group]) == 1,
                        self.__group_to_names.keys()
                    )
                )
            )
        )

    def __get_non_unique_groups(self) -> Tuple[int]:
        return tuple(
            filter(
                lambda group: len(self.__group_to_names[group]) > 1,
                self.__group_to_names.keys()
            )
        )

    def __check_file_names(self, file_names: Union[Sized, Iterable]):
        file_names_set = frozenset(file_names)
        if len(file_names_set) != len(file_names):
            raise AssertionError("non unique file names in list")
        if file_names_set != frozenset(self.__file_names):
            raise AssertionError("File names in passed list are not the same in mapper")

    @staticmethod
    def __get_index_of_row(name: CompanyNameWithFileName, series: Series):
        array = numpy.where(series.to_numpy() == name.name)[0]
        if len(array) == 0:
            raise AssertionError("Passed series doesn't contain passed company name")
        if len(array) > 1:
            raise AssertionError("Passed series contain duplicates")
        return array[0]
