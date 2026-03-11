from typing import TypedDict

import gradio as gr
import requests
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
#from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver
from typing_extensions import Annotated
import sqlite3
from pathlib import Path

from src.app.settings import get_settings

settings = get_settings()


serper = GoogleSerperAPIWrapper()
tool_search = Tool(
    name="search",
    func=serper.run,
    description="Useful for when you need more information from an online search",
)


def push(text: str):
    """Send a push notification to the user"""
    requests.post(
        settings.pushover_api,
        data={
            "token": settings.pushover_token,
            "user": settings.pushover_user,
            "message": text,
        },
    )
tool_push = Tool(
    name="send_push_notification",
    func=push,
    description="useful for when you want to send a push notification",
)

tools = [tool_search, tool_push]

# Step 1: Define state of the graph
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Step 2: Create a StateGraph
graph_builder = StateGraph(State)

llm = ChatOpenAI(model=settings.openai_model)
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Step 3: Create Nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

# Step 4: Create Edges
# why do we need conditional edges? Because we only want to go to the tools node if the chatbot decides to call a tool. If we just add an edge from chatbot to tools, then we would always go to the tools node after the chatbot, which is not what we want.
graph_builder.add_conditional_edges("chatbot", tools_condition, "tools")

# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

"""
can use different checkpointer implementations to store the state of the graph in different places. The MemorySaver will just store the state in memory, while the SqliteSaver will store the state in a sqlite database
memory = MemorySaver()
"""

db_path = Path(__file__).parent / "db.sqlite"
conn = sqlite3.connect(db_path, check_same_thread=False)
sql_memory = SqliteSaver(conn)

graph = graph_builder.compile(checkpointer=sql_memory)

config = {"configurable": {"thread_id": "1"}}
def chat(user_input: str, history):
    result = graph.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
    )

    return result["messages"][-1].content


gr.ChatInterface(chat).launch()

# print(list(graph.get_state(config)))
# print(list(graph.get_state_history(config)))

""" 
code to visualize our graph
png_bytes = graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png_bytes)
print("Graph saved to graph.png") """
