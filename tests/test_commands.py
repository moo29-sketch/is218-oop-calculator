import pytest
from calculator.commands import Command, CalculateCommand, HistoryCommand, ClearHistoryCommand, HelpCommand
from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession


def test_contract_is_abstract():

    class IncompleteCommand(Command):
        pass
    with pytest.raises(TypeError):
        IncompleteCommand()


def test_action_flow_and_history():
    session = CalculatorSession()
    calculation = CalculationFactory.create('add', *[2, 3])
    command = CalculateCommand(session, calculation)
    assert session.get_history() == []
    assert command.execute() == 'Result: 5.0000'
    assert 'add 2.0 3.0 = 5.0000' in HistoryCommand(session).execute()
    assert ClearHistoryCommand(session).execute() == 'History cleared.'
    assert HistoryCommand(session).execute() == 'History is empty.'


def test_failure_is_not_recorded():
    session = CalculatorSession()
    command = CalculateCommand(session, CalculationFactory.create('divide', *[1, 0]))
    with pytest.raises(ZeroDivisionError):
        command.execute()
    assert session.get_history() == []


def test_help_has_no_session_dependency():
    assert 'history' in HelpCommand().execute()
