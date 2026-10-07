import pytest
from calculator.factory import CalculationFactory
from calculator.inputs import read_csv_values


def test_sources_share_calculation_policy(tmp_path):
    path = tmp_path / 'values.csv'
    path.write_text('value\n10\n20\n30\n40\n50\n')
    for name in ('mean', 'stddev'):
        from_csv = CalculationFactory.create(name, *read_csv_values(path)).get_result()
        manual = CalculationFactory.create(name, *[10, 20, 30, 40, 50]).get_result()
        assert from_csv == pytest.approx(manual)


def test_missing_column(tmp_path):
    path = tmp_path / 'values.csv'
    path.write_text('wrong\n1\n2\n')
    with pytest.raises(ValueError, match='value'):
        read_csv_values(path)


def test_missing_file(tmp_path):
    with pytest.raises(OSError):
        read_csv_values(tmp_path / 'missing.csv')


def test_missing_observation_is_rejected(tmp_path):
    path = tmp_path / 'values.csv'
    path.write_text('value\n1\n""\n3\n')
    with pytest.raises(ValueError, match='finite'):
        CalculationFactory.create('stddev', *read_csv_values(path))


def test_blank_lines_follow_pandas_default(tmp_path):
    path = tmp_path / 'values.csv'
    path.write_text('value\n1\n\n3\n')
    assert CalculationFactory.create('stddev', *read_csv_values(path)).get_result() == pytest.approx(2 ** 0.5)
