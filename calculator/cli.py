"""Read, evaluate, print, and loop until the user exits."""

from math import isfinite

from calculator.calculation import Add, Calculation, Subtract
from calculator.history import History


HELP = """Commands:
  add       Add two numbers
  subtract  Subtract the second number from the first
  history   Show this session's calculations
  remove    Remove a calculation by its displayed number
  help      Show available commands
  exit      Exit the calculator"""


def describe(calculation: Calculation) -> str:
    """Format any calculation through its common interface."""
    # Polymorphism: get_result() chooses the object's implementation for us.
    # The class name is only a display label, not a decision about arithmetic.
    # An f-string inserts values; :g displays numbers compactly (15, not 15.0).
    return (
        f"{type(calculation).__name__}: "
        f"{calculation.a:g}, {calculation.b:g} = {calculation.get_result():g}"
    )


def show_history(history: History) -> None:
    """Display a snapshot without changing the collection."""
    calculations = history.get_history()
    # An empty list is false in a condition. Return ends this function early.
    if not calculations:
        print("No calculations in history.")
        return
    print("Calculation History\n")
    # enumerate supplies a display number and an object on each iteration.
    for number, calculation in enumerate(calculations, start=1):
        print(f"{number}. {describe(calculation)}")


def read_number(prompt: str) -> float:
    """Convert terminal text into a finite floating-point number."""
    # input returns text. float converts it or raises ValueError.
    number = float(input(prompt))
    # float also accepts nan and inf; reject those explicitly for this CLI.
    if not isfinite(number):
        raise ValueError("A finite number is required.")
    return number


def run() -> None:
    """Run one independent calculator session."""
    history = History()
    # The dictionary stores classes, not objects. Calling a selected class
    # constructs the operation requested by the user.
    operations = {"add": Add, "subtract": Subtract}
    print('OOP Calculator\n\nType "help" for commands.')
    while True:
        try:
            # READ: normalize whitespace and case before interpreting a command.
            command = input("> ").strip().lower()
            if command == "exit":
                # break leaves the loop; the farewell runs below it.
                break
            # EVALUATE: select an operation and collect its operands.
            if command in operations:
                try:
                    a = read_number("First number: ")
                    b = read_number("Second number: ")
                    # For command == "add", this is the same as Add(a, b).
                    operation_class = operations[command]
                    calculation = operation_class(a, b)
                    # Even finite operands can produce an infinite result.
                    result = calculation.get_result()
                    if not isfinite(result):
                        raise ValueError("Result is outside the supported range.")
                except ValueError:
                    print("Invalid number or result. Please use finite numbers.")
                    # continue starts the next loop without recording bad input.
                    continue
                # Save only successful calculations through History's interface.
                history.add(calculation)
                # PRINT, then LOOP: reaching the end returns to the next prompt.
                print(f"Result: {result:g}")
            elif command == "history":
                show_history(history)
            elif command == "remove":
                show_history(history)
                if not history.get_history():
                    continue
                try:
                    number = int(input("Enter calculation number to remove: "))
                    # Users count from 1; Python list indexes start at 0.
                    removed = history.remove(number - 1)
                # Catch specific errors so each mistake gets a useful message.
                except ValueError:
                    print("Please enter a whole calculation number.")
                except IndexError:
                    print("Calculation does not exist.")
                else:
                    # A try/except else runs only if the try block succeeded.
                    print(f"Removed: {describe(removed)}")
            elif command == "help":
                print(HELP)
            else:
                print('Unknown command.\nType "help" for available commands.')
        except (EOFError, KeyboardInterrupt):
            # The outer handler covers every prompt, including operand input.
            # EOF means input ended; KeyboardInterrupt usually means Ctrl+C.
            print()
            break
    print("Goodbye!")
