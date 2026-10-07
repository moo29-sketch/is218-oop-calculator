import pytest
from calculator.statistics import mean, standard_deviation


def test_known_sample():
    assert standard_deviation([10, 20, 30, 40, 50]) == pytest.approx(15.811388300841896)


def test_constant_values():
    assert standard_deviation([7, 7, 7]) == 0


def test_mean():
    assert mean(['2', '4', '6']) == 4


@pytest.mark.parametrize('values', [[], [1], [1, 'x'], [1, None], [1, float('inf')], [1, float('nan')]])

def test_reject_invalid_values(values):
    with pytest.raises(ValueError):
        standard_deviation(values)


def test_mean_requires_observation():
    with pytest.raises(ValueError):
        mean([])


@pytest.mark.parametrize('operation', [mean, standard_deviation])

def test_reject_overflowing_statistic(operation):
    with pytest.raises(ValueError, match='range'):
        operation([1e+308, 1e+308])


def test_reject_invalid_ddof():
    with pytest.raises(ValueError, match="ddof"):
        standard_deviation([1, 3], ddof=2)
