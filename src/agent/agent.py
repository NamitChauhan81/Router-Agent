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

load_dotenv()

llm = ChatGoogleGenerativeAI(model = "gemini-3-flash-preview")

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

