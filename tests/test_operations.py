import pytest
from calculator.operations import Operations


@pytest.mark.parametrize('operation,a,b,expected', [(Operations.add, 2, 3, 5), (Operations.subtract, 2, 3, -1), (Operations.multiply, -2, 3, -6), (Operations.divide, 7, 2, 3.5)])

def test_arithmetic(operation, a, b, expected):
    assert operation(a, b) == pytest.approx(expected)


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        Operations.divide(1, 0)


@pytest.mark.parametrize("operation,expected", [(Operations.square, 9), (Operations.sqrt, 3)])

def test_unary_operations(operation, expected):
    assert operation(9 if operation is Operations.sqrt else 3) == expected



def test_power_keyword_only_option():
    assert Operations.power(3, exponent=4) == 81



def test_square_root_domain():
    with pytest.raises(ValueError):
        Operations.sqrt(-1)


def test_sum_accepts_a_collection():
    assert Operations.sum(2, 4, 6) == 12
    with pytest.raises(ValueError):
        Operations.sum()
