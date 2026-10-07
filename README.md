# IS218 Command Factory Statistics Calculator

This project extends the completed OOP calculator with static operations, callable composition, a calculation factory, flexible operands and named settings, command objects, pandas statistics, CSV input, and prepared-sequence execution.

## Requirements

- Python 3.11–3.14
- pandas 2.2+
- pytest 8.3+

Install dependencies:

`py -m pip install -r requirements.txt`

Run the test suite:

`py -m pytest -q`

Start the calculator:

`py -m calculator`

## Supported requests

Examples:

- `add 2 3` → `Result: 5.0000`
- `subtract 2 3` → `Result: -1.0000`
- `multiply 2 3` → `Result: 6.0000`
- `divide 7 2` → `Result: 3.5000`
- `square 3` → `Result: 9.0000`
- `sqrt 9` → `Result: 3.0000`
- `power 3 exponent=4` → `Result: 81.0000`
- `sum 2 3 4` → `Result: 9.0000`
- `mean 2 4 6` → `Result: 4.0000`
- `median 9 1 5` → `Result: 5.0000`
- `stddev 10 20 30 40 50` → `Result: 15.8114`
- `csv mean values.csv`
- `csv median values.csv`
- `csv stddev values.csv`
- `history`
- `clear`
- `help`
- `exit`

Standard deviation defaults to sample deviation (`ddof=1`). `ddof=0` selects population deviation.

## Architecture

`Operations` contains stateless mathematical methods. `Calculation` stores validated operands, a callable operation, and copied named options without executing the operation during construction.

`CalculationFactory` selects a registered operation, validates its operand count and supported settings, and returns an unexecuted `Calculation`. Construction and execution therefore stay separate.

`CalculatorSession` executes a calculation first and records it only after successful completion. `History` owns its private entry list and returns a shallow copy so callers cannot clear or append to the owned collection directly.

Application actions implement the abstract `Command.execute()` contract. `CalculateCommand`, `HistoryCommand`, `ClearHistoryCommand`, and `HelpCommand` reuse the same CLI loop while keeping application actions separate from calculation construction.

CSV loading is an input-source concern. `read_csv_values()` reads the `value` column and supplies ordinary observations to the same factory path used by typed values. The mathematical operations do not know whether values came from a terminal request or a CSV file.

`execute_sequence()` processes already-prepared calculations one at a time. Each item has its own exception boundary, so one expected failure does not stop later calculations. Only successful calculations enter history.

## Error handling

The project uses EAFP where Python or pandas already owns the failure, such as numeric conversion, file reading, division by zero, and square-root domain errors. It uses explicit checks where the application has its own published contract, such as operand counts, supported option names, finite values, required CSV headers, and minimum observation counts.

Failed calculations are not written to history. The CLI reports expected failures as `Error:` and continues accepting requests.

## Independent adaptation: median

The independent extension adds `median` as another collection statistic. It uses the same numeric validation policy as mean and standard deviation and works from both typed values and CSV input.

Components affected:

- `calculator/statistics.py` — defines the shared median policy.
- `calculator/operations.py` — exposes median as a stateless operation.
- `calculator/factory.py` — registers the operation.
- `calculator/cli.py` — permits `csv median PATH`.
- `calculator/commands.py` — documents median in help text.
- `tests/test_adaptation.py` — proves typed, factory, and CSV behavior.

History, session execution, `Calculation`, and CSV file structure did not need special median-specific logic because the existing boundaries already support a new collection operation.

## One successful and one failed request trace

Successful request: `power 3 exponent=4`

The CLI parses the operand and named setting, then asks `CalculationFactory` to construct a `Calculation` holding `Operations.power`, `(3.0,)`, and `{"exponent": 4.0}`. No power calculation occurs during construction. `CalculateCommand.execute()` asks the session to execute it. `Calculation.get_result()` calls the stored operation, producing `81.0`. The session then records `(calculation, 81.0)` and the command returns `Result: 81.0000`.

Failed request: `divide 1 0`

The factory successfully constructs the calculation because zero division does not happen during construction. During command execution, `Operations.divide(1.0, 0.0)` raises `ZeroDivisionError`. Because the session records only after `get_result()` returns successfully, no history entry is added. The CLI catches the expected error, prints `Error:`, and accepts the next request.

## History copy limitation

`History.get_history()` returns a new list, so changing that returned list does not change the collection owned by `History`. It is only a shallow copy: the `Calculation` objects inside the returned entries are still the same objects. Saved numerical results are stored with the calculations so history display does not recalculate old requests.
