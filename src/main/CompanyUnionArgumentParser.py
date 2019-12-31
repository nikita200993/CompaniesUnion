from argparse import ArgumentParser


class CompanyUnionArgumentParser(ArgumentParser):

    def __init__(self):
        super().__init__(prog="Union maker from excel datasets of companies")
        self.add_argument("datasets",
                          type=str,
                          nargs="+",
                          help="list of excel files to process (more than one file)")
        self.add_argument("-id",
                          "--idFieldName",
                          required=True,
                          type=str,
                          help="Field name with companies identificators")
