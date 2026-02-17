from pydantic import BaseModel, Field
from agents.agent import Agent
from src.app.ai_researcher.agent_name_enum import AgentNames
from src.app.settings import get_settings

settings = get_settings()

HOW_MANY_SEARCHES = 5

INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."


class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    
planner_agent = Agent(
    name=AgentNames.PLANNER_AGENT.value,
    instructions=INSTRUCTIONS,
    model=settings.openai_model,
    output_type=WebSearchPlan,
)