# app/exceptions.py
class CalculationError(Exception):
    """Base class for calculation errors."""

class DivisionByZeroError(CalculationError):
    """Raised when dividing by zero."""

class InvalidInputError(CalculationError):
    """Raised for invalid user input."""

class ConfigError(Exception):
    """Configuration error."""