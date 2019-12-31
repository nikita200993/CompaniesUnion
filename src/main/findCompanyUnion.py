import pandas as pd
import collections.abc as abc
from os import path
from contracts import contract

from main.CompanyUnionArgumentParser import CompanyUnionArgumentParser
from preprocessing.utils import Utils


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


@contract
def preprocess_col_names(data_frame: pd.DataFrame):
    data_frame.columns = pd.Index(
        data=[Utils.replace_redundant_ws(column_name).lower()
              for column_name in data_frame.columns]
    )


@contract
def preprocess_name_column(data_frame: pd.DataFrame, key: str):
    data_frame[key] = data_frame[key].map(Utils.replace_redundant_ws)
    data_frame[key] = data_frame[key].map(str.lower)


@contract
def add_cleaned_names_column(data_frame: pd.DataFrame, key: str, mapper: abc.Mapping):
    data_frame[key + "_cleaned"] = data_frame[key].map()


if __name__ == "__main__":
    args = CompanyUnionArgumentParser().parse_args()
    id_field_name = args.idFieldName.lower()
    data_frame_list = get_data_frames_from_paths(args.datasets)
    data_frame_copies_list = [data_frame.copy(deep=True) for data_frame in data_frame_list]
    for data_frame in data_frame_copies_list:
        preprocess_col_names(data_frame)
    for data_frame in data_frame_copies_list:
        check_key_existence(data_frame.columns, key=id_field_name, original_key=args.idFieldName)
    for data_frame in data_frame_copies_list:
        preprocess_name_column(data_frame, id_field_name)
    for data_frame in data_frame_copies_list:
        pass




