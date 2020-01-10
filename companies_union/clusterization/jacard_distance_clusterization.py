from typing import Dict, List, Tuple
from contracts import contract


class FullName:

    def __init__(self, file_name: str, name: str, cleaned_name: str):
        self.__file_name = file_name
        self.__name = name
        self.__cleaned_name = cleaned_name
        self.__tokens = set(cleaned_name.split(" "))

    def jacard_distance(self, other):
        if len(self.tokens) == 0 or len(other.tokens) == 0:
            raise AssertionError("length of list is zero")
        return 1 - len(self.tokens.intersection(other.tokens)) / len(self.tokens.union(other.tokens))

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

    def __eq__(self, other):
        if self is other:
            return True
        elif other is None:
            return False
        elif not isinstance(other, FullName):
            return False
        else:
            return self.file_name == other.file_name and self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        hash((self.file_name, self.name))

    def __repr__(self):
        return "file_name: %s, company_name: %s" % (self.file_name, self.name)


class JacardDistanceClusterization:

    def __init__(self, map_: Dict[str, List[Tuple[str, str]]], file_name_list: list, treshold=0.25):
        self.__file_to_name_and_cleaned_name_list = map_.copy()
        self.__file_name_list = file_name_list
        self.__treshold = treshold
        self.__next_group = 0
        self.__maps = _Maps()

    def clusterize(self):
        full_name_pairs_list = [
            (FullName(*tuple1), FullName(*tuple2)) for tuple1, tuple2 in self._get_full_name_pairs()
        ]
        for full_name1, full_name2 in full_name_pairs_list:
            if self.__isin(full_name1) and self.__isin(full_name2):
                continue
            elif self.__isin(full_name1) and not self.__isin(full_name2):
                if self.__get_jacard_distance_to_group(full_name2, self.__maps.get_group(full_name1)) <= self.__treshold:
                    self.__maps.put_second(full_name1, full_name2)

            elif not self.__isin(full_name1) and self.__isin(full_name2):
                if self.__get_jacard_distance_to_group(full_name1, self.__maps.get_group(full_name2)) <= self.__treshold:
                    self.__maps.put_second(full_name2, full_name1)
            else:
                pass


    def _get_full_name_pairs(self):
        pairs = []
        for idx1 in range(len(self.__file_name_list)):
            for idx2 in range(idx1 + 1, len(self.__file_name_list)):
                for name1, cleaned_name1 in self.__file_to_name_and_cleaned_name_list[self.__file_name_list[idx1]]:
                    for name2, cleaned_name2 in self.__file_to_name_and_cleaned_name_list[self.__file_name_list[idx2]]:
                        pairs.append(
                            (
                                (self.__file_name_list[idx1], name1, cleaned_name1),
                                (self.__file_name_list[idx2], name2, cleaned_name2)
                            )
                        )
        return pairs

    def __isin(self, full_name):
        self.__maps.is_in_group(full_name)

    @staticmethod
    def __get_jacard_distance_to_group(full_name: FullName, group):
        return min(
            map(
                lambda full_name_: full_name.jacard_distance(full_name_),
                group
            )
        )


class _Maps:

    def __init__(self):
        self.current_group = 0
        self.full_name_to_group = dict()
        self.group_to_full_name = dict()
        self.full_names_set = set()

    @contract
    def is_in_group(self, full_name: FullName):
        return full_name in self.full_names_set

    @contract
    def put_both(self, full_name_one: FullName, full_name_two: FullName):
        self.full_names_set.update((full_name_one, full_name_two))
        self.full_name_to_group[full_name_one] = self.current_group
        self.full_name_to_group[full_name_two] = self.current_group
        self.group_to_full_name[self.current_group] = [full_name_one, full_name_two]
        self.current_group += 1

    @contract
    def put_second(self, full_name_one: FullName, full_name_two: FullName):
        self.full_names_set.add(full_name_two)
        group = self.full_name_to_group[full_name_one]
        self.full_name_to_group[full_name_two] = group
        self.group_to_full_name[group].append(full_name_two)

    def put(self, full_name: FullName):
        self.full_names_set.add(full_name)
        self.full_name_to_group[full_name] = self.current_group
        self.group_to_full_name[self.current_group] = [full_name]
        self.current_group += 1

    @contract
    def get_group(self, full_name: FullName):
        group = self.full_name_to_group.get(full_name)
        if group is None:
            raise AssertionError("Should be used only for FullName which is already mapped to group")
        return self.group_to_full_name[group]






