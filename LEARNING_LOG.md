# Learning Log

## Part 1 — Static operations and callable composition

Starting point: the prerequisite calculator used calculation subclasses to encode different arithmetic behaviors.

Prediction: if behavior becomes a stored callable, constructing a calculation should not execute the math.

Evidence: `test_construction_defers_execution_and_snapshots_inputs` uses a spy callable. The call list remains empty after construction and receives one call only when `get_result()` runs. Earlier arithmetic behavior remains covered by the operations tests.

Change in relationship: inheritance is no longer needed to create one class per mathematical operation. `Calculation` stores data plus a callable. Inheritance is still useful later for commands because different application actions share the `execute()` contract.

## Part 2 — Calculation factory

Prediction: the factory should select and configure a calculation but should not perform the calculation.

Evidence: `test_factory_does_not_execute` creates division by zero without an exception. The exception occurs only when `get_result()` executes. This distinguishes construction from execution.

Successful trace: `CalculationFactory.create("add", 2, 3)` selects `Operations.add`, validates two values, and returns a `Calculation`.

Failed trace: `CalculationFactory.create("unknown", 1, 2)` fails during preparation because no operation is registered for that name. No calculation reaches the session.

## Part 3 — Flexible operands and named settings

Prediction: fixed binary operand fields cannot represent unary operations, collection operations, and configured operations cleanly.

Evidence: factory tests cover square/sqrt with one operand, add with exactly two, mean/stddev with collections, and power with a named exponent. A nondefault exponent proves that `**options` are forwarded instead of merely stored.

Operands are positional mathematical values. Named settings configure how an operation interprets those values. Collection unpacking turns the stored tuple into separate positional arguments only when the stored callable is invoked.

## Part 4 — Commands and successful-only history

Prediction: application actions such as history and clear should share a command contract without editing history internals directly.

Evidence: command tests show successful calculations are recorded, failed division is not recorded, history can be displayed, and clear works through the session.

History owns the collection. A returned shallow copy protects membership but not deep immutability of contained objects. Saved results are displayed rather than recalculated, so viewing history cannot accidentally run a calculation again.

## Part 5 — pandas statistics and CSV input

Prediction: typed values and CSV values should share one mathematical policy after the input source supplies observations.

Evidence: `test_sources_share_calculation_policy` compares manual and CSV mean/stddev results. Missing columns, missing files, missing observations, and blank-line behavior are checked separately.

Flow: DataFrame → `value` Series → Python list → numeric tuple → factory-created Calculation → shared operation → saved result.

EAFP is used for file access and conversion because those operations already report useful failures. Explicit checks enforce application-specific rules such as required headers, minimum counts, finite values, and ddof policy.

## Part 6 — Prepared sequences and transfer

Prediction: if each item has its own try/except boundary, one failing calculation should not stop later prepared calculations.

Evidence: `test_sequence_continues_after_failure_and_records_only_success` runs add, failing divide, then square. Results contain `5.0` and `9.0`, one error is retained, and history contains exactly two successful calculations.

Independent adaptation: median was added without adding a new command hierarchy or file-aware math. The change affected the shared statistic, operations registry, factory registry, CSV operation allow-list, help text, and tests. Session/history/calculation boundaries stayed unchanged.

Current evidence limitation: passing tests establish the published cases that are asserted, not every possible input. CI establishes the checked revision on the configured Python versions; an older green run does not establish a later revision.
