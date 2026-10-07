"""Preserve the previous project's controlled history boundary."""
from calculator.calculation import Calculation


class History:
    def __init__(self):
        self._entries = []

    def add(self, calculation, result) -> None:
        if not isinstance(calculation, Calculation):
            raise TypeError("History accepts Calculation objects only.")
        self._entries.append((calculation, result))

    def get_history(self):
        # A new list protects membership; the Calculation objects remain shared.
        return self._entries.copy()

    def clear(self) -> None:
        self._entries.clear()
