import pytest
from calculator.cli import run, prepare_command
from calculator.session import CalculatorSession


def test_interactive_session(monkeypatch, capsys):
    answers = iter(['add 2 3', 'history', 'clear', 'history', 'help', 'exit'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(answers))
    run()
    output = capsys.readouterr().out
    assert 'Result: 5.0000' in output
    assert 'add 2.0 3.0 = 5.0000' in output
    assert 'History cleared.' in output
    assert 'History is empty.' in output
    assert 'Goodbye!' in output


def test_recovers_after_invalid_input(monkeypatch, capsys):
    answers = iter(['unknown', 'add one two', 'divide 1 0', 'add 2 3', 'exit'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(answers))
    run()
    output = capsys.readouterr().out
    assert output.count('Error:') == 3
    assert 'Result: 5.0000' in output


@pytest.mark.parametrize('text', ['', 'history 1', 'clear 1', 'help 1', 'csv', 'csv add values.csv'])

def test_reject_invalid_syntax(text):
    with pytest.raises(ValueError):
        prepare_command(text, CalculatorSession())


def test_csv_and_manual_session(monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'values.csv').write_text('value\n10\n20\n30\n40\n50\n')
    answers = iter(['stddev 10 20 30 40 50', 'csv stddev values.csv', 'exit'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(answers))
    run()
    assert capsys.readouterr().out.count('Result: 15.8114') == 2


@pytest.mark.parametrize('error', [EOFError, KeyboardInterrupt])

def test_input_ends_cleanly(monkeypatch, capsys, error):

    def stop(prompt):
        raise error()
    monkeypatch.setattr('builtins.input', stop)
    run()
    assert 'Goodbye!' in capsys.readouterr().out


def test_recovers_from_csv_failures(monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'empty.csv').write_text('')
    (tmp_path / 'bad.csv').write_text('value\n"unterminated\n')
    answers = iter(['csv mean missing.csv', 'csv mean empty.csv', 'csv mean bad.csv', 'add 1 2', 'exit'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(answers))
    run()
    output = capsys.readouterr().out
    assert output.count('Error:') == 3
    assert 'Result: 3.0000' in output


def test_unary_and_options_session(monkeypatch, capsys):
    answers = iter(["square 3", "sqrt -1", "sqrt 9", "power 3 exponent=4", "power 3 exponent=2 exponent=4", "history", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    run()
    output = capsys.readouterr().out
    assert "Result: 9.0000" in output
    assert "Result: 3.0000" in output
    assert "Result: 81.0000" in output
    assert output.count("Error:") == 2
    assert "power 3.0 exponent=4.0 = 81.0000" in output
