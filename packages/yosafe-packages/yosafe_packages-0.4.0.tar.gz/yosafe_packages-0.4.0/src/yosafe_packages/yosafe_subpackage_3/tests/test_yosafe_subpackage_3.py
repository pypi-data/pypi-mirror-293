
from yosafe_subpackage_3 import *

def test_yosafe_get_yosafe_subpackage_2():
    result = yosafe_get_yosafe_subpackage_3()
    print(result)
    assert "Error" not in result



def test_yosafe_add():
    assert yosafe_mul(4,5) == 20
    assert yosafe_mul(-3, 5) == -15
    assert yosafe_mul(-3, -5) == 15