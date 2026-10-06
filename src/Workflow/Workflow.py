from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from agent.agent import( Router_Agent_State, Router_Agent, Coding_Agent, General_Agent, SQL_Agent, Research_Agent, Stock_Market_Agent, Email_Agent)
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition



def Choose_Route(state: Router_Agent_State):
    if state["route"]== "Coding":
        return "Coding"
    elif state["route"]=="SQL":
        return "SQL"
    elif state["route"]=="Research":
        return "Research"
    elif state["route"]=="Email":
        return "Email"
    elif state["route"]=="Stock_Market":
        return "Stock_Market"
    else:
        return "General"


graph = StateGraph(Router_Agent_State)

graph.add_node("Router_Agent", Router_Agent)
graph.add_node("Coding_Agent", Coding_Agent)
graph.add_node("Research_Agent", Research_Agent)
graph.add_node("SQL_Agent", SQL_Agent)
graph.add_node("General_Agent", General_Agent)
graph.add_node("Stock_Market_Agent", Stock_Market_Agent)
graph.add_node("Email_Agent", Email_Agent)



graph.add_edge(START, "Router_Agent")
graph.add_conditional_edges("Router_Agent", Choose_Route, {"Coding":"Coding_Agent", 
                                                           "SQL": "SQL_Agent", 
                                                           "Research":"Research_Agent",
                                                             "Stock_Market": "Stock_Market_Agent",
                                                             "Email":"Email_Agent",
                                                             "General":"General_Agent"})
graph.add_edge("Coding_Agent", END)
graph.add_edge("SQL_Agent", END)
graph.add_edge("Research_Agent", END)

