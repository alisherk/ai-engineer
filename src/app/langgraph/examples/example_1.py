import random
from typing import Annotated

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from src.app.settings import get_settings

settings = get_settings()

nouns = [
    "Cabbages",
    "Unicorns",
    "Toasters",
    "Penguins",
    "Bananas",
    "Zombies",
    "Rainbows",
    "Eels",
    "Pickles",
    "Muffins",
]
adjectives = [
    "outrageous",
    "smelly",
    "pedantic",
    "existential",
    "moody",
    "sparkly",
    "untrustworthy",
    "sarcastic",
    "squishy",
    "haunted",
]


class State(BaseModel):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


def our_first_node(old_state: State) -> State:
    reply = f"{random.choice(nouns)} are {random.choice(adjectives)}"
    messages = [{"role": "assistant", "content": reply}]
    return State(messages=messages)


graph_builder.add_node("first_node", our_first_node)

graph_builder.add_edge(START, "first_node")
graph_builder.add_edge("first_node", END)

graph = graph_builder.compile()

def chat(user_input: str, history):
    message = {"role": "user", "content": user_input}
    messages = [message]
    state = State(messages=messages)
    result = graph.invoke(state)
    #print(result)
    return result["messages"][-1].content

response = chat("Tell me something interesting!", [])
print(response)