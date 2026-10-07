"""A calculation stores inputs and a callable, without executing it yet."""
from math import isfinite
from calculator.validation import numeric_values


class Calculation:
    def __init__(self, values, operation, **options):
        self.values = numeric_values(values)
        self.operation = operation
        self.options = dict(options)

    def get_result(self) -> float:
        result = float(self.operation(*self.values, **self.options))
        if not isfinite(result):
            raise ValueError("Result is outside the supported range.")
        return result
