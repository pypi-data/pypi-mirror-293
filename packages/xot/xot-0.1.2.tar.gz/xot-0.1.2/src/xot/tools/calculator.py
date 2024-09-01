"""
This module provides a calculator tool implementation.

It defines a Calculator class that can perform basic arithmetic operations.
"""

from .base_tool import BaseTool, ToolRegistry


@ToolRegistry.register("calculator")
class Calculator(BaseTool):
    """
    A calculator tool for performing basic arithmetic operations.

    This tool evaluates mathematical expressions provided as strings and
    returns the result with a configurable precision.
    """

    def __init__(self, precision: int = 4, scientific_notation: bool = False):
        self.precision = precision
        self.scientific_notation = scientific_notation

    def use(self, input_text: str) -> str:
        """
        Evaluate the given mathematical expression and return the result with the configured precision.

        Args:
            input_text (str): A string containing a mathematical expression to be evaluated.

        Returns:
            str: The result of the calculation as a string formatted to the specified precision,
                 or an error message if the evaluation fails.

        Examples:
            >>> calc = Calculator()
            >>> calc.use("3 + 2")
            '5'
            >>> calc.use("10 / 3")
            '3.3333'
            >>> calc.use("500 / 200")
            '2.5'
            >>> calc.use("invalid input")
            'Error: Invalid expression'
        """
        try:
            result = eval(input_text)
            if self.scientific_notation:
                return f"{result:.{self.precision}e}"
            result = round(result, self.precision)
            result_str = str(result)
            if result_str.endswith(".0"):
                return str(int(result))
            if "e" in str(result_str):
                return f"{result:.{self.precision}f}"
            return str(result_str)
        except Exception as e:
            return f"Error: {str(e)}"

    @classmethod
    def name(cls) -> str:
        return "calculator"
