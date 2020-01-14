#!/usr/bin/env/ python3
from companies_union.union import get_union_from_files
from companies_union.CompanyUnionArgumentParser import CompanyUnionArgumentParser


if __name__ == "__main__":
    argparser = CompanyUnionArgumentParser()
    args = argparser.parse_args()
    field_name = " ".join(args.field_name).strip()
    file_names = args.datasets
    get_union_from_files(file_names, field_name, mapper_path=args.mapper, save_path=args.target)
