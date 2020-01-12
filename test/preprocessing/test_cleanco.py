from cleanco import cleanco


def test_commas():
    name = "bp, kek, llc"
    cleaned_name = cleanco(name).clean_name()
    assert cleaned_name == "bp, kek"
