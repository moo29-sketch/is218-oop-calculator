"""Shared finite-number conversion and pandas statistical policy."""
from math import isfinite
import pandas as pd


from calculator.validation import numeric_values


def mean(values) -> float:
    numbers = numeric_values(values)
    if not numbers:
        raise ValueError("Enter at least one value.")
    result = float(pd.Series(numbers, dtype=float).mean())
    if not isfinite(result):
        raise ValueError("Result is outside the supported range.")
    return result



def median(values) -> float:
    """Return the median using the same finite-number policy as other statistics."""
    numbers = numeric_values(values)
    if not numbers:
        raise ValueError("Enter at least one value.")
    result = float(pd.Series(numbers, dtype=float).median())
    if not isfinite(result):
        raise ValueError("Result is outside the supported range.")
    return result


def standard_deviation(values, *, ddof=1) -> float:
    """Default to sample deviation; permit explicit population policy."""
    if ddof not in (0, 1):
        raise ValueError("ddof must be 0 (population) or 1 (sample).")
    numbers = numeric_values(values)
    if len(numbers) < 2:
        raise ValueError("Enter at least two values.")
    result = float(pd.Series(numbers, dtype=float).std(ddof=ddof))
    if not isfinite(result):
        raise ValueError("Result is outside the supported range.")
    return result
