import pandas as pd
import collections.abc as abc
from os import path
from contracts import contract

from companies_union.CompanyUnionArgumentParser import CompanyUnionArgumentParser
from companies_union.preprocessing.DataFramePreprocessor import DataFramePreprocessor
from companies_union.companymapper import CompanyMapper


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
    if args.mapper:
        id_field_name = args.idFieldName
        data_frame_list = get_data_frames_from_paths(args.datasets)
        data_frame_copy_list = [df.copy(deep=True) for df in data_frame_list]
        file_names = get_file_names_from_paths(args.datasets)
        processor = DataFramePreprocessor(id_field_name)
        company_names = processor.get_company_names_from_dataframes(data_frame_list, file_names)
        args.mapper = "mapper.xlsx"
        CompanyMapper.save_mapper_to_excel(args.mapper)

    check_existence(path.abspath(args.mapper))
    mapper = CompanyMapper.create_mapper_from_excel_file(path.abspath(args.mapper))
