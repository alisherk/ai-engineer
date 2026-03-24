from typing import Annotated

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from src.app.settings import get_settings

settings = get_settings()

class State(BaseModel):
    messages: Annotated[list, add_messages]

# 1: Create a StateGraph
graph_builder = StateGraph(State)

llm = ChatOpenAI(model=settings.openai_model)

# Step 2: Create Node Functions
def chatbot_node(old_state: State) -> State:
    response = llm.invoke(old_state.messages)
    new_state = State(messages=[response])
    return new_state

# Step 3: Create Nodes
graph_builder.add_node("chatbot", chatbot_node)

# Step 4: Create Edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


def chat(user_input: str, history):
    initial_state = State(messages=[{"role": "user", "content": user_input}])
    graph = graph_builder.compile()
    result = graph.invoke(initial_state)
    # print(result)
    return result['messages'][-1].content

resp = chat("Hello, how are you?", [])
print(resp)

