
from yosafe_subpackage_2 import *

def test_yosafe_get_yosafe_subpackage_2():
    result = yosafe_get_yosafe_subpackage_2()
    print(result)
    assert "Error" not in result



def test_yosafe_add():
    assert yosafe_sub(99, 99) == 0
    assert yosafe_sub(-3, 1) == -4