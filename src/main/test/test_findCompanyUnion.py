import os
from contracts import ContractNotRespected

from main.findCompanyUnion import check_existence

RESOURCES_FOLDER = os.path.abspath("./src/test/resources/")


def test_check_existence_1():
    non_existent_file = ".fsdfa32d"
    try:
        check_existence([non_existent_file])
        assert 1 == 0, f"{FileNotFoundError} wasn't thrown"
    except FileNotFoundError:
        pass


def test_check_existence_2():
    non_existent_file = "./src"
    try:
        check_existence([non_existent_file])
    except FileNotFoundError as er:
        assert 1 == 0, f"Error was thrown, but it shouldn't: {er}"


def test_check_existence_contract():
    try:
        check_existence(1)
        assert 1 == 0, "contract doesn't work"
    except ContractNotRespected:
        pass

