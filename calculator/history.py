"""Manage a collection of calculation objects."""

from calculator.calculation import Calculation


class History:
    """Own session history and expose controlled access to its collection."""

    def __init__(self) -> None:
        # An instance attribute gives each History its own list.
        # A leading underscore means internal use by convention, not security.
        # History HAS MANY calculations; it does not inherit from Calculation.
        self._calculations: list[Calculation] = []

    def add(self, calculation: Calculation) -> None:
        """Append a calculation to history."""
        # isinstance accepts subclasses too, including Add and Subtract.
        if not isinstance(calculation, Calculation):
            raise TypeError("History accepts Calculation objects only.")
        self._calculations.append(calculation)

    def get_history(self) -> list[Calculation]:
        """Return a copy so callers cannot modify the internal list."""
        # This is a shallow copy: the list is new, its calculation objects are not.
        # Clearing this returned list cannot erase History's internal entries.
        return self._calculations.copy()

    def remove(self, index: int) -> Calculation:
        """Remove and return a calculation by its zero-based index."""
        # Python allows negative indexes, but our public method rejects them.
        # Validate before changing state so invalid requests preserve history.
        if index < 0 or index >= len(self._calculations):
            raise IndexError("Calculation does not exist.")
        return self._calculations.pop(index)  # pop both removes and returns an item.
