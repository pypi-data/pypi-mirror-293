####################################################
# test_utils.py for the 'cmpparis' library
# Created by: Sofiane Charrad
####################################################

from cmpparis.utils import hello_paris

def test_hello_paris():
    assert hello_paris() == "Bonjour, Paris!"