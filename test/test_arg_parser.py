from companies_union.CompanyUnionArgumentParser import CompanyUnionArgumentParser


class TestArgParser:

    def test_1(self):
        args = ["./ds.xlsx", "kek.xlsx", "-f", "abc"]
        arg_parser = CompanyUnionArgumentParser()
        namespace = arg_parser.parse_args(args)
        set_of_files_expected = {"./ds.xlsx", "kek.xlsx"}
        assert set_of_files_expected == {x for x in namespace.datasets}

    def test_2(self):
        args = ["./ds.xlsx", "kek.xlsx"]
        arg_parser = CompanyUnionArgumentParser()
        try:
            arg_parser.parse_args(args)
            assert 1 == 0, "exception wasn't thrown"
        except SystemExit:
            pass

    def test_3(self):
        args = ["./ds.xlsx", "kek.xlsx", "-f", "abc"]
        arg_parser = CompanyUnionArgumentParser()
        namespace = arg_parser.parse_args(args)
        assert " ".join(namespace.field_name) == "abc"

    def test_4(self):
        args = ["./ds.xlsx", "kek.xlsx", "-f", "abc kek"]
        arg_parser = CompanyUnionArgumentParser()
        namespace = arg_parser.parse_args(args)
        assert " ".join(namespace.field_name).strip() == "abc kek"

    def test_5(self):
        args = ["./ds.xlsx", "kek.xlsx", "-f", "abc kek zZa    ", "-m", "Ab.xlsx"]
        arg_parser = CompanyUnionArgumentParser()
        namespace = arg_parser.parse_args(args)
        assert namespace.mapper == "Ab.xlsx"