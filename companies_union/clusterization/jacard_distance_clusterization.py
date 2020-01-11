from companies_union.company_name import CompanyNameWithFileName

from typing import List
from itertools import groupby


class JacardDistanceClusterization:

    def __init__(self, company_name_list: List[CompanyNameWithFileName], treshold=0.25):
        self.__company_name_list = company_name_list.copy()
        self.__treshold = treshold
        self.__maps = _Maps()
        self.__file_name_to_names = self.get_dict_file_name_to_company_names()
        self.__file_names = tuple(sorted(self.__file_name_to_names.keys()))
        self.__file_name_to_other_names = self.get_dict_file_name_to_other_company_names()

    def clusterize(self):
        for file_name in self.__file_names:
            for name in self.__file_name_to_names[file_name]:
                if not self.__maps.is_in(name):
                    self.__maps.add(name)
                for other_name in self.__file_name_to_other_names[file_name]:
                    if not self.__maps.is_in(other_name):
                        if name.distance(other_name) <= self.__treshold:
                            self.__maps.add_to_group(name, other_name)

    def get_group_to_names(self):
        return self.__maps.get_group_to_names()

    def get_name_to_group(self):
        return self.__maps.get_name_to_group()

    def get_dict_file_name_to_company_names(self):
        sorted_list = sorted(self.__company_name_list, key=lambda company_name: company_name.file_name)
        file_name_to_names = {}
        for file_name, names in groupby(sorted_list, key=lambda company_name: company_name.file_name):
            file_name_to_names[file_name] = tuple(names)
        return file_name_to_names

    def get_dict_file_name_to_other_company_names(self):
        result = {}
        for idx1 in range(len(self.__file_names)):
            current_name = self.__file_names[idx1]
            names = []
            for idx2 in range(idx1 + 1, len(self.__file_names)):
                other_name = self.__file_names[idx2]
                names.extend(self.__file_name_to_names[other_name])
            result[current_name] = names
        return result


class _Maps:

    def __init__(self):
        self.name_to_group = dict()
        self.group_to_names = dict()
        self.classified_names = set()
        self.next_group = 0

    def add(self, name: CompanyNameWithFileName):
        self.classified_names.add(name)
        self.name_to_group[name] = self.next_group
        self.group_to_names[self.next_group] = [name]
        self.next_group += 1

    def add_to_group(self, name: CompanyNameWithFileName, other_name: CompanyNameWithFileName):
        self.classified_names.add(other_name)
        if self.name_to_group.get(name) is None:
            raise AssertionError("Must be in dict")
        group: int = self.name_to_group[name]
        self.name_to_group[other_name] = group
        self.group_to_names[group].append(other_name)

    def is_in(self, name: CompanyNameWithFileName):
        return name in self.classified_names

    def get_group_to_names(self):
        return self.group_to_names.copy()

    def get_name_to_group(self):
        return self.name_to_group.copy()






