from typing import Dict, List, Tuple


class JacardDistanceClusterization:

    def __init__(self, map_: Dict[str, List[Tuple[str, str]]], file_name_list: list, treshold=0.25, prefix_treshold=0.3):
        self.__file_to_name_and_cleaned_name_list = map_.copy()
        self.__file_name_list = file_name_list
        self.__treshold = treshold
        self.__prefix_treshold = prefix_treshold
        self.__next_group = 0
        self.__full_name_to_group = dict()
        self.__group_to_full_name = dict()
        self.__set_of_full_name_in_group = set()

    def clusterize(self):
        pairs_list = self._get_full_name_pairs()
        for pair in pairs_list:
            self.__update(pair[0], pair[1])

    @staticmethod
    def get_full_name_from_tokens(pair):
        return pair[0], " ".join(pair[1])

    def _get_full_name_pairs(self):
        pairs = []
        for idx1 in range(len(self.__file_name_list)):
            for idx2 in range(idx1 + 1, len(self.__file_name_list)):
                for name1, cleaned_name1 in self.__file_to_name_and_cleaned_name_list[self.__file_name_list[idx1]]:
                    for name2, cleaned_name2 in self.__file_to_name_and_cleaned_name_list[self.__file_name_list[idx2]]:
                        pairs.append(
                            ((name1, cleaned_name1.split(" ")), (name2, cleaned_name2.split(" ")))
                        )
        return pairs

    @staticmethod
    def __jacard_distance(list_one, list_two):
        if len(list_one) == 0 or len(list_two) == 0:
            raise AssertionError("length of list is zero")
        set_one = set(list_one)
        set_two = set(list_two)
        return 1 - len(set_one.intersection(set_two)) / len(set_one.union(set_two))

    @staticmethod
    def __is_prefix(list_one, list_two):
        return list_one[0] == list_two[0]

    @staticmethod
    def __get_name_and_tokens_list(name_and_cleaned_name_list):
        for tuple_ in name_and_cleaned_name_list:
            if not isinstance(tuple_, tuple) and len(tuple_) != 2:
                raise AssertionError("list contents don't satisfy assertion")
        return [(name, cleaned_name.split(" ")) for name, cleaned_name in name_and_cleaned_name_list]

    def __update(self, pair_one, pair_two):
        full_name_one = self.get_full_name_from_tokens(pair_one)
        full_name_two = self.get_full_name_from_tokens(pair_two)
        if self.is_in_group(full_name_one) and self.is_in_group(full_name_two):
            return
        elif self.is_in_group(full_name_one) and not self.is_in_group(full_name_two):
            if self.__is_prefix(pair_one[1], pair_two[1]):
                if self.__jacard_distance(pair_one[1], pair_two[1]) <= self.__prefix_treshold:
                    self.__put_second(full_name_one, full_name_two)
            elif self.__jacard_distance(pair_one[1], pair_two[1]) <= self.__treshold:
                self.__put_second(full_name_one, full_name_two)
        elif self.is_in_group(full_name_two) and not self.is_in_group(full_name_one):
            if self.__is_prefix(pair_one[1], pair_two[1]):
                if self.__jacard_distance(pair_one[1], pair_two[1]) <= self.__prefix_treshold:
                    self.__put_second(full_name_two, full_name_one)
            elif self.__jacard_distance(pair_one[1], pair_two[1]) <= self.__treshold:
                self.__put_second(full_name_two, full_name_one)
        else:
            if self.__is_prefix(pair_one[1], pair_two[1]):
                if self.__jacard_distance(pair_one[1], pair_two[1]) <= self.__prefix_treshold:
                    self.__put_both(full_name_two, full_name_one)
            elif self.__jacard_distance(pair_one[1], pair_two[1]) <= self.__treshold:
                self.__put_both(full_name_two, full_name_one)


    def __put_both(self, full_name_one, full_name_two):
        pass

    def __put_second(self, full_name_one, full_name_two):
        pass


    def is_in_group(self, full_name):
        return full_name in self.__set_of_full_name_in_group

