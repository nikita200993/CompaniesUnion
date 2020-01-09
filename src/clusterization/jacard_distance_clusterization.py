from typing import Dict, List


class JacardDistanceClusterization:

    def __init__(self, map_: Dict[str, List[str]]):
        self.__initial_map = map_.copy()
        self.__map_with_tokens = {}
        for key, value in self.__initial_map:
            map(lambda string: string.split(" "))
