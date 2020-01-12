from companies_union.company_name import CompanyNameWithFileName
from companies_union.preprocessing.utils import Utils

import os.path as path_utils
from pandas import DataFrame, read_excel, Index
from typing import Dict


class CompanyMapper:

    COLUMN_NAMES = ["file_name", "company_name", "group_id"]

    def __init__(self, name_to_group: Dict[CompanyNameWithFileName, int]):
        self.__name_to_group = name_to_group.copy()
        self.__group_to_names = CompanyMapper.get_group_to_names(self.__name_to_group)


    @staticmethod
    def create_dataframe_from_mapper(mapper: Dict[CompanyNameWithFileName, int]) -> DataFrame:
        row_list = []
        for name, group in mapper.items():
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
    def create_mapper_from_excel_file(path: str) -> Dict[CompanyNameWithFileName, int]:
        dataframe = read_excel(path_utils.abspath(path))
        return CompanyMapper.create_mapper_from_dataframe(dataframe)

    @staticmethod
    def create_mapper_from_dataframe(dataframe: DataFrame) -> Dict[CompanyNameWithFileName, int]:
        dataframe.columns = Index(
            map(
                Utils.normalize_string,
                dataframe.columns)
        )
        if not set(CompanyMapper.COLUMN_NAMES).issubset(set(dataframe.columns)):
            raise AssertionError("dataframe")
        dataframe = dataframe[CompanyMapper.COLUMN_NAMES]
        mapper: Dict[CompanyNameWithFileName, int] = {}
        for _, row in dataframe.iterrows():
            name = CompanyNameWithFileName(
                row[CompanyMapper.COLUMN_NAMES[0]],
                row[CompanyMapper.COLUMN_NAMES[1]]
            )
            mapper[name] = row[CompanyMapper.COLUMN_NAMES[2]]
        return mapper

    @staticmethod
    def save_mapper_to_excel(path: str, mapper: Dict[CompanyNameWithFileName, int]) -> None:
        CompanyMapper\
            .create_dataframe_from_mapper(mapper)\
            .to_excel(path_utils.abspath(path))

    @staticmethod
    def get_group_to_names(name_to_group: Dict[CompanyNameWithFileName, int]):
        value_set = set(name_to_group.values())
        group_to_names = {}
        for group in value_set:
            group_to_names[group] = []
            for name in name_to_group.keys():
                if name_to_group[name] == group:
                    group_to_names[group].append(name)
        return group_to_names



