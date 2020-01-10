import pandas as pd
import collections.abc as abc
from os import path
from contracts import contract

from companies_union.CompanyUnionArgumentParser import CompanyUnionArgumentParser
from companies_union.preprocessing.DataFramePreprocessor import DataFramePreprocessor


@contract(paths=abc.Iterable)
def check_existence(paths: "list of strings representing paths"):
    for path_ in paths:
        if not path.exists(path_):
            raise FileNotFoundError(f"File: {path_} was not found")


@contract
def check_key_existence(indexes: pd.Index, *, key: str, original_key: str):
    if not indexes.contains(key):
        raise AssertionError(f"There is no column with key = {original_key}")


@contract(paths_to_excel_files=abc.Iterable)
def get_data_frames_from_paths(paths_to_excel_files: "list of strings representing excel files"):
    absolute_paths = [path.abspath(path_) for path_ in paths_to_excel_files]
    check_existence(absolute_paths)
    return list(
        map(pd.read_excel, absolute_paths)
    )


@contract(paths_to_excel_files=abc.Iterable)
def get_file_names_from_paths(paths_to_excel_files: "list of strings representing excel files"):
    return [path.basename(path.abspath(path_)) for path_ in paths_to_excel_files]


if __name__ == "__main__":
    args = CompanyUnionArgumentParser().parse_args()
    id_field_name = args.idFieldName
    data_frame_list = get_data_frames_from_paths(args.datasets)
    file_names = get_file_names_from_paths(args.datasets)
    processer = DataFramePreprocessor(id_field_name)
    grouper_dataframe = processer.get_grouper_dataframe_from_lists(data_frame_list, file_names)