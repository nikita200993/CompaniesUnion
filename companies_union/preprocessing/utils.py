import re
from contracts import contract


class Utils:

    WS_PATTERN = re.compile("\\s+")

    @staticmethod
    @contract
    def replace_redundant_ws(string: str):
        return re.subn(Utils.WS_PATTERN, " ", string)[0].strip()

