"""Launch with python -m calculator."""

from calculator.cli import run

# Python executes this module when the user types python -m calculator.
# Keep arithmetic and the REPL in other modules so tests can import them.
run()
