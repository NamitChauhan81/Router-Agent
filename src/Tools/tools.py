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


@tool
def Send_Email(email_adderss: str, message: str) -> str:
        """This tool sends message via email to a specific email adderess."""
        return f"""{message} is sent to {email_adderss}"""


@tool
def get_current_stock_price(stock_symbol: str)-> str:
        """This tool gives the current stock price of any listed stock."""

        return f"""The current stock price of {stock_symbol} is $241.5"""
@tool
def Purchase_Stocks(stock_symbol: str, quantity : int)-> str:
        """Simulating the purchasing of a given quantity of a particular stock symbol."""

        return f"purchase order placed for {quantity} shares of {stock_symbol}"

