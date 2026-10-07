"""A shared calculation contract and its concrete implementations."""

from abc import ABC, abstractmethod


# ABC makes this an abstract base class: a shared contract for subclasses.
# Calculation describes the idea of an operation; Add and Subtract perform one.
class Calculation(ABC):
    """Store two operands and require subclasses to provide a result."""

    def __init__(self, a: float, b: float) -> None:
        # Python calls __init__ when an object is created. self is that object.
        # Each instance stores its own operands as attributes.
        # For Add(10, 5), self is that new Add object, a is 10, and b is 5.
        # Type hints document expected types; they do not validate values.
        self.a = a
        self.b = b

    @abstractmethod
    def get_result(self) -> float:
        """Return the result of this calculation."""
        # The docstring is a valid method body. There is no shared arithmetic.
        # Concrete subclasses must override this method before instantiation.


class Add(Calculation):
    """Add the two operands."""

    def get_result(self) -> float:
        # Inheritance gives Add the parent's __init__ and operand attributes.
        return self.a + self.b


class Subtract(Calculation):
    """Subtract the second operand from the first."""

    def get_result(self) -> float:
        # Same interface, different behavior: callers still use get_result().
        return self.a - self.b
