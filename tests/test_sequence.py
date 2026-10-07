from calculator.calculation import Calculation
from calculator.operations import Operations
from calculator.sequence import execute_sequence
from calculator.session import CalculatorSession


def test_sequence_continues_after_failure_and_records_only_success():
    calculations = [
        Calculation([2, 3], Operations.add),
        Calculation([1, 0], Operations.divide),
        Calculation([3], Operations.square),
    ]
    session = CalculatorSession()
    results, errors = execute_sequence(session, calculations)
    assert results == [5.0, 9.0]
    assert len(errors) == 1
    assert len(session.get_history()) == 2


def test_empty_sequence_changes_no_state():
    session = CalculatorSession()
    assert execute_sequence(session, []) == ([], [])
    assert session.get_history() == []
