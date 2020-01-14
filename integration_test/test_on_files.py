from companies_union.CompanyUnionArgumentParser import CompanyUnionArgumentParser
from companies_union.union import get_union_from_files

import os.path as path_utils
from pandas import read_excel

cmd_line_args = ["1.xlsx", "2.xlsx", "3.xlsx", "4.xlsx", "-f", "company", "name", "-t", "resources"]
result_path_1 = path_utils.join("resources", "result.xlsx")
result_path_2 = path_utils.join("resources", "processedResult.xlsx")


def on_real_files_1():
    args = CompanyUnionArgumentParser().parse_args(cmd_line_args)
    file_names = map(lambda file_name: path_utils.join("resources", file_name), args.datasets)
    field_name = " ".join(args.field_name).strip()
    actual = get_union_from_files(file_names, field_name, mapper_path=args.mapper, save_path=args.target)
    expected = read_excel(result_path_1, header=[0, 1])
    assert actual.equals(expected)


def test_on_real_files_2():
    cmd_line_args.extend(
        ("-m", path_utils.join("resources", "processedMapper.xlsx"))
    )
    args = CompanyUnionArgumentParser().parse_args(cmd_line_args)
    file_names = map(lambda file_name: path_utils.join("resources", file_name), args.datasets)
    field_name = " ".join(args.field_name).strip()
    actual = get_union_from_files(file_names, field_name, mapper_path=args.mapper, save_path=args.target)
    expected = read_excel(result_path_2, header=[0, 1])
    actual.fillna(value="", inplace=True)
    expected.fillna(value="", inplace=True)
    assert actual.equals(expected)