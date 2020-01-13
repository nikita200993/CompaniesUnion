from argparse import ArgumentParser


class CompanyUnionArgumentParser(ArgumentParser):

    def __init__(self):
        super().__init__(prog="Union maker from excel datasets of companies")
        self.add_argument("datasets",
                          type=str,
                          nargs="+",
                          help="list of excel files to process (more than one file)")
        self.add_argument("-f",
                          "--field_name",
                          required=True,
                          type=str,
                          nargs="+",
                          help="Field name with companies identificators")

        self.add_argument("-m",
                          "--mapper",
                          required=False,
                          type=str,
                          help="map from companies to group ids")
        self.add_argument("-t",
                          "--target",
                          required=False,
                          type=str,
                          help="path to save results")
