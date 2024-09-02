
from yosafe_subpackage_1 import *

def test_yosafe_get_yosafe_subpackage_1():
    result = yosafe_get_yosafe_subpackage_1()
    print(result)
    assert "Error" not in result



def test_yosafe_add():
    assert yosafe_add(1, 2) == 3
    assert yosafe_add(-1, 1) == 0