from companies_union.company_name import CompanyNameWithFileName


class TestCompanyNameWithFileName:

    def test_equals_FullName(self):
        first = ["das", "a b, llc"]
        second = ["das", "a B, \n lLc \n"]
        assert CompanyNameWithFileName(*first) == CompanyNameWithFileName(*second)

    def test_tokens(self):
        first = ["das", "a b, llc"]
        assert CompanyNameWithFileName(*first).tokens == {"a", "b"}

    def test_jacard_distances(self):
        first = ["das", "a e", "a"]
        second = ["das", "a b c d e", "a b c d"]
        assert CompanyNameWithFileName(*first).jacard_distance(CompanyNameWithFileName(*second)) == 0.75
