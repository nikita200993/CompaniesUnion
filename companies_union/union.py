from companies_union.preprocessing.DataFramePreprocessor import DataFramePreprocessor
from companies_union.clusterization.jacard_distance_clusterization import JacardDistanceClusterization
from companies_union.companymapper import CompanyMapper
from companies_union.preprocessing.utils import Utils

import os.path as path_utils
from typing import Iterable
from pandas import DataFrame, Index, MultiIndex, read_excel
from os import getcwd


def get_union_from_files(paths: Iterable[str], key: str, mapper_path=None):
    file_paths_absolute = [path_utils.abspath(file_name) for file_name in paths]
    check_existence(file_paths_absolute)
    file_names = [path_utils.basename(path) for path in paths]
    file_names = sorted(file_names)
    dataframes = [read_excel(path) for path in file_paths_absolute]
    get_union_from_dataframes(dataframes, file_names, key)


def get_union_from_dataframes(dataframes: Iterable[DataFrame], file_names: Iterable[str], key: str, mapper_path=None):
    """

    :param dataframes: correspond to file_names
    :param file_names: sorted!!!!
    :param key: name of field with company names
    :param mapper_path: path to dataframe in file system with mapping info
    :return: rows from original dataframes for some dataframes
    """
    if mapper_path is None:
        processor = DataFramePreprocessor(key)
        company_names_list = processor.get_company_names_from_dataframes(dataframes, file_names)
        clusterizator = JacardDistanceClusterization(company_names_list)
        clusterizator.clusterize()
        mapper_path = path_utils.join(getcwd(), "mapper.xlsx")
        CompanyMapper.save_mapper_to_excel(mapper_path, clusterizator.get_name_to_group())
    name_to_group = CompanyMapper.create_mapper_from_excel_file(mapper_path)
    file_name_to_series = {}
    for file_name, df in zip(file_names, dataframes):
        df_copy = df.copy()
        df_copy.columns = Index(df_copy.columns.map(Utils.normalize_string))
        file_name_to_series[file_name] = df[key].map(Utils.normalize_string)
    mapper = CompanyMapper(name_to_group)
    indexes_list = mapper.get_indexes_of_common_companies(file_name_to_series)
    row_list = []
    for indexes in indexes_list:
        row = []
        for idx, df in enumerate(dataframes):
            if indexes[idx] is None:
                row.extend([None] * df.shape[1])
            else:
                row.extend(df.iloc[indexes[idx], :].to_list())
        row_list.append(row)
    level_0_index = []
    level_1_index = []
    for file_name, df in zip(file_names, dataframes):
        level_0_index.extend([file_name] * df.shape[1])
        level_1_index.extend(df.columns.to_list())
    new_column_index = MultiIndex.from_tuples(zip(level_0_index, level_1_index))
    union_df = DataFrame(
        data=row_list,
        columns=new_column_index
    )
    return union_df


def check_existence(paths: "list of strings representing paths"):
    for path_ in paths:
        if not path_utils.exists(path_):
            raise FileNotFoundError(f"File: {path_} was not found")