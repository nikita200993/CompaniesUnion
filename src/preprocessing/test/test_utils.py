from utils import Utils
from contracts import ContractNotRespected


class TestUtils:

    def test_contract(self):
        try:
            Utils.replace_redundant_ws(1)
            assert 1 == 0, "contract doesn't work"
        except ContractNotRespected:
            pass

    def test_ws_remove_1(self):
        arg = "abc  abc\tabc"
        expected = "abc abc abc"
        actual = Utils.replace_redundant_ws(arg)
        assert expected == actual

    def test_ws_remove_2(self):
        arg = "\tabc \t abc\t\tabc"
        expected = "abc abc abc"
        actual = Utils.replace_redundant_ws(arg)
        assert expected == actual

    def test_newline_replace(self):
        arg = "\n\n abc\r\n\r\n\tabc"
        expected = "abc abc"
        actual = Utils.replace_redundant_ws(arg)
        assert actual == expected
