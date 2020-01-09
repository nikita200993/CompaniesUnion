from typing import Dict, List
from contracts import contract
import project_contracts.project_contracts


class JacardDistanceClusterization:

    def __init__(self, map_: Dict[str, List[str]], treshold=0.25, prefix_treshold=0.35):
        self.__initial_map = map_.copy()
        self.__treshold = treshold
        self.__prefix_treshold = prefix_treshold
        self.__full_name_to_group = dict()
        self.__next_available__group = 0
        self.__map_with_tokens = {}
        for key, list_value in self.__initial_map:
            self.__map_with_tokens[key] = list(
                map(lambda string: string.split(" "), list_value)
            )

    def clusterize(self):
        pairs_list = self.__get_full_name_pairs()
        for pair in pairs_list:
            self.__update(pair[0], pair[1])

    @staticmethod
    @contract(list_one="non_empty_iterable", list_two="non_empty_iterable")
    def __jacard_distance(list_one, list_two):
        if len(list_one) == 0 or len(list_two) == 0:
            raise AssertionError("length of list is zero")
        set_one = set(list_one)
        set_two = set(list_two)
        return 1 - len(set_one.intersection(set_two)) / len(set_one.union(set_two))

    @staticmethod
    @contract(list_one="non_empty_iterable", list_two="non_empty_iterable")
    def __is_prefix(list_one, list_two):
        return list_one[0] == list_two[0]

    def __update(self, full_name_one, full_name_two):
        key_set = self.__full_name_to_group.keys()
        if (full_name_one in key_set) and (full_name_two in key_set):
            return
        elif (full_name_one in key_set) or (full_name_two in key_set):
            if self.__is_prefix(full_name_one[1], full_name_two[1]):
                if self.__jacard_distance(full_name_one[1], full_name_two[1]) <= self.__prefix_treshold:
                    if self.__full_name_to_group.get(full_name_one) is None:
                        group = self.__full_name_to_group.get(full_name_two)
                        self.__full_name_to_group[full_name_one] = group
                    else:
                        group = self.__full_name_to_group.get(full_name_one)
                        self.__full_name_to_group[full_name_two] = group
            elif self.__jacard_distance(full_name_one[1], full_name_two[1]) <= self.__treshold:
                if self.__full_name_to_group.get(full_name_one) is None:
                    group = self.__full_name_to_group.get(full_name_two)
                    self.__full_name_to_group[full_name_one] = group
                else:
                    group = self.__full_name_to_group.get(full_name_one)
                    self.__full_name_to_group[full_name_two] = group
        else:
            if self.__is_prefix(full_name_one[1], full_name_two[1]):
                if self.__jacard_distance(full_name_one[1], full_name_two[1]) <= self.__prefix_treshold:
                        self.__full_name_to_group
                        self

            elif self.__jacard_distance(full_name_one[1], full_name_two[1]) <= self.__treshold:
                if self.__full_name_to_group.get(full_name_one) is None:
                    group = self.__full_name_to_group.get(full_name_two)
                    self.__full_name_to_group[full_name_one] = group
                else:
                    group = self.__full_name_to_group.get(full_name_one)
                    self.__full_name_to_group[full_name_two] = group

    def __get_full_name_pairs(self):
        keys_list = list(self.__map_with_tokens.keys())
        result = []
        for idx in range(len(keys_list)):
            for token_list in self.__map_with_tokens.get(keys_list[idx]):
                for idx2 in range(idx + 1, len(keys_list)):
                    for token_list2 in self.__map_with_tokens.get(keys_list[idx2]):
                        result.append([(keys_list[idx], token_list), (keys_list[idx2], token_list2)])
        return result
