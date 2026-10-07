import pytest

from calculator.cli import prepare_command
from calculator.factory import CalculationFactory
from calculator.inputs import read_csv_values
from calculator.session import CalculatorSession
from calculator.statistics import median


def test_median_known_odd_and_even_samples():
    assert median([1, 5, 3]) == 3
    assert median([2, 4, 6, 8]) == 5


def test_median_requires_an_observation():
    with pytest.raises(ValueError):
        median([])


def test_factory_creates_median_calculation():
    calculation = CalculationFactory.create("median", 9, 1, 5)
    assert calculation.get_result() == 5


def test_csv_median_uses_the_same_calculation_policy(tmp_path):
    path = tmp_path / "values.csv"
    path.write_text("value\n9\n1\n5\n")
    from_csv = CalculationFactory.create("median", *read_csv_values(path)).get_result()
    manual = CalculationFactory.create("median", 9, 1, 5).get_result()
    assert from_csv == pytest.approx(manual)


def test_cli_prepares_csv_median(tmp_path):
    path = tmp_path / "values.csv"
    path.write_text("value\n10\n30\n20\n")
    command = prepare_command(f"csv median {path}", CalculatorSession())
    assert command.execute() == "Result: 20.0000"
