from cleanco import cleanco

from companies_union.preprocessing.utils import Utils


class CompanyNameWithFileName:

    def __init__(self, file_name: str, name: str):
        self.__file_name = file_name
        self.__name = Utils.replace_redundant_ws(name).lower()
        self.__cleaned_name = cleanco(self.__name).clean_name()
        self.__tokens = set(self.__cleaned_name.split(" "))

    def __eq__(self, other):
        if self is other:
            return True
        elif other is None:
            return False
        elif not isinstance(other, CompanyNameWithFileName):
            return False
        else:
            return self.file_name == other.file_name and self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        hash((self.file_name, self.name))

    def __repr__(self):
        return "file_name: %s, company_name: %s" % (self.file_name, self.name)

    @property
    def file_name(self):
        return self.__file_name

    @property
    def name(self):
        return self.__name

    @property
    def cleaned_name(self):
        return self.__cleaned_name

    @property
    def tokens(self):
        return self.__tokens

    def jacard_distance(self, other):
        if not isinstance(other, CompanyNameWithFileName):
            raise TypeError("Argument should be instance of class: %s" % CompanyNameWithFileName.__name__)
        if self.file_name != other.file_name:
            return 1
        if len(self.tokens) == 0 or len(other.tokens) == 0:
            raise AssertionError("length of list is zero")
        return 1 - len(self.tokens.intersection(other.tokens)) / len(self.tokens.union(other.tokens))
