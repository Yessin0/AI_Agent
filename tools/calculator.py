from langchain.tools import Tool

def get_calculator_tool() -> Tool:
    """
    Internal tool: safely evaluates mathematical expressions.
    No external API needed.
    """

    def calculate(expression: str) -> str:
        try:
            # Only allow safe math characters
            allowed = set("0123456789+-*/()., **%")
            if not all(c in allowed for c in expression.replace(" ", "")):
                return "Error: Invalid characters in expression."

            result = eval(expression, {"__builtins__": {}})
            return f"Result: {result}"
        except ZeroDivisionError:
            return "Error: Division by zero."
        except Exception as e:
            return f"Calculation error: {str(e)}"

    return Tool(
        name="calculator",
        func=calculate,
        description=(
            "Useful for solving mathematical expressions and calculations. "
            "Input should be a valid math expression like '2 + 2' or '(10 * 5) / 2'. "
            "Supports +, -, *, /, ** (power), % (modulo)."
        )
    )