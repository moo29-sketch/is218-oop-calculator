import pytest
from calculator.calculation import Calculation
from calculator.factory import CalculationFactory


@pytest.mark.parametrize('name,values,expected', [(' ADD ', ['2', '3'], 5), ('subtract', [2, 3], -1), ('multiply', [2, 3], 6), ('divide', [7, 2], 3.5), ('mean', [2, 4, 6], 4), ('stddev', [2, 4, 6], 2)])

def test_factory_configures_calculation(name, values, expected):
    calculation = CalculationFactory.create(name, *values)
    assert isinstance(calculation, Calculation)
    assert calculation.get_result() == pytest.approx(expected)


@pytest.mark.parametrize('name,values', [('unknown', [1, 2]), ('add', [1]), ('add', [1, 2, 3]), ('add', ['x', '2']), ('add', [1, float('inf')])])

def test_factory_rejects_invalid_request(name, values):
    with pytest.raises(ValueError):
        CalculationFactory.create(name, *values)


def test_factory_does_not_execute():
    calculation = CalculationFactory.create('divide', *[1, 0])
    with pytest.raises(ZeroDivisionError):
        calculation.get_result()


@pytest.mark.parametrize("name,values,options,expected", [
    ("square", [3], {}, 9), ("sqrt", [9], {}, 3),
    ("power", [3], {"exponent": "4"}, 81),
    ("stddev", [2, 4, 6], {"ddof": 0}, (8 / 3) ** .5),
])

def test_argument_counts_and_named_options(name, values, options, expected):
    assert CalculationFactory.create(name, *values, **options).get_result() == pytest.approx(expected)



@pytest.mark.parametrize("name,values,options", [
    ("square", [1, 2], {}), ("sqrt", [], {}),
    ("add", [1, 2], {"exponent": 2}), ("power", [2], {"exponent": "x"}),
])

def test_reject_invalid_argument_contract(name, values, options):
    with pytest.raises(ValueError):
        CalculationFactory.create(name, *values, **options)
