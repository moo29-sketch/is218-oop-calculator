"""A test conversation provides input and checks what the app prints."""

from calculator.cli import run


def session(monkeypatch, capsys, answers):
    # iter is a cursor; next takes one response for each input prompt.
    responses = iter(answers)

    def scripted_input(prompt):
        return next(responses)

    # pytest supplies these fixtures and restores input after the test.
    monkeypatch.setattr("builtins.input", scripted_input)
    run()
    return capsys.readouterr().out


def test_arithmetic_session(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["add", "10", "5", "subtract", "20", "7", "exit"])
    assert "Result: 15" in output
    assert "Result: 13" in output
    assert output.endswith("Goodbye!\n")


def test_history_and_removal(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["add", "10", "5", "subtract", "20", "7",
                      "history", "remove", "1", "history", "exit"])
    assert "1. Add: 10, 5 = 15" in output
    assert "2. Subtract: 20, 7 = 13" in output
    assert "Removed: Add: 10, 5 = 15" in output
    assert output.endswith("1. Subtract: 20, 7 = 13\nGoodbye!\n")


def test_empty_history(monkeypatch, capsys):
    output = session(monkeypatch, capsys, ["history", "remove", "exit"])
    assert output.count("No calculations in history.") == 2


def test_help_and_unknown_command(monkeypatch, capsys):
    output = session(monkeypatch, capsys, [" HELP ", "pizza", " EXIT "])
    assert "Commands:" in output
    assert "Unknown command." in output
    assert output.endswith("Goodbye!\n")


def test_invalid_first_number_recovers(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["add", "hello", "history", "add", "2", "3", "exit"])
    assert "Invalid number or result." in output
    assert "No calculations in history." in output
    assert "Result: 5" in output


def test_invalid_second_number_recovers(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["subtract", "10", "hello", "history", "subtract", "8", "3", "exit"])
    assert "Invalid number or result." in output
    assert "No calculations in history." in output
    assert "Result: 5" in output


def test_invalid_removal_number_preserves_history(monkeypatch, capsys):
    # Familiar loops exercise several boundary inputs without new test syntax.
    for invalid_number in ["0", "-1", "99"]:
        output = session(monkeypatch, capsys,
                         ["add", "1", "2", "remove", invalid_number, "history", "exit"])
        assert "Calculation does not exist." in output, invalid_number
        assert output.count("1. Add: 1, 2 = 3") == 2, invalid_number


def test_invalid_removal_text_preserves_history(monkeypatch, capsys):
    for invalid_text in ["hello", "1.5"]:
        output = session(monkeypatch, capsys,
                         ["add", "1", "2", "remove", invalid_text, "history", "exit"])
        assert "Please enter a whole calculation number." in output, invalid_text
        assert output.count("1. Add: 1, 2 = 3") == 2, invalid_text


def test_nonfinite_operands_do_not_enter_history(monkeypatch, capsys):
    for operands in [["nan"], ["inf"], ["-inf"], ["1", "nan"]]:
        # List concatenation creates the conversation for each operand example.
        answers = ["add"] + operands + ["history", "add", "2", "3", "exit"]
        output = session(monkeypatch, capsys, answers)
        assert "Invalid number or result." in output, operands
        assert "No calculations in history." in output, operands
        assert "Result: 5" in output, operands


def test_overflow_does_not_enter_history(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["add", "1e308", "1e308", "history", "exit"])
    assert "Invalid number or result." in output
    assert "No calculations in history." in output


def test_blank_command_is_unknown(monkeypatch, capsys):
    output = session(monkeypatch, capsys, ["", "exit"])
    assert "Unknown command." in output
    assert output.endswith("Goodbye!\n")


def test_remove_only_entry(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["add", "-1.5", "0.5", "remove", "1", "history", "exit"])
    assert "Removed: Add: -1.5, 0.5 = -1" in output
    assert "No calculations in history." in output


def test_complete_assignment_session(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["add", "10", "5", "subtract", "20", "7", "add", "100", "50",
                      "history", "remove", "2", "history", "exit"])
    assert "Result: 15\n" in output
    assert "Result: 13\n" in output
    assert "Result: 150\n" in output
    assert "Removed: Subtract: 20, 7 = 13" in output
    assert output.endswith("1. Add: 10, 5 = 15\n2. Add: 100, 50 = 150\nGoodbye!\n")


def test_interrupted_input_exits_cleanly(monkeypatch, capsys):
    # Script answers up to a prompt, then simulate input ending or Ctrl+C.
    prefixes = [[], ["add"], ["add", "1"], ["add", "1", "2", "remove"]]
    for interruption in [EOFError, KeyboardInterrupt]:
        for prefix in prefixes:
            responses = iter(prefix)

            def interrupted_input(prompt):
                try:
                    return next(responses)
                except StopIteration:
                    raise interruption from None

            monkeypatch.setattr("builtins.input", interrupted_input)
            run()
            assert capsys.readouterr().out.endswith("\nGoodbye!\n"), (interruption, prefix)


def test_module_entrypoint(monkeypatch, capsys):
    # runpy exercises python -m calculator's entry module in this process.
    import runpy

    def exit_command(prompt):
        return "exit"

    monkeypatch.setattr("builtins.input", exit_command)
    runpy.run_module("calculator", run_name="__main__")
    output = capsys.readouterr().out
    assert "OOP Calculator" in output
    assert output.endswith("Goodbye!\n")
