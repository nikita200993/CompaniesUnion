from companies_union.company_name import CompanyNameWithFileName


class TestCompanyNameWithFileName:

    def test_equals(self):
        first = ["das", "a b, llc"]
        second = ["das", "a B, \n lLc \n"]
        assert CompanyNameWithFileName(*first) == CompanyNameWithFileName(*second)

    def test_tokens(self):
        first = ["das", "a b, llc"]
        assert CompanyNameWithFileName(*first).tokens == {"a", "b"}

    def test_jacard_distances(self):
        first = ["das", "a e"]
        second = ["das", "a b c d e"]
        assert CompanyNameWithFileName(*first).jacard_distance(CompanyNameWithFileName(*second)) == 0.6

    def test_jacard_distances(self):
        first = CompanyNameWithFileName("a", "a b c e f, llc")
        second = CompanyNameWithFileName("a", "a b c d, llc")
        assert first.jacard_distance(second) == 0.5

    def test_distances(self):
        first = CompanyNameWithFileName("a", "a b c e f, llc")
        second = CompanyNameWithFileName("a", "a b c d, llc")
        assert first.distance(second) >= 1

