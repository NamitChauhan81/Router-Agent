from langchain_core.tools import tool
import math

@tool 
def get_weather(city: str)-> str:
    """This is a weather tool returns the current weather of the specific city or a region."""

    return f"It is currently sunny in {city} with a high of 32 and low of 23"

@tool
def calculator(expression: str) -> str:
    """Performs arithmetic calculations. 
    
    Args:
        expression: The math expression to evaluate, for example '25 * 4'.
    """
    try:
        # Restrict built-ins for safe evaluation
        allowed_names = {"abs": abs, "round": round, "min": min, "max": max, "sum": sum, "pow": pow}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"The result is: {result}"
    except Exception as error:
        return f"Error evaluating expression: {error}"