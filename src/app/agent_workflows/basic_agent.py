import asyncio
from agents.tracing import trace
from agents.run import Runner
from agents.agent import Agent

from src.app.settings import get_settings

settings = get_settings()

agent = Agent(
    name="Jokster",
    instructions="Your job is to tell jokes",
    model=settings.openai_model,
)

async def main():
    with trace("Running the agent to tell a joke"):
        result = await Runner().run(agent, "Tell me a joke about airplanes")
        print(result.final_output)


asyncio.run(main())
