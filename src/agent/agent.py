from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated,Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from Tools.tools import Send_Email, get_current_stock_price, get_weather, calculator, Purchase_Stocks

load_dotenv()

Email_Tools = [Send_Email]

Stock_Tools = [get_current_stock_price, Purchase_Stocks, calculator]

General_Tools = [get_weather, calculator]

Email_Tool_Node = ToolNode(Email_Tools)

Stock_Tool_Node = ToolNode(Stock_Tools)

General_Tool_Node = ToolNode(General_Tools)


llm = ChatGoogleGenerativeAI(model = "gemini-3-flash-preview")

Email_llm = llm.bind_tools(Email_Tools)

Stock_llm = llm.bind_tools(Stock_Tools)

General_llm = llm.bind_tools(General_Tools)



class route_schema(BaseModel):
    route : Literal["Stock_Market", "Email", "Coding", "Research", "SQL", "General"]= Field(description="Best Specialist for the question")

class Router_Agent_State(TypedDict):
    route: str
    messages : Annotated[list[BaseMessage], add_messages]


Routing_Model = llm.with_structured_output(route_schema)

def Router_Agent(state : Router_Agent_State):
    system = [SystemMessage(content="""You are a Router Agent give a best sutaible route for the user query.
                                     Stock_Market:
                                     Buying Stocks, get current stock price, etc.

                                     Coding :
                                     bug fixes, programing, APIs, etc.

                                     SQL:
                                     Database queries, sql , etc.

                                     Email:
                                     sending email, drafing email.

                                     Research :
                                     Investigation, Comparision, Expalnation.

                                     General :
                                     Everything else 
       """)]
    messages = system +[state["messages"][-1]]

    route = Routing_Model.invoke(messages)

    return {"route": route.route}




def Coding_Agent(state:Router_Agent_State):

  query = state["messages"][-1]

  prompt = f"""You are a coding specialist 
  give a appropriate solution to the user query.

  query: {query}
  """
  answer = llm.invoke(prompt)

  final_ansewr = answer.content
  return {"messages":[final_ansewr]}

def SQL_Agent(state : Router_Agent_State):
    query = state["messages"][-1]
    prompt = f"""You are a SQL specialist if the user qurey related to Database or SQL,
    Give the appropriate solution.
    query : {query}
    """

    result = llm.invoke(prompt)

    final_result = result.content

    return{"messages": [final_result]}




def Research_Agent(state : Router_Agent_State):
    query = state["messages"][-1]
    prompt = f"""You are a Research specialist,
    Give a concise and conceptual explanation about the below context.

    context : {query}
  
    """

    result = llm.invoke(prompt)

    final_result = result.content

    return{"messages": [final_result]}


def General_Agent(state : Router_Agent_State):
    system = [SystemMessage(content="""You are a General agent use available tools to achieve the specific task.""")]
    query = state["messages"][-1]
    prompt = system + [query]

    response = General_llm.invoke(prompt)

    return{"messages": [response]}

def Email_Agent(state:Router_Agent_State):
    system = [SystemMessage(content="""You are a email agent use available tools to achieve the specific task.""")]
    prompt = system + [state["messages"][-1]]
    response = Email_llm.invoke(prompt)

    return {"messages": [response]}

def Stock_Market_Agent(state: Router_Agent_State):
    system = [SystemMessage(content="""You are a Stock Market agent use available tools to Know current stock price, buy stocks""")]
    prompt = system +[state["messages"][-1]]
    response = Stock_llm.invoke(prompt)
    return{"messages":[response]}