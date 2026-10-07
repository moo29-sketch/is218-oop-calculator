# OOP Calculator

This project is a command-line calculator built with object-oriented Python. It supports addition and subtraction, keeps a calculation history for the current session, lets the user remove saved calculations, and handles bad input without crashing.

Repository URL after publishing:
https://github.com/moo29-sketch/is218-oop-calculator

## Features

The calculator supports six commands:

- `add` — add two numbers and save the successful calculation
- `subtract` — subtract the second number from the first and save the successful calculation
- `history` — show the calculations saved during the current session
- `remove` — remove a calculation using the number shown in history
- `help` — display the available commands
- `exit` — end the calculator session

Invalid numbers, unknown commands, invalid removals, Ctrl+C, and end-of-input are handled without crashing the program. `nan`, positive or negative infinity, and results that overflow to infinity are rejected and are not added to history.

## Requirements

- Python 3.11 or newer
- pip

The automated GitHub workflow checks Python 3.11, 3.12, 3.13, and 3.14.

## Installation

Clone the repository and enter the project folder:

```text
git clone https://github.com/moo29-sketch/is218-oop-calculator.git
cd is218-oop-calculator
```

Create a virtual environment:

Windows PowerShell:

```text
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```text
python3 -m venv .venv
source .venv/bin/activate
```

Install the testing dependencies:

```text
python -m pip install -r requirements.txt
```

## Run the calculator

```text
python -m calculator
```

Example session:

```text
OOP Calculator

Type "help" for commands.
> add
First number: 10
Second number: 5
Result: 15
> subtract
First number: 20
Second number: 7
Result: 13
> history
Calculation History

1. Add: 10, 5 = 15
2. Subtract: 20, 7 = 13
> exit
Goodbye!
```

History only lasts for the current run of the program.

## Run the tests

```text
python -m pytest
```

The pytest configuration measures both line and branch coverage for the `calculator` package and requires 100% coverage. The project contains 37 test functions covering the calculation classes, history behavior, REPL behavior, invalid input, interrupts, and the module entry point.

## Design choices

`Calculation` is an abstract base class that stores two operands and requires subclasses to implement `get_result()`. `Add` and `Subtract` inherit from that class and provide their own arithmetic. Code that receives a `Calculation` can call the same method without checking which concrete operation it was given.

`History` owns the collection of successful calculation objects. The internal list is not exposed directly; `get_history()` returns a copy. This keeps other parts of the program from accidentally clearing or replacing the history. Invalid removal requests are rejected before the list changes.

The command-line interface is kept separate from the calculation classes. It converts user input, chooses the requested operation class, displays results, and saves only successful calculations. This keeps input/output concerns out of the arithmetic classes.

## Continuous integration

`.github/workflows/tests.yml` runs the complete pytest suite on GitHub Actions for Python 3.11, 3.12, 3.13, and 3.14. Each job installs the packages in `requirements.txt` and then runs `python -m pytest`, so the same coverage requirement used locally is also enforced in CI.

If tests pass but the workflow still reports a coverage failure, I would read the coverage table and look at the `Missing` column first. That tells me which lines or branches were not executed. I would then reproduce the missing path locally, add a test that exercises that behavior, and rerun the full suite before pushing again. A coverage failure is different from an assertion failure because the behavior tests may all be correct while part of the application is still untested.

## Stage 6 reflection

### 1. Where would Multiply belong?

I would create a `Multiply` class that inherits from `Calculation` and implements `get_result()` by returning `self.a * self.b`. Then I would register the command in the CLI operations dictionary, add `multiply` to the help text, and add tests for normal multiplication, negative values, zero, decimals, and CLI history output. `History` would not need multiplication-specific code because it already stores any object that follows the `Calculation` contract. That is one advantage of using a common abstraction instead of putting arithmetic rules inside the history class.

### 2. What contract could email and text-message notifications share?

Email and text-message notification classes could share a `Notification` interface or abstract base class with a `send()` method. Code that needs to deliver a message could work with the shared contract and call `send()` without needing separate branches for email and SMS. Each concrete notification class would handle its own delivery details.

### 3. What transfers to another language?

The main design ideas transfer even when the syntax changes. I can still separate responsibilities, define a common interface, use different implementations through the same contract, hide a collection behind methods, and test observable behavior. In another language I would still need to learn its class syntax, visibility rules, type system, error handling, package/module system, testing tools, and runtime behavior. The design questions transfer more directly than the exact Python grammar.

## README usability improvement

A setup instruction that can easily confuse users is virtual-environment activation because the command is different on Windows and macOS/Linux. This README lists both versions instead of giving one command and assuming it works everywhere.
